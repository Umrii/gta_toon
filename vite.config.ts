import { defineConfig } from 'vitest/config';

export default defineConfig({
  server: { port: 5173, strictPort: true },
  // Three.js alone is ~560 kB minified; revisit with code-splitting in Phase 5.
  build: { target: 'es2022', sourcemap: true, chunkSizeWarningLimit: 700 },
  test: { include: ['tests/**/*.test.ts'], environment: 'node' },
});
