# TYNE CITY

A browser-based, single-player open-world 3D game set in a recreation of Newcastle upon Tyne.
Original IP, built with Three.js and TypeScript. The full specification is in
[TYNE_CITY_SPEC.md](TYNE_CITY_SPEC.md).

**Current state:** Sprint 1 (project foundation). A placeholder test scene renders in the browser.
Real Newcastle map data arrives in Phase 1 and Phase 2.

## Requirements

- Node.js 20.19+ or 22.12+ (developed on Node 24.18, npm 12.0)
- A current Chrome or Edge browser

## Setup

```bash
npm install
```

## Commands

| Command             | What it does                                            |
| ------------------- | ------------------------------------------------------- |
| `npm run dev`       | Start the Vite dev server at http://localhost:5173      |
| `npm run build`     | Type-check with strict TypeScript, then build to `dist/` |
| `npm run preview`   | Serve the production build locally                      |
| `npm run test`      | Run unit tests once (Vitest)                            |
| `npm run typecheck` | Type-check only                                         |

## Controls (Sprint 1 development camera)

- Left-drag: orbit
- Right-drag: pan
- Mouse wheel: zoom

The overlay at the top left shows FPS, draw calls and triangle count.

## Project layout

```text
src/
  app/config.ts          Central tuning values (loop, rendering, test scene)
  core/GameLoop.ts       Fixed-timestep loop with delta clamping and pause
  core/Logger.ts         Console logging and global error capture
  rendering/Renderer.ts  WebGL renderer, camera and resize handling
  world/TestScene.ts     Placeholder environment (replaced in Phase 2)
  world/random.ts        Deterministic PRNG
  main.ts                Bootstrap and teardown
tests/unit/              Vitest unit tests
docs/                    Status, weekly reports, decision records
```

## Licensing and attribution

All code and content are original. Future map data will come from OpenStreetMap
(© OpenStreetMap contributors, ODbL) and will be credited in the game.
