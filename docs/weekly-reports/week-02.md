# Week 02 Progress Report

## Dates
Start: 18 November 2026
End:

## Weekly objective
Phase 1: establish a reproducible, version-correct OpenStreetMap extraction pipeline for the proposed initial Newcastle core.

## Planned tasks
- [ ] Owner confirms the provisional bbox, limited Tyne Bridge south landing, wider Gateshead deferral, and real-world scale.
- [x] Add a configurable initial map boundary.
- [x] Add Python extraction dependencies and reproducible setup instructions.
- [x] Add an OSMnx 2.x extraction script for roads, buildings, parks, water and landmark candidates.
- [x] Add bounded retries and a no-network configuration validation mode.
- [x] Add explicit owner-approval gate before Overpass extraction.
- [x] Record CRS, axis convention, local origin and source provenance in the generated manifest.
- [x] Ignore local virtual environments and generated map downloads/outputs.
- [ ] Create Python virtual environment and install dependencies locally.
- [ ] Run `--check-config` and confirm validation.
- [ ] After approval, run extraction once against Overpass.
- [ ] Validate GeoJSON/GeoPackage outputs, feature counts and geometry quality.
- [ ] Inspect outputs for map coverage and obvious gaps.

## Completed tasks
- Added `data/configs/newcastle-core.json` with the proposed central Newcastle area.
- Added `scripts/map-pipeline/extract_osm.py` using OSMnx 2.x API conventions.
- Added `scripts/map-pipeline/requirements.txt` and pipeline setup documentation.
- Added provisional map/CRS decision record.
- Updated project status and Claude Code instructions.
- Script supports a no-network config check and blocks extraction until explicit owner approval.

## Incomplete tasks
- No OSM network extraction has been run.
- No local Python environment or generated map files have been verified.
- The proposed boundary and true-scale default still need owner confirmation.

## Tests and validation
- Config/script review: source reviewed in GitHub.
- Python syntax check: not run in this environment.
- Config validation: not run locally.
- Overpass extraction: not run.
- GeoJSON/GeoPackage validation: not run.
- Visual inspection: pending.

## Demonstration
Screenshot/video: none yet for Phase 1.
Commits: see recent `main` history.

## Bugs and blockers
- Owner approval is required before making Overpass requests.
- Overpass may rate-limit or temporarily reject large queries; the script uses bounded retries.

## Technical decisions
- See `docs/decisions/0002-initial-map-area.md`.
- Local origin is Grey's Monument (configured in WGS84 and transformed to EPSG:27700 by the script).
- EPSG:27700 is used for metric processing; GeoJSON outputs remain EPSG:4326 and a projected GeoPackage is also generated.

## Time spent
Planned:
Actual: Not measured.

## Lessons learned
- OSMnx 2.x uses bbox order `(left, bottom, right, top)`.
- The proposed area is provisional; configuration validation should be possible without network access.

## Next week's objectives
1. Confirm boundary and run the first extraction.
2. Review feature counts and output geometry.
3. Build a map inspection/debug view.
4. Begin generating simple road surfaces and building footprints.

## Overall project status
In progress
