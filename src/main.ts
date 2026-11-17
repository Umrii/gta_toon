import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { config } from './app/config';
import { GameLoop } from './core/GameLoop';
import { Logger, installGlobalErrorHandlers } from './core/Logger';
import { Renderer } from './rendering/Renderer';
import { TestScene } from './world/TestScene';

function requireElement(id: string): HTMLElement {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Missing #${id} element in index.html`);
  return el;
}

function showError(message: string): void {
  const el = document.getElementById('error');
  if (!el) return;
  el.textContent = `Something went wrong while running TYNE CITY.\n\n${message}\n\nCheck the browser console for details.`;
  el.hidden = false;
}

function bootstrap(): () => void {
  const removeErrorHandlers = installGlobalErrorHandlers(showError);
  const container = requireElement('app');
  const debugEl = requireElement('debug');

  const renderer = new Renderer(container, config.render);
  renderer.camera.position.set(90, 70, 110);

  const world = new TestScene(config.testScene, config.render.shadows);

  // Development camera only; replaced by the third-person camera in Phase 3.
  const controls = new OrbitControls(renderer.camera, renderer.webgl.domElement);
  controls.target.set(0, 5, 0);
  controls.enableDamping = true;
  controls.maxPolarAngle = Math.PI / 2 - 0.05;
  controls.update();

  let fpsFrames = 0;
  let fpsTime = 0;
  const loop: GameLoop = new GameLoop(config.loop, {
    fixedUpdate: (dt) => world.fixedUpdate(dt),
    render: (frameDelta) => {
      controls.update();
      renderer.render(world.scene);
      fpsFrames++;
      fpsTime += frameDelta;
      if (fpsTime >= 0.5) {
        const info = renderer.webgl.info.render;
        debugEl.textContent = `${Math.round(fpsFrames / fpsTime)} fps | ${info.calls} draw calls | ${info.triangles} tris`;
        fpsFrames = 0;
        fpsTime = 0;
      }
    },
  });

  const onVisibility = (): void => loop.setPaused(document.hidden);
  document.addEventListener('visibilitychange', onVisibility);

  loop.start();
  requireElement('loading').hidden = true;
  Logger.info('Sprint 1 test scene running');

  return () => {
    loop.stop();
    document.removeEventListener('visibilitychange', onVisibility);
    controls.dispose();
    world.dispose();
    renderer.dispose();
    removeErrorHandlers();
  };
}

try {
  const teardown = bootstrap();
  import.meta.hot?.dispose(teardown);
} catch (err) {
  Logger.error('Failed to start', err);
  showError(err instanceof Error ? err.message : String(err));
}
