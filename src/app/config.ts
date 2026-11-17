/** Central tuning values. Keep magic numbers out of game logic. */
export interface LoopConfig {
  /** Fixed simulation step in seconds. */
  readonly fixedStep: number;
  /** Largest frame delta accepted before clamping, in seconds. */
  readonly maxFrameDelta: number;
  /** Upper bound on fixed steps per rendered frame. */
  readonly maxSubSteps: number;
}

export interface RenderConfig {
  readonly fov: number;
  readonly near: number;
  readonly far: number;
  readonly maxPixelRatio: number;
  readonly shadows: boolean;
  readonly clearColour: number;
}

export interface TestSceneConfig {
  readonly groundSize: number;
  readonly gridDivisions: number;
  readonly blockCount: number;
  readonly seed: number;
}

export interface GameConfig {
  readonly loop: LoopConfig;
  readonly render: RenderConfig;
  readonly testScene: TestSceneConfig;
}

export const config: GameConfig = {
  loop: { fixedStep: 1 / 60, maxFrameDelta: 0.25, maxSubSteps: 5 },
  render: { fov: 60, near: 0.1, far: 2000, maxPixelRatio: 2, shadows: true, clearColour: 0xa9c4dc },
  testScene: { groundSize: 400, gridDivisions: 40, blockCount: 60, seed: 1928 },
};
