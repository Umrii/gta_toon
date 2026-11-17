import * as THREE from 'three';
import type { TestSceneConfig } from '../app/config';
import { createRandom } from './random';

/**
 * Sprint 1 placeholder environment: ground, debug grid, a road cross and
 * deterministic placeholder blocks. Replaced by OSM-derived geometry in Phase 2.
 */
export class TestScene {
  readonly scene = new THREE.Scene();
  private readonly disposables: { dispose(): void }[] = [];
  private readonly spinner: THREE.Mesh;

  constructor(cfg: TestSceneConfig, shadows: boolean) {
    this.scene.fog = new THREE.Fog(0xa9c4dc, 150, 600);

    // Lighting
    const hemi = new THREE.HemisphereLight(0xdfe9f3, 0x4a4a3a, 0.9);
    const sun = new THREE.DirectionalLight(0xfff1dc, 2.2);
    sun.position.set(120, 180, 80);
    sun.castShadow = shadows;
    sun.shadow.mapSize.set(2048, 2048);
    const s = cfg.groundSize / 2;
    const shadowCam = sun.shadow.camera;
    shadowCam.left = -s;
    shadowCam.right = s;
    shadowCam.top = s;
    shadowCam.bottom = -s;
    shadowCam.near = 1;
    shadowCam.far = 600;
    this.scene.add(hemi, sun);

    // Ground
    const groundGeo = this.track(new THREE.PlaneGeometry(cfg.groundSize, cfg.groundSize));
    const groundMat = this.track(new THREE.MeshStandardMaterial({ color: 0x5b6b4f, roughness: 1 }));
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    this.scene.add(ground);

    // Debug grid, slightly raised to avoid z-fighting with the ground
    const grid = new THREE.GridHelper(cfg.groundSize, cfg.gridDivisions, 0x222222, 0x3d3d3d);
    grid.position.y = 0.02;
    this.track(grid.geometry);
    this.track(grid.material as THREE.Material);
    this.scene.add(grid);

    // Two placeholder roads crossing at the origin
    const roadMat = this.track(new THREE.MeshStandardMaterial({ color: 0x2b2b2e, roughness: 0.9 }));
    const roadGeo = this.track(new THREE.PlaneGeometry(cfg.groundSize, 12));
    for (const angle of [0, Math.PI / 2]) {
      const road = new THREE.Mesh(roadGeo, roadMat);
      road.rotation.set(-Math.PI / 2, 0, angle);
      road.position.y = 0.04;
      road.receiveShadow = true;
      this.scene.add(road);
    }

    // Placeholder buildings: one shared unit box, scaled per mesh.
    const boxGeo = this.track(new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0));
    const palette = [0x8c7b6b, 0xa39181, 0x6e6259, 0xb7a99a, 0x7d8591].map((c) =>
      this.track(new THREE.MeshStandardMaterial({ color: c, roughness: 0.85 })),
    );
    const rand = createRandom(cfg.seed);
    const half = cfg.groundSize / 2 - 20;
    let placed = 0;
    for (let attempt = 0; placed < cfg.blockCount && attempt < cfg.blockCount * 10; attempt++) {
      const x = (rand() * 2 - 1) * half;
      const z = (rand() * 2 - 1) * half;
      if (Math.abs(x) < 20 || Math.abs(z) < 20) continue; // keep the road cross clear
      const material = palette[Math.floor(rand() * palette.length) % palette.length];
      if (!material) continue;
      const block = new THREE.Mesh(boxGeo, material);
      block.scale.set(8 + rand() * 18, 6 + rand() * 40, 8 + rand() * 18);
      block.position.set(x, 0, z);
      block.castShadow = true;
      block.receiveShadow = true;
      this.scene.add(block);
      placed++;
    }

    // Origin marker: makes the fixed-step update visibly alive.
    const markerGeo = this.track(new THREE.TorusKnotGeometry(2, 0.6, 96, 12));
    const markerMat = this.track(new THREE.MeshStandardMaterial({ color: 0x7fb3d5, metalness: 0.3, roughness: 0.4 }));
    this.spinner = new THREE.Mesh(markerGeo, markerMat);
    this.spinner.position.set(0, 5, 0);
    this.spinner.castShadow = true;
    const axes = new THREE.AxesHelper(10);
    axes.position.y = 0.06;
    this.track(axes);
    this.scene.add(this.spinner, axes);
  }

  fixedUpdate(dt: number): void {
    this.spinner.rotation.y += dt * 0.8;
  }

  dispose(): void {
    for (const d of this.disposables) d.dispose();
    this.disposables.length = 0;
  }

  private track<T extends { dispose(): void }>(resource: T): T {
    this.disposables.push(resource);
    return resource;
  }
}
