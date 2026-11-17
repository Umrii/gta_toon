import { describe, expect, it } from 'vitest';
import { advanceAccumulator } from '../../src/core/GameLoop';
import type { LoopConfig } from '../../src/app/config';

const cfg: LoopConfig = { fixedStep: 1 / 60, maxFrameDelta: 0.25, maxSubSteps: 5 };

describe('advanceAccumulator', () => {
  it('runs one step for a 60 Hz frame', () => {
    const r = advanceAccumulator(0, 1 / 60 + 1e-9, cfg);
    expect(r.steps).toBe(1);
    expect(r.accumulator).toBeCloseTo(0, 6);
  });

  it('carries leftover time between frames', () => {
    const first = advanceAccumulator(0, 0.01, cfg);
    expect(first.steps).toBe(0);
    const second = advanceAccumulator(first.accumulator, 0.01, cfg);
    expect(second.steps).toBe(1);
    expect(second.alpha).toBeGreaterThan(0);
    expect(second.alpha).toBeLessThan(1);
  });

  it('caps sub-steps and drops backlog after a long stall', () => {
    const r = advanceAccumulator(0, 10, cfg);
    expect(r.steps).toBe(cfg.maxSubSteps);
    expect(r.accumulator).toBe(0);
  });

  it('ignores negative deltas', () => {
    const r = advanceAccumulator(0, -1, cfg);
    expect(r.steps).toBe(0);
    expect(r.accumulator).toBe(0);
  });
});
