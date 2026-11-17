# 0001: Foundation stack and game loop

**Date:** 17 November 2026

## Context
Sprint 1 needs a browser 3D baseline that later phases (physics, map data, vehicles) can build on without rework.

## Decision
- Vite 8 + TypeScript 7 (strict, plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`) + Three.js r187.
- Vitest for unit tests, configured through `vite.config.ts`.
- `GameLoop` uses a fixed timestep (1/60 s). Frame deltas are clamped at 0.25 s and capped at 5 sub-steps per frame, and any excess backlog is dropped. The accounting is a pure function (`advanceAccumulator`) so it can be unit-tested.
- The loop pauses when the tab is hidden and resets its timing on resume, so returning to the tab never triggers a burst of catch-up steps.
- All tuning lives in `src/app/config.ts`.

## Alternatives considered
- Babylon.js or PlayCanvas: more batteries included, but the spec chose Three.js for direct control.
- A variable timestep: simpler, but unstable once Rapier is added.

## Trade-offs
- TypeScript 7 is new. If tooling incompatibilities appear, pin it to 5.x.
- The Three.js bundle is ~560 kB minified, so the chunk warning limit is raised to 700 kB until code-splitting in Phase 5.

## Consequences
- Physics in Phase 3 plugs into `fixedUpdate`, and rendering and camera work stay in `render`.
