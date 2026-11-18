"""Extract the provisional TYNE CITY Newcastle core from OpenStreetMap.

From the repository root:
    python -m pip install -r scripts/map-pipeline/requirements.txt
    python scripts/map-pipeline/extract_osm.py --check-config
    python scripts/map-pipeline/extract_osm.py --confirm-boundary

The explicit confirmation flag prevents an accidental network query before
the project owner has approved the configured boundary.
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

import geopandas as gpd
import osmnx as ox
from pyproj import Transformer
from shapely.geometry import box

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "data" / "configs" / "newcastle-core.json"
RAW_DIR = ROOT / "data" / "raw" / "osm"
PROCESSED_DIR = ROOT / "data" / "processed" / "osm"
LOG = logging.getLogger("tyne_city.map_pipeline")

T = TypeVar("T")


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def validate_config(cfg: dict[str, Any]) -> None:
    bbox = cfg["bbox"]
    west, south, east, north = (
        float(bbox["west"]),
        float(bbox["south"]),
        float(bbox["east"]),
        float(bbox["north"]),
    )
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise ValueError("Invalid bbox: expected west < east and south < north in EPSG:4326")

    origin = cfg["coordinate_system"]["local_origin"]
    if not (-90 <= float(origin["latitude"]) <= 90):
        raise ValueError("Local origin latitude is outside valid bounds")
    if not (-180 <= float(origin["longitude"]) <= 180):
        raise ValueError("Local origin longitude is outside valid bounds")

    if float(cfg["coordinate_system"].get("scale", 1.0)) <= 0:
        raise ValueError("Coordinate scale must be positive")


def with_retries(label: str, operation: Callable[[], T], attempts: int, base_delay: int) -> T:
    """Retry transient service/network errors with bounded exponential backoff."""
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception:
            if attempt == attempts:
                raise
            delay = min(base_delay * (2 ** (attempt - 1)), 60)
            LOG.warning("%s failed (attempt %s/%s); retrying in %ss",
                        label, attempt, attempts, delay)
            time.sleep(delay)
    raise RuntimeError(f"{label} failed without returning a result")


def clean_geometries(frame: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if frame.empty:
        return frame
    cleaned = frame.copy()
    cleaned = cleaned[cleaned.geometry.notna() & ~cleaned.geometry.is_empty]
    return cleaned


def write_geojson(frame: gpd.GeoDataFrame, output: Path) -> None:
    """Write WGS84 GeoJSON, including a valid empty FeatureCollection."""
    if frame.empty:
        output.write_text(
            json.dumps({"type": "FeatureCollection", "features": []}),
            encoding="utf-8",
        )
        return
    frame.to_crs("EPSG:4326").to_file(output, driver="GeoJSON")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Validate and print the configured area without querying Overpass.",
    )
    parser.add_argument(
        "--confirm-boundary",
        action="store_true",
        help="Confirm the project owner has approved the configured extraction boundary.",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    cfg = load_config()
    validate_config(cfg)

    bbox = cfg["bbox"]
    bbox_tuple = (bbox["west"], bbox["south"], bbox["east"], bbox["north"])
    LOG.info("Configured bbox (west, south, east, north): %s", bbox_tuple)
    LOG.info("CRS: %s -> %s", cfg["coordinate_system"]["source_crs"],
             cfg["coordinate_system"]["projected_crs"])
    LOG.info("Local origin: %s", cfg["coordinate_system"]["local_origin"]["name"])

    if args.check_config:
        LOG.info("Configuration is valid. No network request was made.")
        return 0

    if not args.confirm_boundary or not cfg.get("owner_approved_for_extraction", False):
        raise SystemExit(
            "Extraction blocked: obtain the project owner's approval, set "
            "owner_approved_for_extraction=true in the config, and pass "
            "--confirm-boundary."
        )

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    ox.settings.timeout = int(cfg["overpass"]["timeout_seconds"])
    attempts = int(cfg["overpass"]["max_retries"])
    base_delay = int(cfg["overpass"]["retry_backoff_seconds"])
    ox.settings.max_query_area_size = 50_000_000

    LOG.info("OSMnx version: %s", ox.__version__)
    LOG.info("Downloading drivable road graph...")
    graph = with_retries(
        "road network",
        lambda: ox.graph.graph_from_bbox(
            bbox_tuple,
            network_type=cfg["features"]["roads_network_type"],
            simplify=True,
            retain_all=True,
        ),
        attempts,
        base_delay,
    )
    if graph.number_of_edges() == 0:
        raise RuntimeError("OSMnx returned a road graph with no edges")

    ox.io.save_graphml(graph, filepath=RAW_DIR / "roads.graphml")
    _, edges = ox.convert.graph_to_gdfs(graph)
    if edges.crs is None:
        raise ValueError("OSM road graph has no CRS")

    layers: dict[str, gpd.GeoDataFrame] = {"roads": edges}

    if cfg["features"].get("buildings", True):
        LOG.info("Downloading building footprints...")
        buildings = with_retries(
            "building footprints",
            lambda: ox.features.features_from_bbox(bbox_tuple, tags={"building": True}),
            attempts,
            base_delay,
        )
        buildings = clean_geometries(buildings)
        buildings = buildings[
            buildings.geometry.geom_type.isin(["Polygon", "MultiPolygon"])
        ].copy()
        layers["buildings"] = buildings

    extra_queries = {
        "parks": {"leisure": ["park", "garden"], "landuse": ["grass", "recreation_ground"]},
        "water": {"natural": ["water"], "waterway": ["riverbank", "river", "canal"]},
        "landmarks": {
            "historic": True,
            "tourism": ["attraction", "museum", "viewpoint"],
            "railway": "station",
        },
    }
    for layer_name, tags in extra_queries.items():
        if not cfg["features"].get(layer_name, False):
            continue
        LOG.info("Downloading %s...", layer_name)
        layer = with_retries(
            layer_name,
            lambda tags=tags: ox.features.features_from_bbox(bbox_tuple, tags=tags),
            attempts,
            base_delay,
        )
        layers[layer_name] = clean_geometries(layer)

    target_crs = cfg["coordinate_system"]["projected_crs"]
    bounds_geom = gpd.GeoSeries(
        [box(bbox["west"], bbox["south"], bbox["east"], bbox["north"])],
        crs=cfg["coordinate_system"]["source_crs"],
    ).to_crs(target_crs).iloc[0]

    # Project the configured origin once. The manifest is the source of truth
    # for all future geographic-to-game coordinate conversion.
    origin = cfg["coordinate_system"]["local_origin"]
    transformer = Transformer.from_crs(
        cfg["coordinate_system"]["source_crs"], target_crs, always_xy=True
    )
    origin_easting, origin_northing = transformer.transform(
        float(origin["longitude"]), float(origin["latitude"])
    )

    projected_gpkg = PROCESSED_DIR / "newcastle-projected.gpkg"
    if projected_gpkg.exists():
        projected_gpkg.unlink()

    counts: dict[str, int] = {}
    for layer_name, source_layer in layers.items():
        projected = source_layer.to_crs(target_crs)
        clipped = clean_geometries(projected.clip(bounds_geom))
        counts[layer_name] = len(clipped)

        if not clipped.empty:
            clipped.to_file(
                projected_gpkg,
                layer=layer_name,
                driver="GPKG",
                mode="w" if not projected_gpkg.exists() else "a",
            )

        write_geojson(clipped, PROCESSED_DIR / f"{layer_name}.geojson")
        LOG.info("%s: %s features", layer_name, counts[layer_name])

    retrieved_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "dataset": "TYNE CITY Newcastle core",
        "source": "© OpenStreetMap contributors",
        "source_url": "https://www.openstreetmap.org/copyright",
        "license": "ODbL-1.0",
        "retrieved_at": retrieved_at,
        "osmnx_version": ox.__version__,
        "source_crs": cfg["coordinate_system"]["source_crs"],
        "projected_crs": target_crs,
        "bbox": bbox,
        "counts": counts,
        "projected_geopackage": projected_gpkg.name if projected_gpkg.exists() else None,
        "geojson_outputs": [f"{name}.geojson" for name in counts],
        "local_origin": {
            "name": origin["name"],
            "latitude": float(origin["latitude"]),
            "longitude": float(origin["longitude"]),
            "easting": origin_easting,
            "northing": origin_northing,
        },
        "threejs_axes": cfg["coordinate_system"]["threejs_axes"],
        "scale": float(cfg["coordinate_system"].get("scale", 1.0)),
        "units": cfg["coordinate_system"]["units"],
        "notes": [
            "Building height inference and mesh generation are later pipeline stages.",
            "GeoJSON outputs use EPSG:4326; the GeoPackage stores clipped projected geometries.",
            "Estimated values must be distinguished from source OSM attributes.",
            "Derived OSM database content remains subject to ODbL obligations.",
        ],
    }
    (PROCESSED_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    LOG.info("Extraction complete: %s", PROCESSED_DIR / "manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
