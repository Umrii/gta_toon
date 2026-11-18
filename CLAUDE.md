# TYNE CITY: working notes for Claude Code

- Read `TYNE_CITY_SPEC.md` before changes.
- Follow section 15 of the specification: small tasks, inspect before editing, explain assumptions, run build/tests, report actual validation, and do not claim tests that were not run.
- Stack: Vite + strict TypeScript + Three.js; tests use Vitest. Rapier is deferred until the player/physics phase.
- Keep tuning/configuration centralised. Avoid creating placeholder modules for distant phases.
- Always run `npm run build` and `npm test` after TypeScript changes.
- Python map tooling is under `scripts/map-pipeline/`; setup and commands are documented in that directory.
- The proposed map area and CRS are documented in `docs/decisions/0002-initial-map-area.md`. It is provisional until the owner confirms.
- OSM extraction requires an explicit `--confirm-boundary` flag and an approved config. Do not bypass this gate.
- Do not run large repeated Overpass queries or commit raw downloads.
- Retain source, retrieval date and licence metadata. Public OSM use requires attribution and ODbL compliance.
- Update `docs/PROJECT_STATUS.md` and the current weekly report when milestone status changes.
- Do not claim local browser verification unless the owner or a controlled browser test actually verifies it.

- The project owner approved the initial map area and true 1:1 scale on 18 Nov 2026. The config now enables extraction; still pass `--confirm-boundary` explicitly.
- For realistic environment work, follow `docs/BUILDING_REALISM_PLAN.md`: preserve OSM building/part tags, distinguish measured from estimated heights, investigate Environment Agency LiDAR DTM/DSM, and reserve bespoke Blender modelling for hero landmarks.
- Do not describe OSM footprint extrusion as photorealistic. Verify geometry and source provenance first, then build the highest-quality realistic slice that meets browser performance targets.
