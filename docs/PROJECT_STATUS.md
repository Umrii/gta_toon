# Project Status

| Field | Value |
|---|---|
| Current release | Release 0: technical prototype |
| Current phase | Phase 1: geographic extraction |
| Current week | Week 02 (from 18 Nov 2026) |
| Completed milestones | Sprint 1 foundation committed as `55cb361`; Phase 1 extraction scaffolding committed |
| In progress | Python environment setup and first OSM extraction |
| Blockers | Python environment and actual OSM extraction still need local validation |
| Known critical bugs | None reported |
| Latest stable commit | See `git log` on `main` |
| Latest playable demo URL | Local development: http://localhost:5173 (not publicly deployed) |
| Total hours invested | Update from actual time tracking |
| Next milestone | Extract and validate roads, buildings, parks, water and landmark data |

## Approved initial map decision (18 November 2026)

- Initial area: central Newcastle around Monument/Grey Street, Haymarket, Central Station, Quayside and the Tyne Bridge crossing/approach.
- Wider Gateshead: deferred from the first pass; the bridge's south landing may fall inside the extraction envelope.
- Scale: real-world metric scale (1.0).
- Processing CRS: EPSG:27700.
- GeoJSON export CRS: EPSG:4326.
- Projected processing output: GeoPackage in EPSG:27700.
- Three.js axes: X east, Y elevation, Z south.
- Local origin: Grey's Monument; exact EPSG:27700 coordinates are calculated and written to the manifest.

See `docs/decisions/0002-initial-map-area.md`.

## Owner checks

- [x] Confirm proposed map boundary and defer wider Gateshead; include full Tyne Bridge crossing.
- [x] Confirm real-world scale (1.0).
- [ ] Run the app and personally test orbit controls.
- [ ] Run `python scripts/map-pipeline/extract_osm.py --check-config`.
- [ ] Run extraction with `python scripts/map-pipeline/extract_osm.py --confirm-boundary`.
