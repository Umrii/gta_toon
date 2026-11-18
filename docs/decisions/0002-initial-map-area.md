# 0002: Initial map extraction boundary and geographic conventions

**Date:** 18 November 2026  
**Status:** Approved by project owner on 18 November 2026

## Context

Phase 1 needs a small area for validating extraction, coordinate handling and feature quality. The first area should include core Newcastle landmarks and the Quayside/Tyne Bridge approach without making the first Overpass query unnecessarily broad.

## Proposed decision

- Use the configured bounding box in `data/configs/newcastle-core.json`.
- Include the Newcastle city-centre core: Monument/Grey Street, Haymarket, Central Station, Quayside and the Tyne Bridge crossing/approach.
- Do not attempt to model wider Gateshead in the first pass. The bridge's south landing may be inside the coarse extraction envelope.
- Preserve real-world metric scale (scale factor 1.0).
- Use EPSG:27700 for metric geometry processing.
- Export GeoJSON in EPSG:4326 and a projected GeoPackage in EPSG:27700.
- Use Grey's Monument as the local origin; its configured latitude/longitude is transformed and recorded in the generated manifest.
- Three.js axes: X east, Y elevation, Z south.

## Rationale

A contained first extraction makes it easier to inspect geometry, tune road widths and verify alignment before adding more districts. Real-world scale preserves geographic authenticity and avoids conversion problems later.

## Approval gate

This proposal has not yet been approved by the project owner. The extraction script validates configuration without network access, but blocks Overpass queries unless:
1. The owner confirms this proposed area and scale.
2. `owner_approved_for_extraction` is set to `true`.
3. The script is run with `--confirm-boundary`.

## Consequences

- Initial map area is a coarse bounding box and must be inspected against extracted output.
- Wider Gateshead expansion is deferred, not excluded from the long-term world.
- The runtime manifest is the source of truth for CRS, local origin, scale and axis convention.
- The source and ODbL attribution must be retained.

## Revisit when

- First roads/buildings render in Three.js.
- The map boundary proves too restrictive for a continuous driving route.
- Performance or geographic scope requires chunking.
