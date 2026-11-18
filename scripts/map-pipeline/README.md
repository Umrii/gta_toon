# TYNE CITY map pipeline

## Initial area

The initial extraction uses `data/configs/newcastle-core.json`. It covers the central Newcastle core around Monument, Haymarket, Central Station, the Quayside and the Tyne Bridge approach. The first pass intentionally does not include the Gateshead riverside.

The configured bounds are a coarse extraction envelope, not a final playable polygon. Inspect the outputs and refine the area before large expansions.

## Setup (Windows PowerShell)

From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r scripts/map-pipeline/requirements.txt
python scripts/map-pipeline/extract_osm.py
```

On macOS/Linux, activate with:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r scripts/map-pipeline/requirements.txt
python scripts/map-pipeline/extract_osm.py
```

## Outputs

Raw graph data is stored under `data/raw/osm/` (gitignored). Processed data is stored under `data/processed/osm/`:

- `roads.geojson`
- `buildings.geojson`
- `parks.geojson`
- `water.geojson`
- `manifest.json`

Do not commit raw downloads or unexpectedly large generated datasets without reviewing file size and licensing implications.

## Data conventions

- Input bbox: west, south, east, north in EPSG:4326.
- Projected processing CRS: EPSG:27700 (British National Grid).
- GeoJSON output CRS: EPSG:4326, as required by the GeoJSON convention.
- Future game-local coordinates: X=east, Y=elevation, Z=south.
- Coordinate origin must be selected once and written to the generated runtime manifest before Three.js geometry conversion.

## Reliability

The script retries transient Overpass failures with bounded exponential backoff. Do not run repeated high-volume queries in parallel. If Overpass is unavailable, wait and retry later.

## Attribution and licensing

Source: © OpenStreetMap contributors, licensed under the Open Database License (ODbL). See https://www.openstreetmap.org/copyright.

Review ODbL obligations before publishing derived databases or generated map assets. Keep source, retrieval date, licence and processing metadata with the dataset.
