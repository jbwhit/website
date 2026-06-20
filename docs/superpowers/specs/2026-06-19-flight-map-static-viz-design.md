# Static Flight-Map Visualization — Design

**Status:** Approved design, pending spec review
**Date:** 2026-06-19
**Author:** Jonathan Whitmore (with Claude)
**Trigger:** The 2014 blog post "One chapter closes; a new chapter opens" embedded a D3 flight map hosted on bl.ocks.org (now shut down). Rather than restore the dead post, Jonathan wants to *modernize that kind of visualization* as a standalone, durable artifact driven by his full flight log.

---

## Goal

Produce a **static, dark-themed SVG world map** of every flight Jonathan has taken, rendered from his personal flight log by a small, reproducible Python/uv pipeline. "Static" is a deliberate choice: the original died because it depended on client-side JS and a third-party host. A pre-rendered SVG never rots and embeds anywhere.

The deliverable is the **artifact and its pipeline**, not its placement. Where the SVG ultimately lives (a blog post, a project page) is decided later.

## Decisions locked during brainstorming

- **Goal:** the visualization artifact itself, not a finished post. Restoring the 2014 post is explicitly someday-maybe.
- **Experience:** static, no interactivity, no animation, no client-side JS — a single rendered SVG.
- **Data:** Jonathan supplies the real data (already provided: `data/flight-log.csv`, a Google Sheets export — 346 flights, 69 airports, 2005–2026). The viz is data-driven.
- **Look:** "B — Dark / Gruvbox": glowing semi-transparent arcs on deep slate, matching the site's dark theme. Chosen from a live three-way preview rendered with the real data.
- **Privacy / publish model:** the raw log contains booking PNRs (`record_locator`) and `seat` numbers and must never enter this **public** repo. The repo commits only **minimal safe geometry** (airports + coordinates + ordered legs — no dates, PNRs, or seats). CI/anyone can rebuild the map from that safe file.
- **Render toolchain:** Python + uv (`pyproj` + `shapely` + `matplotlib`), honoring the global uv-first toolchain rule and keeping a single runtime. (Node/d3 considered for pixel-fidelity but rejected to avoid a second runtime; inline Quarto OJS rejected because it re-introduces client-side JS + CDN fragility, defeating "static".)
- **SVG handling:** commit the rendered SVG directly to `assets/images/flights/flights-map.svg` (the site's established media dir) for now. Wiring a Quarto pre-render/CI step is deferred until the map is placed in a page.

## Architecture

Two stages, separated by **what data they touch** (this is the core privacy boundary):

### Stage 1 — Prep (local only; touches the private log)
`data/flight-log.csv` → `data/flights.geo.json`

- Reads the raw log (gitignored), extracts `departing_airport` / `arriving_airport` per row, in file order.
- Joins each IATA code to coordinates from the public **OurAirports** dataset (`https://davidmegginson.github.io/ourairports-data/airports.csv`), fetched at prep time (local only — never in CI).
- Applies `scripts/flights/airport_overrides.json` for codes OurAirports lacks (e.g. `TXL`, Berlin Tegel — closed 2020, dropped from the dataset).
- **Errors loudly** if any code remains unresolved after overrides, so a newly added airport can never silently disappear from the map.
- Writes `data/flights.geo.json` containing **only** airports+coords and ordered legs — no dates, PNRs, or seats.

Run locally whenever the log changes. The OurAirports join happens here (occasional, local), so coordinates are baked into the committed JSON and the render stage needs no network.

### Stage 2 — Render (anywhere, incl. CI; touches only safe data)
`data/flights.geo.json` → `assets/images/flights/flights-map.svg`

- Reads the safe geometry plus the vendored `scripts/flights/land-110m.geojson`.
- Projects with PROJ Natural Earth, Pacific-centered.
- Draws sphere/ocean, graticule, land, boundaries, then great-circle arcs, then airport dots.
- Writes a single deterministic SVG.

## File layout

```
data/flight-log.csv          # private raw log — gitignored (already in place)
data/flights.geo.json        # SAFE, committed — the rebuildable source of truth
assets/images/flights/
  flights-map.svg            # committed rendered artifact
scripts/flights/
  prepare_data.py            # Stage 1: CSV -> flights.geo.json   (stdlib + urllib fetch)
  render_map.py              # Stage 2: flights.geo.json -> SVG    (pyproj, shapely, matplotlib)
  airport_overrides.json     # manual coords for codes OurAirports lacks
  land-110m.geojson          # vendored Natural Earth 110m land/countries (committed)
```

Each script is a standalone `uv run` entry point with PEP 723 inline dependency metadata, so `uv run scripts/flights/<script>.py` self-installs deps. No shared package, no `__init__.py` — two focused scripts.

## Data formats

`data/flights.geo.json` (safe — the only flight data that becomes public):
```json
{
  "airports": { "DFW": [-97.0380, 32.8968], "MEL": [144.8433, -37.6733] },
  "legs": [ ["BNA","DFW"], ["DFW","SAN"] ]
}
```
- `airports`: IATA code → `[longitude, latitude]` (GeoJSON order).
- `legs`: ordered array of `[departing, arriving]` code pairs. Order is retained (harmless; lets a future animation reuse the file) but the static render ignores it. Duplicate corridors are kept, not deduped — overlapping arcs are what produce the glow.

`scripts/flights/airport_overrides.json`:
```json
{ "TXL": [13.2877, 52.5597] }
```

## Render details

- **Projection:** `+proj=natearth +lon_0=150` (Pacific-centered, so trans-Pacific corridors sit in the middle, not the edges). Coordinates and land geometry reprojected via `pyproj.Transformer`.
- **Land:** read the vendored 110m GeoJSON with stdlib `json`, build `shapely` geometries, reproject, draw as matplotlib paths. (No `geopandas` dependency — keeps the stack small.)
- **Great-circle arcs:** densify each leg with `pyproj.Geod(ellps="WGS84").npts(...)` (~48 intermediate points), reproject, draw as thin semi-transparent polylines. **Antimeridian handling:** split any arc whose successive points jump across the ±180° seam (relative to `lon_0`) into separate path segments, so trans-Pacific legs don't smear a horizontal line across the whole map. This is the one fiddly rendering case and must be explicitly handled and tested.
- **Palette (B — Dark/Gruvbox), exact values from the approved preview:**
  | Element | Color | Notes |
  |---|---|---|
  | background / ocean | `#1d2021` | baked into the SVG |
  | land | `#32302f` | |
  | boundaries | `#3c3836` | ~0.4 width |
  | graticule | `#262626` | ~0.4 width, subtle |
  | arcs | `#83a598` | ~0.34 alpha, ~0.65 width, round caps |
  | airport dots | `#fe8019` | r ≈ 1.3 |
- **Canvas:** single SVG, ~1.6:1 aspect, no axes/ticks/margins, dark background filling the frame.
- **Determinism:** render must be byte-stable across runs (fixed/stripped SVG metadata, no embedded timestamps, e.g. set `svg.hashsalt` and disable date metadata; `svg.fonttype = 'none'`). CI diffs and re-renders should be no-ops when inputs are unchanged.

## Verification

1. `uv run scripts/flights/prepare_data.py` regenerates `data/flights.geo.json` from the sample log with no errors; all 69 current codes resolve (68 via OurAirports + `TXL` via override).
2. The generated `flights.geo.json` contains **no** `record_locator`, `seat`, `date`, `flight_number`, or free-text `notes` — assert on absence of those keys/values.
3. A deliberately-unknown airport code in the log causes prep to **exit non-zero** with a clear message (no silent drop).
4. `uv run scripts/flights/render_map.py` produces a valid SVG that opens and matches preview B on visual spot-check (dark ground; Bay-Area SAN/SFO/SJC and DFW corridors visibly brightest).
5. At least one trans-Pacific leg (e.g. SYD↔LAX) renders as a clean arc, not a horizontal smear (antimeridian split works).
6. Running render twice yields byte-identical SVG output (determinism).
7. `git status` / `git check-ignore data/flight-log.csv` confirm the raw log stays ignored; only `flights.geo.json`, the SVG, the scripts, the overrides, and the vendored GeoJSON are tracked.

## Out of scope (explicit)

- **Placement / embedding.** Which page or post the SVG appears in, and any surrounding prose, is a later task.
- **CI / Quarto pre-render wiring.** Deferred until placement; for now the SVG is committed directly.
- **Light-theme variant, interactivity, animation, tooltips, 3D globe.** All deliberately excluded — the choice was a single static dark map.
- **Restoring the 2014 post** (`posts/2014-08-01-a-chapter-closes-a-chapter-opens/index.qmd`). Independent someday-maybe task.
- **Editing the flight data content.** Jonathan owns the log; the pipeline consumes whatever it contains.
