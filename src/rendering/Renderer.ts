import * as THREE from 'three';
import type { RenderConfig } from '../app/config';

/** Owns the WebGL renderer and main camera, and keeps both in sync with the container size. */
export class Renderer {
  readonly webgl: THREE.WebGLRenderer;
  readonly camera: THREE.PerspectiveCamera;
  private readonly observer: ResizeObserver;

  constructor(private readonly container: HTMLElement, cfg: RenderConfig) {
    this.webgl = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    this.webgl.setPixelRatio(Math.min(window.devicePixelRatio, cfg.maxPixelRatio));
    this.webgl.setClearColor(cfg.clearColour);
    this.webgl.outputColorSpace = THREE.SRGBColorSpace;
    this.webgl.toneMapping = THREE.ACESFilmicToneMapping;
    this.webgl.shadowMap.enabled = cfg.shadows;
    this.webgl.shadowMap.type = THREE.PCFShadowMap;
    container.appendChild(this.webgl.domElement);

    this.camera = new THREE.PerspectiveCamera(cfg.fov, 1, cfg.near, cfg.far);

    this.observer = new ResizeObserver(() => this.resize());
    this.observer.observe(container);
    this.resize();
  }

  resize(): void {
    const width = Math.max(1, this.container.clientWidth);
    const height = Math.max(1, this.container.clientHeight);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.webgl.setSize(width, height, false);
  }

  render(scene: THREE.Scene): void {
    this.webgl.render(scene, this.camera);
  }

  dispose(): void {
    this.observer.disconnect();
    this.webgl.dispose();
    this.webgl.domElement.remove();
  }
}
