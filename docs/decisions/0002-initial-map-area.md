# 0002: Initial map extraction boundary and geographic conventions

**Date:** 17 November 2026  
**Status:** Provisional implementation baseline

## Context

Phase 1 needs a small area for validating extraction, coordinate handling and feature quality. The first area should include core Newcastle landmarks and the Quayside approach without making the first Overpass query unnecessarily broad.

## Decision

- Use the configured bounding box in `data/configs/newcastle-core.json`.
- Include the Newcastle city-centre core: Monument/Grey Street, Haymarket, Central Station, Quayside and Tyne Bridge approach.
- Do not include the wider Gateshead riverside in the first extraction. Expand after the pipeline is validated.
- Preserve real-world metric scale.
- Use EPSG:27700 for metric geometry processing.
- Export GeoJSON in EPSG:4326.
- Use a local origin near Grey's Monument for later Three.js coordinates; calculate and record exact origin coordinates during processing.
- Three.js axes: X east, Y elevation, Z south.

## Rationale

A contained first extraction makes it easier to inspect geometry, tune road widths and verify alignment before adding more districts. Real-world scale preserves geographic authenticity and avoids conversion problems later.

## Consequences

- Initial map area is a coarse bounding box and must be inspected against extracted output.
- Gateshead expansion is deferred, not excluded from the long-term world.
- The runtime manifest must record exact CRS, origin, scale and axis convention.
- The source and ODbL attribution must be retained.

## Revisit when

- First roads/buildings render in Three.js.
- The map boundary proves too restrictive for a continuous driving route.
- Performance or geographic scope requires chunking.
