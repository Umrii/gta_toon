# Week 01 Progress Report

## Dates
Start: 17 November 2026
End:

## Weekly objective
Sprint 1: a clean Vite + TypeScript + Three.js project with a working 3D scene and documented workflow.

## Planned tasks
- [x] Create Vite vanilla TypeScript project
- [x] Install Three.js and TypeScript types
- [x] Configure strict TypeScript
- [x] Create the scene, perspective camera, renderer and lighting
- [x] Add ground plane, temporary buildings, grid/axes helpers
- [x] Add responsive resize handling (ResizeObserver)
- [x] Add a stable animation loop (fixed timestep, delta clamp, sub-step cap, pause on hidden tab)
- [x] Add basic error logging and an on-screen error state
- [x] Add Git repository and initial commit
- [x] Write setup instructions
- [x] Capture a screenshot of the scene
- [ ] Owner confirms the scene in their own browser

## Completed tasks
- Project scaffolded by hand (no interactive template) with Vite 8, TypeScript 7, Three.js r187 and Vitest 5.
- Placeholder scene with 60 seeded blocks, a road cross, shadows, fog and an animated origin marker.
- OrbitControls development camera (part of the `three` package, so no new dependency).
- Debug overlay showing FPS, draw calls and triangle count.

## Incomplete tasks
- ESLint/Prettier aren't set up yet. They're listed in Phase 0 but not in Sprint 1. Add them next week.
- No GitHub remote yet. This is waiting on the public/private decision.

## Tests and validation
- Build: `npm run build` passes (strict `tsc --noEmit` + Vite build).
- Unit tests: 4/4 pass (`tests/unit/GameLoop.test.ts`, fixed-timestep accounting).
- Browser test: checked in the Claude desktop browser pane (Chromium). The scene renders, the console has no errors, and the canvas resizes correctly at 1000×400 (no distortion). The first deprecation warning (`PCFSoftShadowMap`) is fixed.
- Manual playtest: orbit controls weren't exercised by hand. The owner should check this.

## Demonstration
Screenshot: `docs/assets/sprint-01.jpg`
Commit: Sprint 1 baseline

## Bugs and blockers
- `npm audit` reports a high-severity ReDoS advisory in `picomatch`, which comes in through Vite and Vitest. It's dev-time only and not in the shipped bundle. The suggested "fix" downgrades Vite, so it's not applied. Re-check when Vite updates.

## Technical decisions
- See `docs/decisions/0001-foundation-stack.md`.

## Time spent
Planned: 8–15 h (Phase 0)
Actual: ~1 h (estimate)

## Lessons learned
- Three.js r187 removed `PCFSoftShadowMap`, so use `PCFShadowMap`.

## Next week's objectives
1. Add ESLint + Prettier.
2. Agree the initial map boundary (polygon/bbox config file).
3. Set up the Python map pipeline environment (OSMnx, GeoPandas, Shapely, PyProj).

## Overall project status
In progress
