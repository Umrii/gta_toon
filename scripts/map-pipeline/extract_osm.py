"""Extract the initial TYNE CITY area from OpenStreetMap.

Run from the repository root:
    python -m pip install -r scripts/map-pipeline/requirements.txt
    python scripts/map-pipeline/extract_osm.py

Raw downloads are written under data/raw (gitignored). Processed GeoJSON
and a provenance manifest are written under data/processed.
"""
from __future__ import annotations

import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import geopandas as gpd
import osmnx as ox
from shapely.geometry import box

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "data" / "configs" / "newcastle-core.json"
RAW_DIR = ROOT / "data" / "raw" / "osm"
PROCESSED_DIR = ROOT / "data" / "processed" / "osm"
LOG = logging.getLogger("tyne_city.map_pipeline")


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def with_retries(label: str, operation, attempts: int = 3):
    """Retry transient Overpass/network errors with bounded backoff."""
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception:
            if attempt == attempts:
                raise
            delay = min(10 * (2 ** (attempt - 1)), 60)
            LOG.warning("%s failed (attempt %s/%s); retrying in %ss",
                        label, attempt, attempts, delay)
            time.sleep(delay)


def clean_properties(frame: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Keep useful OSM tags while ensuring a serialisable GeoDataFrame."""
    if frame.empty:
        return frame
    frame = frame.copy()
    frame = frame[frame.geometry.notna() & ~frame.geometry.is_empty]
    return frame


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    cfg = load_config()
    bbox = cfg["bbox"]
    # OSMnx 2.x: bbox order is (left, bottom, right, top).
    bbox_tuple = (bbox["west"], bbox["south"], bbox["east"], bbox["north"])
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    ox.settings.timeout = int(cfg["overpass"]["timeout_seconds"])
    ox.settings.max_query_area_size = 50_000_000

    LOG.info("OSMnx version: %s", ox.__version__)
    LOG.info("Extracting roads for bbox %s", bbox_tuple)
    graph = with_retries(
        "road network",
        lambda: ox.graph.graph_from_bbox(
            bbox_tuple, network_type=cfg["features"]["roads_network_type"],
            simplify=True, retain_all=True,
        ),
        int(cfg["overpass"]["max_retries"]),
    )

    # Save reproducible raw graph before projection or clipping.
    ox.io.save_graphml(graph, RAW_DIR / "roads.graphml")
    nodes, edges = ox.convert.graph_to_gdfs(graph)
    if edges.crs is None:
        raise ValueError("OSM road graph has no CRS")

    LOG.info("Extracting building footprints")
    tags = {"building": True}
    buildings = with_retries(
        "building footprints",
        lambda: ox.features.features_from_bbox(bbox_tuple, tags=tags),
        int(cfg["overpass"]["max_retries"]),
    )
    buildings = clean_properties(buildings)
    buildings = buildings[
        buildings.geometry.geom_type.isin(["Polygon", "MultiPolygon"])
    ].copy()

    # Additional polygonal features. Separate queries keep tags explicit.
    extras: dict[str, gpd.GeoDataFrame] = {}
    for name, feature_tags in {
        "parks": {"leisure": ["park", "garden"], "landuse": ["grass", "recreation_ground"]},
        "water": {"natural": ["water"], "waterway": ["riverbank"]},
    }.items():
        LOG.info("Extracting %s", name)
        extras[name] = with_retries(
            name,
            lambda feature_tags=feature_tags: ox.features.features_from_bbox(
                bbox_tuple, tags=feature_tags
            ),
            int(cfg["overpass"]["max_retries"]),
        )
        extras[name] = clean_properties(extras[name])

    # Reproject to British National Grid, clip and export consistent GeoJSON.
    target_crs = cfg["coordinate_system"]["projected_crs"]
    bounds_geom = gpd.GeoSeries([box(
        bbox["west"], bbox["south"], bbox["east"], bbox["north"]
    )], crs="EPSG:4326").to_crs(target_crs).iloc[0]

    layers: dict[str, gpd.GeoDataFrame] = {
        "roads": edges.to_crs(target_crs),
        "buildings": buildings.to_crs(target_crs),
        **{name: layer.to_crs(target_crs) for name, layer in extras.items()},
    }

    counts: dict[str, int] = {}
    for name, layer in layers.items():
        clipped = layer.clip(bounds_geom)
        clipped = clean_properties(clipped)
        # OSM IDs/index are retained in GeoJSON properties where supported.
        out = PROCESSED_DIR / f"{name}.geojson"
        clipped.to_crs("EPSG:4326").to_file(out, driver="GeoJSON")
        counts[name] = len(clipped)
        LOG.info("%s: %s features -> %s", name, counts[name], out.relative_to(ROOT))

    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "dataset": "TYNE CITY Newcastle core",
        "source": "OpenStreetMap contributors",
        "source_url": "https://www.openstreetmap.org/copyright",
        "license": "ODbL-1.0",
        "retrieved_at": retrieved_at,
        "osmnx_version": ox.__version__,
        "source_crs": "EPSG:4326",
        "projected_crs": target_crs,
        "bbox": bbox,
        "axis_convention": "Three.js X=east, Y=elevation, Z=south",
        "counts": counts,
        "outputs": {name: f"{name}.geojson" for name in counts},
        "notes": [
            "Building heights are not inferred in this extraction stage.",
            "All geometry exports retain source OSM tags where available.",
            "Derived OSM database content remains subject to ODbL obligations."
        ]
    }
    (PROCESSED_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    LOG.info("Extraction complete. Manifest: %s", PROCESSED_DIR / "manifest.json")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        LOG.exception("Map extraction failed: %s", exc)
        raise
