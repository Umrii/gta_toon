# TYNE CITY map pipeline

## Initial area (provisional)

The initial extraction uses `data/configs/newcastle-core.json`. It is designed around central Newcastle, including Monument/Grey Street, Haymarket, Central Station, the Quayside and the Tyne Bridge crossing/approach. It does not attempt to model wider Gateshead in the first pass, although the bridge's south landing may fall inside the extraction envelope.

**The area is provisional.** The script will not query Overpass until the owner sets `owner_approved_for_extraction` to `true` and explicitly passes `--confirm-boundary`.

The configured bounds are a coarse extraction envelope, not a final playable polygon. Inspect outputs and refine the area before large expansions.

## Setup (Windows PowerShell)

From the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r scripts/map-pipeline/requirements.txt
python scripts/map-pipeline/extract_osm.py --check-config
```

After the owner approves the boundary and the config flag is set to true:

```powershell
python scripts/map-pipeline/extract_osm.py --confirm-boundary
```

On macOS/Linux, use `python3` to create the virtual environment and `source .venv/bin/activate` to activate it. The remaining commands are the same.

## Outputs

Raw road graph data is stored under `data/raw/osm/` (gitignored). Processed data is stored under `data/processed/osm/`:

- `roads.geojson`
- `buildings.geojson`
- `parks.geojson`
- `water.geojson`
- `landmarks.geojson`
- `newcastle-projected.gpkg` (projected geometries; absent if every layer is empty)
- `manifest.json`

Do not commit raw downloads or unexpectedly large generated datasets without reviewing file size and licensing implications.

## Data conventions

- Input bbox: west, south, east, north in EPSG:4326.
- Projected processing CRS: EPSG:27700 (British National Grid).
- GeoJSON outputs: EPSG:4326.
- GeoPackage: clipped geometry in EPSG:27700.
- Local origin: Grey's Monument, configured by latitude/longitude and transformed into EPSG:27700 in the manifest.
- Future game-local coordinates: X=east, Y=elevation, Z=south.
- Units: metres; scale: 1.0 (real-world scale).

## Reliability

The script validates the configuration without making a network request when called with `--check-config`. It retries extraction failures with bounded exponential backoff. Do not run repeated high-volume queries in parallel. If Overpass is unavailable, wait and retry later.

## Attribution and licensing

Source: © OpenStreetMap contributors, licensed under the Open Database License (ODbL). See https://www.openstreetmap.org/copyright.

Review ODbL obligations before publishing derived databases or generated map assets. Keep source, retrieval date, licence and processing metadata with the dataset.
