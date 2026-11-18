# Week 02 Progress Report

## Dates
Start: 17 November 2026
End:

## Weekly objective
Phase 1: establish a reproducible, version-correct OpenStreetMap extraction pipeline for the approved initial Newcastle core.

## Planned tasks
- [ ] Confirm owner sign-off for the initial bbox, Gateshead exclusion and true-scale decision.
- [ ] Create Python virtual environment and install pinned-compatible geospatial dependencies.
- [ ] Run the extraction script once against Overpass.
- [ ] Validate the road graph and feature outputs.
- [ ] Record counts, CRS, retrieval timestamp and source attribution in the manifest.
- [ ] Inspect outputs for coverage, geometry validity and obvious missing areas.
- [ ] Keep raw downloads out of Git and review processed output sizes.

## Completed tasks
- Phase 1 pipeline scaffolding added to the repository.
- Initial map boundary and coordinate convention documented provisionally.

## Incomplete tasks
- Extraction and actual output validation remain to be performed locally.

## Tests and validation
- Script syntax/static validation:
- Extraction:
- GeoJSON validation:
- Visual inspection:

## Demonstration
Screenshot/video:
Commit:

## Bugs and blockers
- Overpass availability/rate limits may delay extraction.

## Technical decisions
- See `docs/decisions/0002-initial-map-area.md`.

## Time spent
Planned:
Actual:

## Lessons learned

## Next week's objectives
1. Validate actual extracted data.
2. Build a map inspection/debug view.
3. Start generating simple road surfaces and building footprints.

## Overall project status
In progress
