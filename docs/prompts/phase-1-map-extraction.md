# Claude Code Task: Phase 1 Newcastle Map Extraction and Realism Data

You are working inside the TYNE CITY repository. The project owner has explicitly approved the initial area and scale on 18 November 2026. The approved configuration is already recorded in `data/configs/newcastle-core.json`.

## 1. Read before acting

Read these files in full:

- `TYNE_CITY_SPEC.md`
- `CLAUDE.md`
- `docs/BUILDING_REALISM_PLAN.md`
- `scripts/map-pipeline/README.md`
- `docs/decisions/0002-initial-map-area.md`
- `docs/PROJECT_STATUS.md`
- `docs/weekly-reports/week-02.md`

The owner-approved decision is:

- Central Newcastle around Monument/Grey Street, Haymarket and Central Station.
- Quayside and the full Tyne Bridge crossing/approach.
- Wider Gateshead is deferred; the bridge's south landing is included.
- Real-world 1:1 scale.
- EPSG:27700 for projected metric processing.
- GeoJSON in EPSG:4326.
- Grey's Monument is the local origin.
- Three.js axes: X east, Y elevation, Z south.

Do not ask the owner to approve this boundary again.

## 2. Work safely in the repository

1. Inspect `git status`, current branch, recent commits and existing files.
2. Fetch/pull the latest `main` before creating a feature branch.
3. Create branch `feature/phase-1-newcastle-map-data`.
4. Preserve all Sprint 1 working code.
5. Do not overwrite the current Three.js scene yet.
6. Do not commit raw downloads, virtual environments, caches, or large intermediate files.
7. Do not push or merge without reporting the change and receiving the owner's instruction.
8. Do not claim a browser test or local command passed unless you actually ran it.

## 3. Validate and improve the extraction pipeline

The current starter script is `scripts/map-pipeline/extract_osm.py`. Review it against the installed OSMnx 2.x API and fix any bugs before extraction.

Requirements:

- Create a local Python virtual environment; do not install packages globally.
- Use a supported Python version already installed. Prefer Python 3.11 or 3.12 if available.
- Install `scripts/map-pipeline/requirements.txt`.
- Run `python scripts/map-pipeline/extract_osm.py --check-config` first. This must not make network requests.
- Check that `owner_approved_for_extraction` is true.
- Only then run `python scripts/map-pipeline/extract_osm.py --confirm-boundary`.
- Do not repeatedly hammer Overpass if it rate-limits or fails. Use the script's bounded retry behaviour and report the error if the service remains unavailable.

Before extraction, inspect and improve these data requirements:

### Roads and navigation

- Extract a driving network for cars.
- Extract a walking network for pavements, footways and pedestrian-only streets.
- Preserve names, highway class, lanes, width, maxspeed, oneway, surface, bridge, tunnel, layer, access and OSM IDs wherever available.
- Keep the driving and walking graphs separate.
- Do not assume OSM road centre-lines have exact road widths. Use explicit width/lanes tags where present and mark class-based widths as estimates.

### Buildings

- Query both `building=*` and `building:part=*`.
- Keep building outlines and building parts in separate logical layers.
- Preserve OSM element type and ID.
- Preserve all available relevant tags, especially:
  - `height`
  - `min_height`
  - `building:levels`
  - `building:min_level`
  - `roof:shape`
  - `roof:height`
  - `roof:levels`
  - `roof:angle`
  - `roof:orientation`
  - `roof:material`
  - `roof:colour`
  - `building:material`
  - `building:colour`
  - `building:use`
  - `building:type`
- Do not discard building parts. Some complex buildings are represented by several parts with different heights and roof forms.
- Do not render both an outer building outline and overlapping building parts as independent full buildings. Later mesh generation must use parts as the detailed geometry where they exist and avoid duplicated volumes.
- Report how many buildings have explicit heights, levels, roof tags, material/colour tags and associated building parts.

### Water, parks and landmarks

- Keep water polygons separate from river/waterway line features.
- Preserve riverbank/waterway geometry so the River Tyne can later be represented as a continuous water surface with real width.
- Extract parks, gardens, grass/recreation areas, named points of interest, historic features and major transport landmarks.
- Preserve names and source IDs.
- Do not assume every OSM feature is a polygon; handle points, lines and multipolygons correctly.

### Geometry and provenance

- Validate/repair invalid geometries only where it is safe; record counts of repaired and dropped features.
- Keep source OSM attributes separate from estimates.
- Do not silently replace missing heights with guessed facts.
- Export a clear manifest with retrieval timestamp, OSMnx version, bbox, CRS, local origin in EPSG:27700, scale, layer names, feature counts, source URL and licence.
- Generate a QA report with empty layers, invalid geometries, feature counts, missing-tag percentages and output file sizes.
- Use reproducible output names and make reruns safe.

## 4. Investigate Environment Agency LiDAR for realism

The project has identified these official datasets:

- Environment Agency 1 m LiDAR Composite DTM: https://environment.data.gov.uk/dataset/13787b9a-26a4-4775-8523-806d13af58fc
- Environment Agency 1 m LiDAR Composite DSM: https://environment.data.gov.uk/dataset/9ba4d5ac-d596-445a-9056-dae3ddec0178

The DTM can provide more accurate bare-earth terrain. The DSM includes surface objects such as buildings and vegetation. Their difference can help estimate above-ground massing, but must not be treated as exact building height without classification and quality checks.

Tasks:

1. Inspect the official dataset metadata and licence.
2. Identify the exact 5 km tile or tiles covering the approved map boundary.
3. Record tile names, dates/metadata, CRS, vertical datum, resolution, licence and approximate download size.
4. Verify alignment with EPSG:27700 and the elevation reference before using the rasters.
5. If download size and terms are practical, download only the required tile(s), clip to the approved area and create a documented local processing step.
6. If download is too large, unavailable or unclear, do not guess. Report the blocker and provide a reproducible acquisition plan.
7. Do not treat trees or other elevated objects as buildings. Compare DSM with DTM and use building footprints to mask/classify candidate building heights.
8. Preserve Environment Agency attribution: `© Environment Agency copyright and/or database right 2022`, subject to the dataset's current terms.

## 5. Building realism requirements

The goal is a realistic 3D reconstruction, not generic low-poly boxes. However, do not claim the result is photogrammetric or photorealistic unless the source data supports that.

Use a tiered approach:

### Ordinary buildings

- Actual building footprints at real-world scale.
- Heights from OSM `height`, then building levels with a configurable storey-height assumption, then validated LiDAR-derived estimates, then a clearly labelled fallback estimate.
- Record `height_source` and confidence for every derived height.
- Roof geometry based on real roof tags where available.
- Distinct material classes informed by building type and OSM tags.
- Procedural floor bands, window bays, doors and shopfront zones.
- Variation should be plausible and deterministic, not random on each run.
- Preserve footprints with holes and multipolygon geometry.

### Important streetscapes

Prioritise Grey Street/Grainger Town, Northumberland Street, Monument, Central Station approaches and Quayside. Use targeted facade modules and higher-quality Blender models where justified.

### Hero landmarks

Plan bespoke models for the Tyne Bridge, Grey's Monument, Central Station and selected recognisable buildings. Start with accurate silhouette, proportions and location, then improve materials and detail.

Only use original project photography or assets with an explicit licence allowing the intended use. Do not scrape Google Street View/Google Earth imagery, rip assets from commercial games, or use unlicensed textures.

## 6. First visual deliverable

Do not start player, vehicle, NPC, police or mission work.

First produce:

1. Validated GIS datasets.
2. A map data QA report.
3. A local preview showing actual Newcastle roads, building footprints, water, parks and landmark candidates.
4. A simple real-scale 3D massing preview with actual building footprints and available heights, only after the data passes QA.
5. A visual comparison/checklist for obvious misalignment, missing streets, bad heights, duplicated parts and gaps.

The initial preview may use simple materials, but it must use actual extracted Newcastle geometry. It must not use the old random placeholder blocks as the city.

## 7. Browser quality and performance

When creating the preview:

- Keep geometry local to the Grey's Monument origin.
- Use metres with the approved axis convention.
- Build road surfaces from road lines with configurable class widths.
- Build building roofs and extrusions from valid polygon geometry.
- Avoid one unique draw call per window or small object.
- Use instancing/merged static geometry where suitable.
- Keep collision geometry separate from visual geometry.
- Record FPS, draw calls, triangle count, loaded feature counts and asset size.
- Do not load all future Newcastle districts; only the approved initial area.

## 8. Definition of Done for this task

This task is complete only when:

- Python setup is reproducible and documented.
- Config validation passes.
- Approved OSM extraction has run or a specific external-service blocker is documented.
- Output files are valid and contain expected features.
- A manifest and QA report have been generated.
- Building height/tag coverage is quantified.
- LiDAR acquisition has been evaluated and either integrated or documented as a next task.
- A real-geometry map preview has been produced.
- Existing `npm run build` and `npm test` still pass.
- README, project status and Week 02 report reflect only verified outcomes.
- A screenshot of the extracted map preview is saved under `docs/assets/`.
- Changes are committed on the feature branch, but not merged or pushed without owner approval.

## 9. Final report format

Report:

1. Files changed.
2. Commands executed.
3. Python, OSMnx, GeoPandas and Shapely versions.
4. Extraction time and service outcomes.
5. Feature counts by layer.
6. Building attribute coverage and percentage of estimated heights.
7. LiDAR tile decision, size, licence and result.
8. QA results and known data gaps.
9. Preview screenshot path.
10. Build/test results.
11. Commit hash and branch.
12. Exact next task.

Do not move to the player controller until the map preview has been inspected and accepted by the project owner.
