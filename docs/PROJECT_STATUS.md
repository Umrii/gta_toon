# Project Status

| Field | Value |
|---|---|
| Current release | Release 0: technical prototype |
| Current phase | Phase 1: geographic extraction |
| Current week | Week 02 (from 18 Nov 2026) |
| Completed milestones | Sprint 1 foundation committed as `55cb361`; Phase 1 extraction scaffolding committed |
| In progress | Owner confirmation of proposed map area; validate Python setup and extraction config |
| Blockers | Overpass extraction intentionally gated pending owner approval |
| Known critical bugs | None reported |
| Latest stable commit | See `git log` on `main` |
| Latest playable demo URL | Local development: http://localhost:5173 (not publicly deployed) |
| Total hours invested | Update from actual time tracking |
| Next milestone | Extract and validate roads, buildings, parks, water and landmark data |

## Current proposed map decision (not yet approved)

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

- [ ] Confirm proposed map boundary and that wider Gateshead can wait.
- [ ] Confirm real-world scale.
- [ ] Run the app and personally test orbit controls.
- [ ] Run `python scripts/map-pipeline/extract_osm.py --check-config`.
- [ ] After approving the boundary, enable extraction in config and run with `--confirm-boundary`.
