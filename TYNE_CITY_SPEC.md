# TYNE CITY

## Game Design Document, Software Requirements Specification & Technical Roadmap

**Document version:** 1.0\
**Status:** Initial project baseline\
**Project type:** Solo indie game / portfolio project\
**Target platform:** Desktop web browsers\
**Primary engine:** Three.js + TypeScript\
**Working title:** TYNE CITY\
**Last updated:** 17 November 2026

------------------------------------------------------------------------

# 1. Executive Summary

TYNE CITY is a browser-based, single-player, open-world 3D game set in a
recognisable recreation of Newcastle upon Tyne, England, and surrounding
areas.

The game takes inspiration from the freedom and systemic gameplay of
open-world urban games. It is not intended to reproduce Grand Theft
Auto's copyrighted characters, missions, maps, branding, music, assets,
or other protected material. It will have its own identity, setting,
characters, story, visual language, and mechanics.

The central technical and creative premise is:

> Build a playable, semi-realistic version of Newcastle using real-world
> geographic data, procedural 3D environment generation, browser-based
> rendering, and custom gameplay systems.

The player should eventually be able to:

-   Explore Newcastle on foot.
-   Enter, drive, and exit vehicles.
-   Navigate a recognisable road network.
-   Encounter traffic and pedestrians.
-   Interact with objects and characters.
-   Experience missions and a wanted/police response system.
-   Explore a city that changes through a day/night cycle and weather.
-   Play the game through a public web URL without installing a desktop
    game.

The project should be developed in incremental releases. The first
objective is not to build every GTA-like feature. It is to create a
small, recognisable, performant, playable slice of Newcastle and expand
it systematically.

## 1.1 Product principles

1.  **Playable early:** deliver a small working game before building the
    full feature set.
2.  **Geographic authenticity:** use real Newcastle road layouts and
    building footprints where licensing and data quality permit.
3.  **Visual believability over raw polygon count:** prioritise
    lighting, materials, scale, silhouettes, landmarks, and street
    composition.
4.  **Browser performance:** design for a realistic desktop browser
    performance budget.
5.  **Modular architecture:** gameplay systems must be independent
    enough to develop and test separately.
6.  **Data-driven content:** missions, vehicles, landmarks, and tuning
    values should be configurable rather than hard-coded throughout the
    codebase.
7.  **Visible progress:** each week should produce a demonstrable
    improvement, screenshot, clip, or playable build.
8.  **Original IP:** use original or properly licensed models, audio,
    textures, names, and narrative content.

------------------------------------------------------------------------

# 2. Product Vision and Scope

## 2.1 Intended experience

The player launches the game in a desktop browser and enters a
third-person 3D environment. They spawn at a defined location in
Newcastle city centre, can walk through the environment, approach a
vehicle, enter it, and drive through the city.

The initial map should contain a compact but recognisable section of
central Newcastle. The world can expand later into Jesmond, Heaton,
Gateshead, and additional neighbourhoods.

The game should feel like a small, coherent urban world rather than a
map viewer with a character placed on top.

## 2.2 Target audience

-   People familiar with Newcastle and the North East.
-   Players interested in open-world driving and exploration.
-   Browser-game audiences.
-   Developers and game-development communities.
-   Recruiters and engineering teams interested in the project's
    technical work.

## 2.3 Release definitions

### Release 0: Technical prototype

A browser page renders a Three.js scene, accepts input, and loads a
small test environment.

### Release 1: First playable Newcastle

A player can walk around a small, geographically grounded Newcastle
environment. Buildings, roads, a basic camera, collision, and a simple
HUD work.

### Release 2: Driving prototype

A player can enter and exit at least one vehicle and drive around the
map with usable physics and camera behaviour.

### Release 3: Living city

The world includes basic traffic, pedestrians, environmental ambience,
and a day/night cycle.

### Release 4: Gameplay systems

The game includes interactions, missions, police response, wanted
levels, and a basic progression loop.

### Release 5: Public demo

The game is deployed publicly, has an onboarding flow, settings,
performance checks, analytics that respect privacy, and a feedback
mechanism.

A public demo is not the same as a complete commercial game. The project
should be considered successful when its core loop is stable,
understandable, and enjoyable.

------------------------------------------------------------------------

# 3. Initial Product Decisions and Assumptions

These are the baseline decisions unless the project owner changes them.

  -----------------------------------------------------------------------
  Topic                               Baseline
  ----------------------------------- -----------------------------------
  Game mode                           Single-player

  Multiplayer                         Out of scope for initial releases

  Platform                            Desktop browser

  Initial browser support             Latest stable Chrome and Edge; test
                                      Firefox where practical

  Mobile                              Not a launch target; architecture
                                      should avoid unnecessary mobile
                                      assumptions

  Rendering                           WebGL through Three.js

  Language                            TypeScript

  Build tool                          Vite

  Physics                             Rapier 3D

  Geographic source                   OpenStreetMap and other
                                      appropriately licensed sources

  Geographic processing               Python, OSMnx, GeoPandas, Shapely,
                                      PyProj

  3D authoring                        Blender

  Runtime asset format                GLB/glTF

  Map representation                  GeoJSON during processing; chunked
                                      runtime assets

  Hosting                             Static hosting such as Cloudflare
                                      Pages or Vercel, subject to
                                      deployment requirements

  Backend                             No mandatory backend for first
                                      playable release

  Persistence                         Local save initially; backend only
                                      when justified

  Visual style                        Semi-realistic, optimised for
                                      browser rendering

  Camera                              Third-person by default

  Controls                            Keyboard and mouse; controller
                                      support may follow

  World scale                         Real-world metres converted into a
                                      local game coordinate system

  Initial map                         Newcastle city centre and Quayside

  Expansion                           Jesmond, Heaton, Gateshead, and
                                      further districts
  -----------------------------------------------------------------------

Do not silently introduce multiplayer, accounts, a complex backend, a
live map service dependency, or a large procedural AI framework before
the single-player prototype is playable.

------------------------------------------------------------------------

# 4. Technical Architecture

## 4.1 Technology stack

  -----------------------------------------------------------------------
  Layer                   Technology              Responsibility
  ----------------------- ----------------------- -----------------------
  Runtime                 Browser                 Runs the game

  Rendering               Three.js                Scene graph, cameras,
                                                  meshes, materials,
                                                  lighting

  Language                TypeScript              Gameplay and
                                                  application logic

  Build/development       Vite                    Local server, bundling,
                                                  asset handling

  Physics                 Rapier 3D               Rigid bodies,
                                                  colliders, raycasts,
                                                  vehicle physics
                                                  foundation

  Geographic extraction   OSMnx                   Road networks and OSM
                                                  feature extraction

  Geographic processing   GeoPandas, Shapely,     Geometry filtering,
                          PyProj                  projection, clipping,
                                                  transformations

  3D authoring            Blender                 Landmark models, props,
                                                  custom vehicles, UVs
                                                  and optimisation

  Runtime assets          GLB/glTF                3D asset delivery

  Data interchange        GeoJSON, JSON           Roads, buildings,
                                                  points of interest,
                                                  configuration

  Testing                 Vitest and              Unit and integration
                          browser-based tests     tests
                          where useful            

  Version control         Git                     Source history and
                                                  collaboration

  Repository              GitHub                  Source hosting, issues,
                                                  project tracking

  Hosting                 Cloudflare Pages or     Public static web
                          Vercel                  deployment
  -----------------------------------------------------------------------

### Why Three.js

Three.js offers direct control over a browser-based 3D world and is a
suitable foundation for a custom game architecture. It does not provide
a complete GTA-style game framework by itself. Camera controls, player
controllers, vehicle systems, world streaming, interactions, and game
state must be implemented or integrated deliberately.

### Why Rapier

Rapier provides WebAssembly-backed physics for JavaScript environments.
It can support rigid bodies, colliders, collision queries, and physics
simulation. Vehicle behaviour will still require custom controller logic
and careful tuning.

### Important architecture rule

Rendering and physics must be separate concerns.

-   Three.js owns visual objects.
-   Rapier owns physical bodies and colliders.
-   A synchronisation layer copies physics transforms to visual objects.
-   Gameplay systems communicate through defined interfaces or events.
-   Do not make every system directly manipulate every other system.

## 4.2 Suggested repository structure

Start with a small structure and expand as systems are implemented.

``` text
tyne-city/
├── public/
│   ├── assets/
│   │   ├── characters/
│   │   ├── vehicles/
│   │   ├── buildings/
│   │   ├── props/
│   │   ├── audio/
│   │   └── textures/
│   ├── maps/
│   │   ├── chunks/
│   │   ├── manifests/
│   │   └── landmarks/
│   └── favicon.svg
│
├── scripts/
│   └── map-pipeline/
│       ├── extract_osm.py
│       ├── process_roads.py
│       ├── process_buildings.py
│       ├── project_coordinates.py
│       ├── generate_manifest.py
│       └── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── configs/
│
├── src/
│   ├── app/
│   │   ├── bootstrap.ts
│   │   └── config.ts
│   ├── core/
│   │   ├── Game.ts
│   │   ├── GameLoop.ts
│   │   ├── EventBus.ts
│   │   ├── InputManager.ts
│   │   ├── AssetManager.ts
│   │   └── Logger.ts
│   ├── rendering/
│   │   ├── Renderer.ts
│   │   ├── Lighting.ts
│   │   ├── Environment.ts
│   │   └── QualitySettings.ts
│   ├── world/
│   │   ├── World.ts
│   │   ├── WorldStreamer.ts
│   │   ├── Chunk.ts
│   │   ├── CoordinateSystem.ts
│   │   └── CollisionWorld.ts
│   ├── city/
│   │   ├── CityLoader.ts
│   │   ├── RoadBuilder.ts
│   │   ├── BuildingBuilder.ts
│   │   ├── TerrainBuilder.ts
│   │   └── LandmarkManager.ts
│   ├── player/
│   │   ├── Player.ts
│   │   ├── PlayerController.ts
│   │   ├── PlayerCamera.ts
│   │   └── PlayerAnimation.ts
│   ├── physics/
│   │   ├── PhysicsWorld.ts
│   │   ├── PhysicsSync.ts
│   │   └── CollisionLayers.ts
│   ├── vehicles/
│   │   ├── Vehicle.ts
│   │   ├── VehicleController.ts
│   │   ├── VehicleCamera.ts
│   │   ├── VehicleManager.ts
│   │   └── VehicleConfig.ts
│   ├── ai/
│   │   ├── traffic/
│   │   ├── pedestrians/
│   │   └── police/
│   ├── gameplay/
│   │   ├── InteractionSystem.ts
│   │   ├── MissionSystem.ts
│   │   ├── WantedSystem.ts
│   │   └── ProgressionSystem.ts
│   ├── ui/
│   │   ├── HUD.ts
│   │   ├── Minimap.ts
│   │   ├── MainMenu.ts
│   │   ├── PauseMenu.ts
│   │   └── SettingsMenu.ts
│   ├── audio/
│   │   ├── AudioManager.ts
│   │   └── AudioConfig.ts
│   ├── save/
│   │   ├── SaveManager.ts
│   │   └── SaveSchema.ts
│   └── main.ts
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── weekly-reports/
│   ├── map-pipeline/
│   └── assets/
│
├── .github/
│   └── workflows/
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
├── README.md
├── CLAUDE.md
└── SPEC.md
```

Do not create empty files for every future system immediately. Add
modules when their phase begins. The structure is a target architecture,
not a demand for placeholder code.

------------------------------------------------------------------------

# 5. Newcastle Geographic Data Pipeline

This is a core differentiator of the project.

## 5.1 Data sources

### OpenStreetMap

Use OSM data for:

-   Road centre lines and road classifications.
-   Building footprints.
-   Building names and tags where available.
-   Building height or level tags where available.
-   Parks and green spaces.
-   Waterways and water polygons.
-   Bridges and tunnels where mapped.
-   Points of interest and landmark locations.

OSM data quality and completeness vary by location. Missing tags must be
handled gracefully.

### Additional data sources

Potential future sources:

-   Open elevation data for terrain and river banks.
-   Open government datasets for public-space or transport context.
-   Original photographs and field observations for landmark modelling.
-   Properly licensed 3D assets for generic vehicles, street furniture,
    and vegetation.

Every external dataset must have a source record, licence, attribution
requirements, date retrieved, and any processing notes.

## 5.2 Initial geographic scope

The first area should be deliberately limited.

Initial target districts and landmarks:

-   Grey's Monument and Monument area.
-   Grey Street.
-   Northumberland Street.
-   Haymarket.
-   Central Station.
-   Newcastle city centre.
-   Quayside.
-   Tyne Bridge.
-   Gateshead riverside, if the initial boundary permits.

Expansion candidates:

-   Jesmond.
-   Heaton.
-   Ouseburn.
-   Gateshead town centre.
-   Further Newcastle neighbourhoods.

The project owner must approve a geographic boundary before large-scale
extraction. Use a saved polygon or bounding box configuration rather
than scattering coordinates across scripts.

## 5.3 Coordinate reference system

Do not use longitude and latitude directly as Three.js world
coordinates.

Use a projected coordinate reference system suitable for the area, such
as British National Grid (EPSG:27700), or another appropriate local
metric projection.

Recommended approach:

1.  Retrieve source features in their original CRS.
2.  Reproject all geometries into the selected metric CRS.
3.  Select a fixed local origin near the centre of the game map.
4.  Subtract the origin easting/northing from all coordinates.
5.  Map projected eastings to Three.js X.
6.  Map projected northings to Three.js Z, with a consistent sign
    convention.
7.  Map elevation to Three.js Y.
8.  Store the origin, CRS, units, and axis convention in the map
    manifest.

Use real-world metres as the initial game scale. Keep a single
documented conversion factor in case later gameplay requires a
deliberate scale adjustment.

## 5.4 Map extraction

Create reproducible Python scripts. Avoid relying on a single
unrepeatable notebook.

Expected pipeline:

1.  Load configured area of interest.
2.  Download road network and relevant OSM features.
3.  Download building footprints.
4.  Download parks, water, and selected point features.
5.  Validate and repair invalid geometries where safe.
6.  Reproject to the metric CRS.
7.  Clip to the approved boundary.
8.  Remove irrelevant or malformed geometries.
9.  Preserve useful source tags.
10. Export processed GeoJSON or a more efficient intermediate format.
11. Produce a summary report with feature counts, missing tags, and
    warnings.
12. Generate a manifest describing data provenance and coordinate
    conventions.

The extraction pipeline must be repeatable and should not overwrite raw
source data without an explicit command.

### Road attributes to preserve

Where available:

-   OSM way identifier.
-   Name.
-   Highway classification.
-   One-way flag.
-   Speed limit.
-   Surface.
-   Lanes.
-   Bridge/tunnel status.
-   Geometry.
-   Access restrictions.

### Building attributes to preserve

Where available:

-   OSM feature identifier.
-   Building type.
-   Name.
-   Height.
-   Number of levels.
-   Roof shape and roof height tags.
-   Material or colour hints.
-   Geometry.

If height is missing, use a configurable heuristic based on building
type or level count. Clearly mark estimated heights in the generated
data. Do not imply estimated heights are surveyed facts.

## 5.5 Road geometry generation

The initial road builder should:

-   Convert road centre lines into road surfaces.
-   Assign widths based on road class and available lane information.
-   Create intersections that do not show obvious gaps.
-   Support one-way metadata for future traffic logic.
-   Preserve road names and IDs for navigation and debugging.
-   Handle curves smoothly.
-   Avoid z-fighting with sidewalks and ground.
-   Use material groups or merged geometry to reduce draw calls.

Road widths must be configurable by road class. The first version may
use approximate widths, then improve them using local observation.

Road markings, pavements, crossings, kerbs, bus stops, and street
furniture should be added progressively.

## 5.6 Building generation

Initial procedural building generation:

1.  Read polygon footprint.
2.  Validate geometry.
3.  Convert polygon to local coordinates.
4.  Triangulate footprint.
5.  Extrude to estimated or known height.
6.  Add a roof.
7.  Assign a material based on broad building category.
8.  Generate collision geometry separately from visual geometry.
9.  Store source ID and generated asset metadata.

Do not assume every building should be a plain cuboid. The procedural
system should eventually support:

-   Flat and pitched roofs.
-   Different facade materials.
-   Ground-floor shopfronts.
-   Building setbacks.
-   Repeated window patterns.
-   Variation in height and roof silhouette.

For the first release, convincing massing and street layout are more
important than detailed interiors.

## 5.7 Landmark strategy

Procedural buildings will establish the city, but important landmarks
deserve custom treatment.

Priority landmark list:

1.  Tyne Bridge.
2.  Grey's Monument.
3.  Newcastle Central Station.
4.  Monument and surrounding streetscape.
5.  Quayside waterfront.
6.  Distinctive civic and historic buildings selected after visual
    research.

Landmark workflow:

-   Collect reference photographs or appropriately licensed references.
-   Record approximate dimensions and geographic placement.
-   Build a low-to-medium detail model in Blender.
-   Optimise meshes and materials.
-   Export GLB.
-   Add collision geometry.
-   Validate scale and orientation in the game.

Do not use ripped assets from commercial games or unlicensed 3D scans.

## 5.8 Terrain and River Tyne

A flat plane is acceptable for the first technical test, not the final
city.

Future terrain pipeline:

-   Acquire suitable elevation data.
-   Reproject and clip to the map boundary.
-   Convert elevation into a mesh or heightmap.
-   Blend road surfaces with surrounding terrain.
-   Model river and shoreline separately.
-   Account for bridges, embankments, and underpasses.
-   Avoid terrain geometry intersecting roads and buildings.

The river should be a distinct environment feature, with water material,
shoreline, and bridge integration.

## 5.9 Chunking and world streaming

Do not render the entire expanded city as one monolithic scene.

Initial proposed chunk size: 250 m × 250 m in world coordinates. Treat
this as a configurable starting point, not a fixed truth.

Each chunk should have:

-   Stable chunk ID.
-   Bounding box.
-   Road geometry.
-   Building geometry.
-   Props and vegetation.
-   Collision data.
-   Landmark references.
-   Asset references.
-   Version and source metadata.

The world streamer should:

-   Determine which chunks are near the player.
-   Load nearby chunks asynchronously.
-   Keep a configurable number of surrounding chunks active.
-   Unload distant chunks safely.
-   Avoid unloading the chunk containing the player.
-   Avoid duplicate entities at chunk boundaries.
-   Provide a fallback if a chunk fails to load.
-   Display loading/debug information during development.

For the first small prototype, loading one complete test area is
acceptable. Implement streaming only when the map size justifies it.

## 5.10 Data and licensing

OpenStreetMap data is licensed under the Open Database License (ODbL).
Review current OSM attribution and share-alike obligations before public
distribution. Display appropriate attribution in the game and document
the data source.

For every asset and dataset, maintain an asset register:

  Field           Description
  --------------- ---------------------------------
  Asset ID        Stable identifier
  Name            Human-readable name
  Source          Original creator or dataset
  Licence         Exact licence or terms
  Attribution     Required credit
  Modification    Whether modified
  File path       Repository path
  Date acquired   Date retrieved
  Release use     Whether cleared for public demo

Do not use Rockstar trademarks, logos, music, characters, maps, or
extracted game assets. The game may be described as inspired by the
open-world genre, but its branding and content must be original.

------------------------------------------------------------------------

# 6. Game Runtime and Core Systems

## 6.1 Game bootstrap

The application must:

-   Create the renderer and scene.
-   Initialise camera and lighting.
-   Initialise input.
-   Load configuration.
-   Initialise the physics world.
-   Load the initial map area.
-   Spawn the player.
-   Start the game loop.
-   Handle browser resize.
-   Handle page visibility and pause behaviour.
-   Dispose of resources on teardown.

The game should show a useful loading screen and a recoverable error
state if assets fail.

## 6.2 Game loop

Use a fixed timestep for physics and a render loop for visual
presentation.

Requirements:

-   Use `requestAnimationFrame` for rendering.
-   Use a fixed or bounded timestep for physics.
-   Clamp unusually large frame deltas.
-   Avoid unbounded catch-up loops.
-   Separate update phases clearly.
-   Do not create new geometries, materials, or event listeners every
    frame.
-   Ensure pause and resume do not cause physics explosions.

## 6.3 Input system

Initial keyboard controls:

  -----------------------------------------------------------------------
  Input                               Action
  ----------------------------------- -----------------------------------
  W / Arrow Up                        Move forward / accelerate

  S / Arrow Down                      Move backward / brake

  A / Arrow Left                      Move left / steer left

  D / Arrow Right                     Move right / steer right

  Shift                               Sprint / handbrake contextually

  Space                               Jump on foot / handbrake in
                                      vehicle, subject to final mapping

  E                                   Interact / enter / exit vehicle

  F                                   Alternative vehicle interaction if
                                      required

  Esc                                 Pause

  Mouse                               Camera control

  M                                   Toggle minimap
  -----------------------------------------------------------------------

Avoid conflicting mappings. The final control map must be shown in the
settings menu and be configurable where practical.

Input requirements:

-   Track key down/up state.
-   Handle lost focus and blur.
-   Prevent stuck movement keys after tab switching.
-   Support mouse pointer lock for camera control.
-   Provide a way to release pointer lock.
-   Keep gameplay input separate from UI input.

## 6.4 Player controller

Initial third-person controller:

-   Walk.
-   Run.
-   Sprint.
-   Jump.
-   Gravity.
-   Ground detection.
-   Slope handling.
-   Collision with world geometry.
-   Basic idle/walk/run animations.
-   Camera-relative movement.
-   Smooth acceleration and deceleration.
-   Interaction range detection.

Use a capsule collider or another suitable character collision approach.
Do not use a high-detail character mesh as the physical collider.

The controller should feel responsive, predictable, and stable on uneven
ground.

## 6.5 Third-person camera

Requirements:

-   Follow player position.
-   Orbit using mouse.
-   Adjustable sensitivity.
-   Adjustable distance.
-   Smooth damping.
-   Camera collision handling.
-   Avoid clipping through buildings and terrain.
-   Sensible default field of view.
-   Separate tuning for on-foot and vehicle cameras.
-   Respect pause and pointer-lock state.

## 6.6 Physics architecture

Physics requirements:

-   Central physics world.
-   Documented collision groups.
-   Static world colliders.
-   Dynamic player/vehicle bodies.
-   Collision filtering.
-   Raycasts and shape casts where useful.
-   Fixed timestep.
-   Physics-to-render synchronisation.
-   Debug visualisation toggle.
-   Safe creation and disposal of bodies.

Keep visual geometry and collision geometry separate. Collision meshes
should be simpler than visual meshes wherever possible.

------------------------------------------------------------------------

# 7. Vehicle System

Vehicles are a major milestone and should not be attempted before the
player and world are stable.

## 7.1 First vehicle

Start with one fictional, generic car. Do not model a real-world branded
vehicle unless its design and branding are appropriately licensed.

Initial features:

-   Spawn one car in a clear test area.
-   Approach car.
-   Enter car.
-   Switch camera.
-   Accelerate.
-   Brake and reverse.
-   Steer.
-   Handbrake.
-   Exit car.
-   Prevent player and vehicle occupying the same interaction state.
-   Basic collision response.

## 7.2 Vehicle physics

A simple arcade-style vehicle controller is acceptable initially. The
target is fun, stable handling rather than a full racing simulation.

Potential approaches:

-   Raycast-based wheel suspension and tyre forces.
-   A custom simplified vehicle controller using Rapier rigid bodies.
-   A more complete vehicle model only if the first implementation
    proves inadequate.

Parameters should be configurable:

-   Mass.
-   Centre of mass.
-   Engine force.
-   Maximum speed.
-   Brake force.
-   Steering angle.
-   Steering response.
-   Wheelbase.
-   Track width.
-   Suspension stiffness.
-   Suspension damping.
-   Grip.
-   Handbrake grip.
-   Reverse speed.

Do not hard-code tuning constants throughout the controller.

## 7.3 Vehicle interaction state

Define clear states, for example:

-   `onFoot`
-   `enteringVehicle`
-   `inVehicle`
-   `exitingVehicle`

Only one active player control mode should exist at a time.

Vehicle entry should check:

-   Vehicle is close enough.
-   A suitable door/entry point exists.
-   Player is not already in another vehicle.
-   Vehicle is in a valid state.
-   The exit position is not blocked.

## 7.4 Vehicle camera

-   Smooth follow.
-   Look-ahead at speed.
-   Camera collision.
-   Speed-sensitive damping.
-   Different behaviour when stationary and moving.
-   Return to on-foot camera after exiting.

------------------------------------------------------------------------

# 8. Living City Systems

These systems are deliberately deferred until the map, player, and
vehicle loop work.

## 8.1 Traffic

Initial traffic should be low density and deterministic enough to debug.

Features:

-   Road graph derived from road network.
-   Route selection between nodes.
-   Lane or direction awareness.
-   Basic traffic signals.
-   Following distance.
-   Braking and acceleration.
-   Junction handling.
-   Collision avoidance.
-   Spawn/despawn by distance.
-   Vehicle pooling where useful.

Do not attempt city-wide realistic traffic simulation in the first
implementation. Begin with a small test route and a handful of vehicles.

## 8.2 Pedestrians

Features:

-   Spawn points on suitable pavements and public areas.
-   Simple navigation graph or navigation mesh.
-   Walk cycles.
-   Basic wandering and destination behaviour.
-   Avoid walking into roads where practical.
-   Player proximity reactions.
-   Distance-based spawning and despawning.
-   Pooling and population limits.

Use simple AI state machines initially. Do not introduce an expensive
general-purpose AI framework without a demonstrated need.

## 8.3 Police and wanted system

This is a fictional gameplay system, not a simulation of real police
operations.

Initial wanted-level concept:

-   A small number of wanted levels.
-   A crime/event triggers a wanted state.
-   Police units spawn at controlled locations outside the player's
    immediate view.
-   Police follow the player using simplified navigation.
-   Wanted state decays when the player escapes detection for a
    configured period.
-   Police units despawn or return to patrol when the pursuit ends.

All behaviour must be configurable and testable.

## 8.4 Missions

Mission system should be data-driven.

A mission definition should include:

-   Unique ID.
-   Display name.
-   Description.
-   Start condition.
-   Objectives.
-   Objective completion conditions.
-   Failure conditions.
-   Rewards.
-   Mission state.
-   Optional time limit.
-   Checkpoints.
-   Completion event.

Example original mission concept:

**The Quayside Delivery**

-   Meet an original fictional character at a designated location.
-   Enter a vehicle.
-   Drive to a marked destination.
-   Complete the objective.
-   Receive an in-game reward.

This is an example of a gameplay structure, not final story content.

## 8.5 Interactions

Build a reusable interaction system:

-   Detect nearby interactable objects.
-   Show contextual prompt.
-   Check distance and line of sight where appropriate.
-   Trigger an interaction action.
-   Support vehicles, characters, mission markers, doors, and objects.
-   Avoid each gameplay feature implementing its own unrelated proximity
    logic.

## 8.6 Day/night and weather

Later features:

-   Time-of-day progression.
-   Sun and sky changes.
-   Street lights.
-   Rain.
-   Wet-road visual treatment.
-   Fog and atmospheric effects.
-   Weather configuration.

Start with a fixed daytime environment. Dynamic weather must not be a
blocker for the first playable release.

------------------------------------------------------------------------

# 9. User Interface and Game Experience

## 9.1 Initial UI

First playable release:

-   Loading indicator.
-   Basic start screen or start overlay.
-   Control instructions.
-   Minimal crosshair or interaction indicator if needed.
-   Pause menu.
-   Basic debug overlay during development.

## 9.2 Later HUD

-   Health or player condition if required by gameplay.
-   Vehicle speed.
-   Current objective.
-   Wanted-level indicator.
-   Minimap.
-   Interaction prompt.
-   Mission notifications.
-   Settings menu.

Avoid clutter. The game world should remain the primary focus.

## 9.3 Minimap

The minimap should use the same underlying map data as the game.

Initial implementation may render a simplified top-down representation
of roads and the player's position.

Later improvements:

-   Player heading.
-   Nearby roads.
-   Mission markers.
-   Vehicle marker.
-   Police markers where appropriate.
-   Zoom controls.

Do not depend on a third-party live map API at runtime for the core game
map.

------------------------------------------------------------------------

# 10. Performance and Quality Requirements

Browser performance is a primary constraint.

## 10.1 Target hardware assumptions

Initial development target:

-   Modern desktop/laptop.
-   Dedicated GPU preferred but not required.
-   16 GB RAM recommended for development.
-   Current stable Chrome or Edge.
-   1080p display target.

The game should degrade gracefully on weaker hardware.

## 10.2 Performance targets

Initial targets, to be validated on representative machines:

  -----------------------------------------------------------------------
  Metric                              Target
  ----------------------------------- -----------------------------------
  Frame rate                          Aim for stable 60 FPS on target
                                      desktop hardware

  Lower-end fallback                  Usable 30 FPS with reduced settings

  Initial scene                       Load a small playable area without
                                      long blocking work

  Rendering                           Avoid excessive draw calls and
                                      unnecessary material changes

  Memory                              Avoid unbounded growth while moving
                                      between chunks

  Asset loading                       Load asynchronously where possible

  Recovery                            Show an error message if a required
                                      asset fails
  -----------------------------------------------------------------------

These are targets, not claims that the game already meets them.

## 10.3 Optimisation techniques

Use where justified:

-   Instanced meshes for repeated objects.
-   Geometry merging for static geometry.
-   Frustum culling.
-   Level of detail.
-   Chunk-based loading.
-   Texture atlases where useful.
-   Compressed textures where supported.
-   GLB asset compression.
-   Reuse of materials.
-   Object pooling.
-   Simplified collision meshes.
-   Baked lighting for static environments where practical.
-   Limit active AI entities by distance.
-   Avoid per-frame allocations.
-   Avoid excessive real-time shadows.

Do not optimise blindly. Profile first, record the bottleneck, make one
targeted change, and measure again.

## 10.4 Quality settings

Provide configurable settings:

-   Render resolution scale.
-   Shadow quality.
-   Draw distance.
-   Texture quality.
-   Anti-aliasing where supported.
-   Crowd density.
-   Traffic density.
-   Effects quality.

The game should have a sensible default quality level and a
lower-performance preset.

------------------------------------------------------------------------

# 11. Testing and Quality Assurance

Every milestone must include tests and a manual playtest checklist.

## 11.1 Unit tests

Test pure logic where practical:

-   Coordinate conversion.
-   Chunk coordinate calculation.
-   Road width selection.
-   Building height fallback.
-   Mission state transitions.
-   Wanted-level transitions.
-   Vehicle tuning configuration validation.
-   Save schema validation.

## 11.2 Integration tests

Test:

-   Map manifest loads.
-   Chunk assets load.
-   Player spawns at valid coordinates.
-   Physics and rendering transforms remain synchronised.
-   Vehicle entry and exit state transitions.
-   Mission objective transitions.
-   Save and load round trip.

## 11.3 Manual test checklist

Before a milestone is marked complete:

-   Launch in a clean browser session.
-   Confirm no fatal console errors.
-   Confirm expected assets load.
-   Test keyboard input.
-   Test mouse input and pointer lock.
-   Test browser resizing.
-   Test tab switching and focus recovery.
-   Test collision boundaries.
-   Test pause/resume.
-   Check performance in the target scene.
-   Confirm no obvious memory leak during repeated play.

## 11.4 Definition of Done

A feature is complete only when:

1.  Its acceptance criteria pass.
2.  It works in the browser.
3.  It has no known critical defects.
4.  Relevant tests pass.
5.  It has been manually exercised.
6.  Performance is acceptable for its scope.
7.  The code is committed.
8.  Documentation is updated.
9.  A screenshot, recording, or demonstration is captured where
    appropriate.

------------------------------------------------------------------------

# 12. Development Phases and Work Breakdown

The project should be built in the following order. Estimates are rough
solo-development planning ranges and include implementation and
debugging, not guaranteed delivery dates.

## Phase 0: Project foundation

**Estimate:** 8--15 hours

Tasks:

-   Create Vite TypeScript project.
-   Configure strict TypeScript.
-   Install Three.js.
-   Configure linting and formatting.
-   Set up Git and GitHub.
-   Create initial documentation.
-   Create a basic Three.js scene.
-   Add resize handling.
-   Add a basic render loop.
-   Add a debug grid and simple test geometry.
-   Confirm clean browser startup.

Acceptance criteria:

-   Project starts with documented commands.
-   TypeScript build passes.
-   Browser displays a 3D scene.
-   Window resizing works.
-   No fatal console errors.
-   Initial Git commit exists.

## Phase 1: Geographic extraction

**Estimate:** 15--30 hours

Tasks:

-   Decide initial map boundary.
-   Set up Python environment.
-   Install OSMnx and geospatial dependencies.
-   Extract roads.
-   Extract building footprints.
-   Extract parks and water features.
-   Reproject to metric CRS.
-   Define local origin and axis convention.
-   Clean and validate geometries.
-   Export processed datasets.
-   Generate source and licence manifest.
-   Produce a map summary report.

Acceptance criteria:

-   Extraction is repeatable.
-   Road and building outputs exist.
-   Features align in a GIS or debug visualisation.
-   Coordinate conversion is documented and tested.
-   Source attribution is recorded.
-   Missing data is handled without crashing.

## Phase 2: Procedural city environment

**Estimate:** 25--45 hours

Tasks:

-   Load processed map data.
-   Generate road surfaces.
-   Generate building meshes.
-   Add configurable building heights.
-   Add ground and basic terrain.
-   Add river representation.
-   Add basic materials and lighting.
-   Add simple landmark placeholders.
-   Add collision geometry for static world objects.
-   Add a development camera and navigation controls.

Acceptance criteria:

-   Browser displays actual Newcastle road geometry.
-   Buildings appear in the correct geographic locations.
-   Map orientation and scale are correct.
-   Player/test camera can inspect the area.
-   No major geometry gaps or coordinate distortion.
-   Scene is performant enough for continued development.

## Phase 3: World architecture and player

**Estimate:** 25--40 hours

Tasks:

-   Implement core game bootstrap.
-   Implement input manager.
-   Integrate Rapier.
-   Implement fixed-step physics.
-   Add player capsule collider.
-   Add player movement.
-   Add gravity and ground detection.
-   Add third-person camera.
-   Add camera collision.
-   Add basic character model and animation.
-   Add pause and focus handling.

Acceptance criteria:

-   Player can walk around the initial city.
-   Player collides with ground and buildings.
-   Camera behaves predictably.
-   Input does not stick after browser focus changes.
-   Physics remains stable.
-   Pause and resume work.

## Phase 4: Vehicle prototype

**Estimate:** 30--50 hours

Tasks:

-   Create or acquire a properly licensed fictional vehicle asset.
-   Build vehicle configuration.
-   Add physics body and collision.
-   Implement acceleration and braking.
-   Implement steering.
-   Implement reverse.
-   Implement handbrake.
-   Implement vehicle camera.
-   Implement entry/exit interaction.
-   Add speed display.
-   Tune handling.

Acceptance criteria:

-   Player can enter and exit the vehicle.
-   Vehicle drives, brakes, reverses, and steers.
-   Vehicle collides with static environment.
-   Camera follows correctly.
-   No broken player/vehicle control state.
-   Handling is stable and enjoyable enough for a demo.

## Phase 5: City detail and streaming

**Estimate:** 20--40 hours

Tasks:

-   Define chunk manifest.
-   Split city data into chunks.
-   Implement asynchronous chunk loading.
-   Implement safe unloading.
-   Add asset loading progress.
-   Add instancing and geometry merging.
-   Add LODs.
-   Improve road markings and pavements.
-   Add vegetation and street props.
-   Create custom landmark assets.

Acceptance criteria:

-   Player can move through the target area without loading the entire
    expanded map.
-   Chunks load and unload without visible severe errors.
-   No duplicate boundary objects.
-   Memory remains bounded during repeated traversal.
-   Key landmarks are recognisable where included.

## Phase 6: Traffic and pedestrians

**Estimate:** 25--45 hours

Tasks:

-   Build a usable road navigation graph.
-   Implement simple traffic routes.
-   Add a small number of traffic vehicles.
-   Add basic lane/direction handling.
-   Add traffic signal states.
-   Implement pedestrian spawn areas.
-   Add basic pedestrian navigation.
-   Add proximity behaviour.
-   Add pooling and distance limits.

Acceptance criteria:

-   Traffic follows basic routes.
-   Pedestrians move around designated areas.
-   AI entities do not accumulate indefinitely.
-   Density can be configured.
-   Performance remains acceptable.

## Phase 7: Gameplay systems

**Estimate:** 35--60 hours

Tasks:

-   Implement reusable interaction system.
-   Implement mission state machine.
-   Add mission markers.
-   Add objective tracking.
-   Add wanted-level state.
-   Add simple police AI.
-   Add pursuit behaviour.
-   Add reward and progression data.
-   Add save/load for essential progress.

Acceptance criteria:

-   At least one original mission can be completed.
-   Mission failure and completion work.
-   Wanted level changes correctly.
-   Police response can begin and end.
-   Progression can be saved and restored.

## Phase 8: Presentation, polish and public demo

**Estimate:** 25--45 hours

Tasks:

-   Add title/start screen.
-   Add HUD.
-   Add minimap.
-   Add settings menu.
-   Add audio ambience and sound effects.
-   Add day/night cycle.
-   Add selected weather effects.
-   Improve landmark quality.
-   Optimise target scenes.
-   Add loading/error states.
-   Deploy public demo.
-   Add feedback and issue-reporting route.
-   Capture launch media.

Acceptance criteria:

-   Public URL loads the game.
-   New player can understand how to start.
-   Main gameplay loop works.
-   Performance settings work.
-   No known critical defects.
-   Asset and data attribution is present.
-   Feedback route is available.

## Overall planning estimate

  Scope                                               Estimated hours
  ---------------------------------------------- --------------------
  First playable Newcastle prototype                          70--120
  Living city and expanded environment              Additional 45--85
  Full gameplay systems and public-demo polish     Additional 85--150
  **Total indicative range**                       **200--355 hours**

Actual time depends heavily on asset quality, map complexity, debugging,
browser performance, and how much custom modelling is required. Treat
the estimates as planning ranges, not promises.

------------------------------------------------------------------------

# 13. Weekly Project Management

The project owner and AI coding assistant should maintain a weekly
progress log.

## 13.1 Weekly cadence

At the start of each week:

1.  Review the previous week's goals.
2.  Check the current Git branch and latest commit.
3.  Run the project and relevant tests.
4.  Identify incomplete work and blockers.
5.  Select a small set of achievable tasks.
6.  Define measurable acceptance criteria.
7.  Avoid adding unrelated features mid-week.

At the end of each week:

1.  Run tests and build.
2.  Manually playtest.
3.  Record completed tasks.
4.  Record incomplete tasks and reasons.
5.  Record bugs and technical debt.
6.  Capture a screenshot or video.
7.  Commit stable work.
8.  Update the weekly report.
9.  Select next week's priorities.

## 13.2 Weekly status template

Create a new file each week:

`docs/weekly-reports/week-01.md`

Use this template:

``` markdown
# Week 01 Progress Report

## Dates
Start:
End:

## Weekly objective

## Planned tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Completed tasks
- 

## Incomplete tasks
- 

## Tests and validation
- Build:
- Unit tests:
- Browser test:
- Manual playtest:

## Demonstration
Screenshot/video:
Commit:

## Bugs and blockers
- 

## Technical decisions
- 

## Time spent
Planned:
Actual:

## Lessons learned

## Next week's objectives
1.
2.
3.

## Overall project status
Not started / In progress / Blocked / Complete
```

## 13.3 Project status definitions

-   **Not started:** no implementation work yet.
-   **In progress:** implementation underway.
-   **Blocked:** cannot proceed without resolving a dependency or issue.
-   **Complete:** acceptance criteria satisfied and validated.

Do not mark a feature complete simply because code has been generated.

## 13.4 Weekly project dashboard

Maintain `docs/PROJECT_STATUS.md` containing:

-   Current release.
-   Current phase.
-   Current week.
-   Completed milestones.
-   In-progress tasks.
-   Blockers.
-   Known critical bugs.
-   Latest stable commit.
-   Latest playable demo URL.
-   Total hours invested.
-   Next milestone.

This file should be updated at the end of each weekly review.

------------------------------------------------------------------------

# 14. Git and Development Workflow

## 14.1 Branching

Use:

-   `main` for stable, playable work.
-   `feature/<short-description>` for feature work.
-   `fix/<short-description>` for bug fixes.

Merge only after the relevant checks pass.

## 14.2 Commit conventions

Examples:

``` text
feat: add procedural road geometry
feat: implement third-person player movement
feat: add vehicle entry and exit
fix: correct local coordinate conversion
fix: prevent player falling through terrain
perf: instance repeated building materials
docs: add week 01 progress report
test: add coordinate conversion tests
```

## 14.3 Development commands

Document and maintain these scripts in `package.json` as the project
evolves:

``` bash
npm install
npm run dev
npm run build
npm run preview
npm run test
```

Do not claim a command exists until it has been added and verified.

Python pipeline commands should also be documented in
`scripts/map-pipeline/README.md`.

------------------------------------------------------------------------

# 15. Claude Code Working Instructions

This section is intended to guide Claude Code when this specification is
supplied as project context.

## 15.1 General operating rules

1.  Read `SPEC.md` and `CLAUDE.md` before making changes.
2.  Inspect the existing repository before creating or modifying files.
3.  Do not overwrite existing working code without understanding it.
4.  Implement one coherent task at a time.
5.  Do not attempt to implement the entire game in one response.
6.  Explain the planned change before substantial implementation.
7.  Prefer small, maintainable modules.
8.  Use strict TypeScript and meaningful types.
9.  Avoid `any` unless there is a documented reason.
10. Do not introduce dependencies without explaining why they are
    needed.
11. Do not silently change the architecture.
12. Do not use copyrighted game assets or unlicensed content.
13. Keep configuration separate from game logic.
14. Add tests for important pure logic.
15. Run the relevant tests and build after changes.
16. Report exactly what was tested and what was not tested.
17. Update documentation when architecture, commands, or workflows
    change.
18. Do not mark a task complete if it has not been verified.
19. If a requirement is ambiguous, state the assumption and ask for
    clarification when the decision materially affects architecture or
    product direction.
20. Prefer a working, small implementation over an elaborate untested
    abstraction.

## 15.2 Task execution format

For each task, Claude Code should report:

``` text
TASK
What is being implemented?

PLAN
Which files will change and why?

IMPLEMENTATION
What was created or modified?

VALIDATION
Which commands were run?
Which tests passed?
Was it checked in a browser?

RESULT
What works now?

LIMITATIONS
What remains incomplete?

NEXT STEP
What is the smallest sensible next task?
```

## 15.3 Scope control

If a task belongs to a future phase, do not implement it early unless it
is necessary for the current milestone.

For example:

-   Do not build police AI before player movement works.
-   Do not build missions before interaction handling exists.
-   Do not build large traffic simulations before the road graph is
    validated.
-   Do not add a backend merely to store local configuration.
-   Do not build a complex asset streaming system before profiling
    demonstrates a need.

## 15.4 Architecture decision records

For important architectural decisions, create a short record in:

`docs/decisions/`

Each record should include:

-   Context.
-   Decision.
-   Alternatives considered.
-   Trade-offs.
-   Consequences.
-   Date.

Examples:

-   Why Three.js rather than a different browser engine.
-   Why the chosen coordinate reference system.
-   How map chunks are represented.
-   Which vehicle physics approach is used.
-   How save data is stored.

------------------------------------------------------------------------

# 16. Initial Week-by-Week Schedule

This is an initial planning schedule at approximately 10--15 development
hours per week. Adjust based on actual velocity.

  -----------------------------------------------------------------------
  Week                    Focus                   Expected outcome
  ----------------------- ----------------------- -----------------------
  1                       Repository and 3D       Browser renders a basic
                          foundation              Three.js scene

  2                       Python and OSM          Newcastle roads and
                          extraction              building data extracted

  3                       Coordinate conversion   Correctly projected map
                          and validation          data

  4                       Road geometry           Actual Newcastle roads
                                                  rendered

  5                       Building generation     Procedural buildings
                                                  visible

  6                       Environment and         More recognisable city
                          landmarks               block

  7                       Physics and player      Character can walk and
                          controller              collide

  8                       Camera and player       Stable third-person
                          polish                  exploration

  9                       Vehicle model and       First drivable vehicle
                          physics                 

  10                      Vehicle interaction     Entering and exiting
                                                  works

  11                      Map chunking and        Larger environment
                          optimisation            loads more efficiently

  12                      First playable release  Demonstrable Newcastle
                                                  exploration and driving
                                                  prototype

  13--15                  Traffic and pedestrians Basic living city

  16--18                  Interactions and        First mission loop
                          missions                

  19--21                  Police and wanted       Basic pursuit gameplay
                          system                  

  22--24                  UI, audio, polish and   Public demo candidate
                          deployment              
  -----------------------------------------------------------------------

The schedule is a guide. Do not rush a phase just to match a calendar
date. If a foundational system is unstable, fix it before expanding
scope.

------------------------------------------------------------------------

# 17. First Sprint: Exact Tasks

The first sprint should be small enough to finish and validate.

## Sprint 1 objective

Create a clean browser-based Three.js project with a functioning 3D
scene and a documented development workflow.

### Tasks

-   [ ] Create Vite vanilla TypeScript project.
-   [ ] Install Three.js and TypeScript types.
-   [ ] Configure strict TypeScript.
-   [ ] Create the scene.
-   [ ] Add perspective camera.
-   [ ] Add renderer and lighting.
-   [ ] Add ground plane.
-   [ ] Add temporary buildings.
-   [ ] Add a grid/debug helper.
-   [ ] Add responsive resize handling.
-   [ ] Add a stable animation loop.
-   [ ] Add basic error logging.
-   [ ] Add Git repository and initial commit.
-   [ ] Write setup instructions.
-   [ ] Capture a screenshot of the scene.

### Sprint 1 acceptance criteria

-   `npm install` completes.
-   `npm run dev` starts the application.
-   The browser displays a 3D environment.
-   Resizing the browser does not distort the camera.
-   The console has no fatal errors.
-   `npm run build` succeeds.
-   The repository contains setup instructions and a committed baseline.

### Sprint 1 is not complete if

-   Only source code has been generated but not run.
-   The build fails.
-   The browser displays a blank page.
-   The scene breaks on resize.
-   The work is not committed.

------------------------------------------------------------------------

# 18. Open Questions for the Project Owner

These questions should be resolved progressively. The recommended
defaults are provided so implementation can begin without blocking on
every decision.

  -----------------------------------------------------------------------
  Question                Recommended default     Priority
  ----------------------- ----------------------- -----------------------
  Development OS?         Windows, if that is the High
                          available machine       

  Public or private       Public, if comfortable  Medium
  source repository?                              

  Initial map boundary?   Newcastle city centre,  High
                          Quayside and Tyne       
                          Bridge                  

  Exact visual reference? Semi-realistic,         Medium
                          slightly simplified     
                          city graphics           

  Camera?                 Third-person            High

  Input?                  Keyboard and mouse      High

  Controller support?     Later                   Low

  Multiplayer?            No                      High

  Initial game narrative? Free exploration first  Medium

  Vehicle style?          Fictional, unbranded    Medium
                          vehicles                

  Backend?                None for first playable High
                          version                 

  Hosting?                Cloudflare Pages or     Medium
                          Vercel                  

  Domain?                 Decide later            Low

  Mobile support?         Not initially           High

  Public launch target?   Early playable browser  Medium
                          demo                    
  -----------------------------------------------------------------------

## Questions requiring an explicit answer

1.  What operating system and hardware will be used for development?
2.  Should the first playable area include Gateshead across the river,
    or should we focus on Newcastle first?
3.  Do you want the world to be geographically close to real-world
    scale, or would you prefer a slightly compressed map to make
    gameplay faster?
4.  Should the player character be an original fictional character with
    a defined identity, or a generic player avatar initially?
5.  Should the game be completely free to play, with no accounts or
    payments in the initial release?

These decisions can be answered in the project documentation as they
become relevant. They must not block Sprint 1 unless they affect a
specific implementation decision.

------------------------------------------------------------------------

# 19. Success Criteria

The project should be evaluated on more than the number of implemented
features.

## Technical success

-   Reproducible map extraction.
-   Correct geographic alignment.
-   Modular game architecture.
-   Stable physics.
-   Browser performance.
-   Maintainable TypeScript.
-   Repeatable builds and deployment.

## Gameplay success

-   The player can explore the environment.
-   Walking and driving feel responsive.
-   The map is recognisably Newcastle.
-   The city feels coherent rather than procedurally random.
-   At least one engaging gameplay loop exists.

## Portfolio and community success

-   Public project repository, if approved.
-   Regular development updates.
-   Technical write-ups.
-   Short demonstration videos.
-   A playable public demo.
-   Clear documentation of engineering decisions.

Social reach is not guaranteed. The project should remain technically
and creatively valuable even if individual posts do not perform well.

------------------------------------------------------------------------

# 20. Immediate Instructions to Claude Code

Start by reading this document and inspecting the repository.

Do not implement the full game immediately.

Your first assignment is **Sprint 1: Project Foundation**.

1.  Check the available Node.js and package-manager versions.
2.  Inspect the repository and current files.
3.  Identify any missing environment requirements.
4.  Propose the smallest setup plan.
5.  Create the Vite TypeScript application if one does not already
    exist.
6.  Install and configure Three.js.
7.  Implement the initial 3D scene.
8.  Add responsive resizing and a clean animation loop.
9.  Add or update the README with exact setup commands.
10. Run the production build.
11. Report the files changed, commands executed, and validation results.
12. Do not begin geographic extraction until Sprint 1 passes.

If the repository already contains code, preserve it unless a change is
necessary and explained.

The project owner is responsible for running the application locally and
confirming the browser demonstration. Never claim visual verification
unless it has actually been performed.

**The first deliverable is a working 3D scene in the browser, not a
large collection of generated files.**

------------------------------------------------------------------------

# Appendix A: Useful Official Documentation

Use current official documentation when implementing. APIs can change,
so verify signatures against installed versions.

-   Three.js: https://threejs.org/docs/
-   Three.js installation: https://threejs.org/manual/#en/installation
-   TypeScript: https://www.typescriptlang.org/docs/
-   Vite: https://vite.dev/guide/
-   Rapier JavaScript: https://rapier.rs/docs/
-   OSMnx: https://osmnx.readthedocs.io/
-   OpenStreetMap copyright and licence:
    https://www.openstreetmap.org/copyright
-   GeoPandas: https://geopandas.org/en/stable/
-   Shapely: https://shapely.readthedocs.io/
-   Blender manual: https://docs.blender.org/manual/en/latest/
-   glTF: https://www.khronos.org/gltf/

------------------------------------------------------------------------

# Appendix B: Weekly Review Prompt

Use this prompt at the end of every development week:

> Review the current TYNE CITY repository against SPEC.md and the
> previous weekly report.
>
> Inspect the code and Git history. Run the relevant build and tests. Do
> not infer completion from the existence of source files.
>
> Produce a weekly report containing:
>
> 1.  Planned tasks versus completed tasks.
> 2.  Features demonstrably working.
> 3.  Tests and validation results.
> 4.  Bugs and blockers.
> 5.  Technical debt and architectural concerns.
> 6.  Estimated effort spent, clearly labelled as an estimate if not
>     measured.
> 7.  Screenshots or recordings available.
> 8.  Recommended priorities for next week.
>
> Update `docs/PROJECT_STATUS.md` and create
> `docs/weekly-reports/week-XX.md`.
>
> Do not modify unrelated code during the review. Do not mark work
> complete without evidence.

------------------------------------------------------------------------

**End of specification.**
