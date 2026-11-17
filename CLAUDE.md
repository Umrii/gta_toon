# TYNE CITY: working notes for Claude Code

- The full specification is `TYNE_CITY_SPEC.md`. Section 15 sets the working rules and section 15.2 sets the report format.
- The `CLAUDE.md` in the parent folder (`D:\Downloads`) is about an unrelated business plan. Ignore it for this project.
- Stack: Vite + strict TypeScript + Three.js; tests use Vitest. Rapier is added in Phase 3, not before.
- Always run `npm run build` and `npm test` after changes. Check the browser with the `dev` launch config (`.claude/launch.json`).
- Keep tuning values in `src/app/config.ts`. Don't hard-code them in systems.
- Update `docs/PROJECT_STATUS.md` and the current weekly report when a milestone moves.
