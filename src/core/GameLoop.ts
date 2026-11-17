import type { LoopConfig } from '../app/config';

export interface StepResult {
  /** Number of fixed updates to run this frame. */
  readonly steps: number;
  /** Leftover time carried into the next frame, in seconds. */
  readonly accumulator: number;
  /** Interpolation factor (0..1) for rendering between fixed states. */
  readonly alpha: number;
}

/**
 * Pure fixed-timestep accounting. Clamps large deltas (tab switches, breakpoints)
 * and caps sub-steps so a slow frame can never trigger an unbounded catch-up loop.
 */
export function advanceAccumulator(accumulator: number, frameDelta: number, cfg: LoopConfig): StepResult {
  const delta = Math.min(Math.max(frameDelta, 0), cfg.maxFrameDelta);
  let acc = accumulator + delta;
  let steps = Math.floor(acc / cfg.fixedStep);
  if (steps > cfg.maxSubSteps) {
    steps = cfg.maxSubSteps;
    acc = 0; // drop the backlog rather than spiralling
  } else {
    acc -= steps * cfg.fixedStep;
  }
  return { steps, accumulator: acc, alpha: acc / cfg.fixedStep };
}

export interface LoopCallbacks {
  /** Fixed-rate simulation update (physics, gameplay). */
  fixedUpdate(dt: number): void;
  /** Per-frame visual update and render. */
  render(frameDelta: number, alpha: number): void;
}

export class GameLoop {
  private rafId: number | null = null;
  private lastTime = 0;
  private accumulator = 0;
  private paused = false;

  constructor(private readonly cfg: LoopConfig, private readonly callbacks: LoopCallbacks) {}

  start(): void {
    if (this.rafId !== null) return;
    this.lastTime = performance.now();
    this.rafId = requestAnimationFrame(this.tick);
  }

  stop(): void {
    if (this.rafId !== null) cancelAnimationFrame(this.rafId);
    this.rafId = null;
  }

  setPaused(paused: boolean): void {
    this.paused = paused;
    // Reset timing so resuming does not inject a huge delta.
    this.lastTime = performance.now();
    this.accumulator = 0;
  }

  get isPaused(): boolean {
    return this.paused;
  }

  private readonly tick = (now: number): void => {
    this.rafId = requestAnimationFrame(this.tick);
    const frameDelta = (now - this.lastTime) / 1000;
    this.lastTime = now;

    if (this.paused) {
      this.callbacks.render(0, 0);
      return;
    }

    const result = advanceAccumulator(this.accumulator, frameDelta, this.cfg);
    this.accumulator = result.accumulator;
    for (let i = 0; i < result.steps; i++) this.callbacks.fixedUpdate(this.cfg.fixedStep);
    this.callbacks.render(Math.min(frameDelta, this.cfg.maxFrameDelta), result.alpha);
  };
}
