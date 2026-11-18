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
