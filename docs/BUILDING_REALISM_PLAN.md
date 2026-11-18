# TYNE CITY: Building and Environment Realism Plan

**Status:** Approved technical direction  
**Date:** 18 November 2026

## Objective

Make the initial Newcastle core feel recognisably like the real city while keeping it feasible to render in a desktop browser. Do not equate realism with millions of polygons. Prioritise correct geography, building footprints, street proportions, elevation, silhouette, rooflines, materials, and distinctive landmarks.

## Important data limitation

OpenStreetMap primarily provides geographic features and tags. It does not provide complete photorealistic 3D building meshes or façade photographs. Some buildings have useful 3D tags; many do not. The game must distinguish source facts from estimated values.

## Recommended fidelity tiers

### Tier 1: Ordinary buildings

Use for the majority of buildings.

- Preserve the actual OSM footprint and polygon holes.
- Query both `building=*` and `building:part=*`.
- Preserve OSM element type/ID and all relevant available tags.
- Use `height` when valid.
- Otherwise derive a clearly labelled estimate from `building:levels` and configurable storey heights.
- Use LiDAR DSM/DTM-derived height evidence where available and quality checked.
- Respect `min_height`, `building:min_level`, `roof:shape`, `roof:height`, `roof:levels`, `roof:angle`, `roof:orientation`, `roof:material`, `roof:colour`, `building:material`, and `building:colour`.
- Create roof geometry for common shapes when data supports it.
- Generate façade floor bands, window bays, doors, and shopfront zones procedurally.
- Vary windows/materials by building category and location, not randomly per frame.
- Keep geometry and materials instanced/merged where practical.
- Avoid a city of identical rectangular boxes.

### Tier 2: Streetscape buildings

Prioritise important visible corridors and street walls:

- Grey Street and surrounding historic terraces.
- Northumberland Street.
- Monument / Grainger Town area.
- Central Station approaches.
- Quayside.

For these corridors, improve the façade composition with verified reference material and targeted Blender models or façade modules. Maintain a source/rights record for every photograph, texture, and model. Use original project photography or assets with an explicit licence permitting the intended use.

### Tier 3: Hero landmarks

Create bespoke Blender models for a small number of high-recognition landmarks:

1. Tyne Bridge, including its distinctive arches and structural profile.
2. Grey's Monument.
3. Newcastle Central Station frontage and roof silhouette.
4. Selected Grainger Town / Grey Street façades.
5. Distinctive Quayside buildings chosen after reference inspection.

Use measured or well-documented approximate dimensions, geographic placement, and original or appropriately licensed textures. These models should receive more geometry and texture budget than ordinary buildings.

## Elevation and building massing data

The Environment Agency publishes 1 m LiDAR Composite Digital Terrain Model (DTM) and Digital Surface Model (DSM) datasets for England under the Open Government Licence, subject to their attribution requirements.

- DTM represents bare-earth terrain and should drive the ground/elevation surface.
- DSM includes surfaces such as buildings and vegetation.
- The difference between DSM and DTM can provide candidate above-ground height evidence, but it is not automatically a building-height dataset. Vegetation, moving objects, survey age, and classification errors must be considered.
- The composite uses surveys collected between 2000 and 2022. Record source survey/date metadata when available.
- Verify coverage, tile boundaries, vertical reference, file size, and the applicable licence before downloading.
- Use British National Grid (EPSG:27700) consistently. Confirm vertical datum/units before combining with other elevation data.
- Do not infer exact façade geometry from LiDAR rasters.

Potential official dataset records:
- DTM: https://environment.data.gov.uk/dataset/13787b9a-26a4-4775-8523-806d13af58fc
- DSM: https://environment.data.gov.uk/dataset/9ba4d5ac-d596-445a-9056-dae3ddec0178

Attribution must include © Environment Agency copyright and/or database right 2022, as required by the dataset record. Confirm current licence terms when acquiring the data.

## Extraction requirements

Extend the Phase 1 extraction and QA to include:

- Driving road network.
- Walking network / footways for future pedestrian navigation.
- Building footprints and building parts.
- Parks, gardens, grass and recreation grounds.
- Water polygons and river/waterway geometries.
- Bridge, tunnel, layer, lanes, width, surface, oneway, maxspeed and road-class tags where available.
- POI/landmark candidates with names and categories.
- All useful 3D building tags listed above.
- Counts for how many buildings have explicit height, levels, roof tags, material/colour tags and building parts.

Preserve OSM identifiers and distinguish nodes, ways and relations. Do not discard source tags just because the first renderer does not use them.

## Building height policy

Store both the value and its provenance.

Recommended metadata fields in processed building records:

- `height_m`
- `height_source`: `osm_height`, `osm_levels_estimate`, `lidar_estimate`, or `fallback_estimate`
- `height_confidence`: e.g. `high`, `medium`, `low`
- `levels`
- `roof_shape`
- `roof_height_m`
- `facade_material`
- `facade_colour`
- `roof_material`
- `roof_colour`
- `osm_element_type`
- `osm_id`

Do not overwrite source OSM values with inferred values. Keep source and derived attributes separate.

## Visual implementation sequence

1. Build a 2D/debug map inspection view showing roads, building footprints, water, parks, and landmarks.
2. Verify map orientation, scale, clipping, geometry validity and coverage.
3. Generate terrain from the best validated DTM source.
4. Generate building massing from footprints and the best available height values.
5. Add roof shapes and building parts.
6. Add procedural façade modules and street-level shopfronts.
7. Model the hero landmarks.
8. Add road markings, pavements, trees, lighting and street furniture.
9. Add material/lighting tuning and LODs.
10. Compare the result against appropriately sourced real-world reference photos and fix the biggest visual mismatches.

## Browser performance principles

- Use instancing for repeated windows, streetlights, trees and props.
- Merge static geometry by chunk/material where useful.
- Use separate simplified collision geometry.
- Generate LODs for buildings.
- Load map chunks around the player, not the entire expanded city.
- Use texture atlases and compressed textures where appropriate.
- Avoid a unique draw call for every window or small prop.
- Profile draw calls, triangles, memory, GPU frame time and loading time.
- Keep high-detail hero assets close to their actual scale and location.

## Non-goals and restrictions

- Do not use scraped Google Street View/Google Earth imagery or extracted commercial-game assets.
- Do not claim the whole city is photogrammetric or photorealistic when it is procedurally reconstructed.
- Do not fabricate source accuracy. Mark estimated building heights and generated details.
- Do not build detailed interiors for ordinary buildings in the initial release.
- Do not start broad hand-modelling before the GIS extraction and inspection proves which blocks need it.

## Acceptance criteria for the first realistic map slice

- Road network and building footprints align in real-world coordinates.
- The Tyne Bridge crossing is represented in the correct place and orientation.
- Building height coverage and fallback estimates are reported.
- The tallest/most distinctive buildings have plausible silhouettes.
- Terrain elevation is based on a validated source or explicitly labelled as placeholder.
- The central area has no obvious missing blocks, giant gaps, or duplicated buildings.
- The map renders in Three.js with a documented performance baseline.
