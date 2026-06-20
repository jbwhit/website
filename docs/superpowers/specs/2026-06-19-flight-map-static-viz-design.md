# Static Flight-Map Visualization — Design

**Status:** Approved design, pending spec review
**Date:** 2026-06-19
**Author:** Jonathan Whitmore (with Claude)
**Trigger:** The 2014 blog post "One chapter closes; a new chapter opens" embedded a D3 flight map hosted on bl.ocks.org (now shut down). Rather than restore the dead post, Jonathan wants to *modernize that kind of visualization* as a standalone, durable artifact driven by his full flight log.

**Review provenance:** Codex xhigh, 2+ rounds.
- *Round 1 — NOT SOUND:* (a) the antimeridian seam for `+lon_0=150` is at −30° (mid-Atlantic), not ±180°, and must be handled for land as well as arcs; (b) ordered legs publish chronology even without date fields; (c) the vendored "land" layer can't yield country boundaries; (d) SVG determinism requires pinned deps + stripped metadata + sorted JSON. Verified against the data: 346 flights / 69 airports is correct (the 444 figure includes 98 trailing blank rows); real Atlantic-crossing legs (SFO–CPH, SFO–AMS, SFO–ZRH) confirm the −30° seam matters.
- *Round 2 — NOT SOUND:* (a) render-detail/file-layout contradiction that double-rotated the pre-rotated land; (b) determinism needs full-resolution locking (`uv lock --script`) + `requires-python`, not just direct pins; (c) graticule must be built in the rotated frame or it re-introduces a seam jump. Privacy contract and the `α_eff = 1−(1−α_base)^count` compositing confirmed sound. All folded into this revision.

---

## Goal

Produce a **static, dark-themed SVG world map** of every flight Jonathan has taken, rendered from his personal flight log by a small, reproducible Python/uv pipeline. "Static" is a deliberate choice: the original died because it depended on client-side JS and a third-party host. A pre-rendered SVG never rots and embeds anywhere.

The deliverable is the **artifact and its pipeline**, not its placement. Where the SVG ultimately lives (a blog post, a project page) is decided later.

## Decisions locked during brainstorming

- **Goal:** the visualization artifact itself, not a finished post. Restoring the 2014 post is explicitly someday-maybe.
- **Experience:** static, no interactivity, no animation, no client-side JS — a single rendered SVG.
- **Data:** Jonathan supplies the real data (already provided: `data/flight-log.csv`, a Google Sheets export — **346 flights, 69 airports, 2005–2026**; the export also carries 98 trailing blank rows, which prep ignores).
- **Look:** "B — Dark / Gruvbox": glowing semi-transparent arcs on deep slate, matching the site's dark theme. Chosen from a live three-way preview rendered with the real data.
- **Privacy / publish model:** the raw log contains booking PNRs (`record_locator`) and `seat` numbers and must never enter this **public** repo. The repo commits only **minimal safe geometry**: airports + coordinates and **undirected corridor counts** (e.g. `SAN–SFO ×86`) — **no dates, no chronology, no PNRs, no seats**. Counts (not an ordered leg list) are committed precisely so the public file leaks no sequence/timeline; CI/anyone can rebuild the map from it.
- **Render toolchain:** Python + uv (`pyproj` + `shapely` + `matplotlib`), honoring the global uv-first toolchain rule and keeping a single runtime. (Node/d3 considered for pixel-fidelity but rejected to avoid a second runtime; inline Quarto OJS rejected because it re-introduces client-side JS + CDN fragility, defeating "static".) **Accepted cost:** d3-geo would handle antimeridian clipping of both geometry and arcs for free; in the Python stack we take that on ourselves — hence the rotated-frame + pre-cut-land + arc-split design below. The one-time `prepare_land.py` confines the polygon-cutting complexity to a local prep step, leaving the render simple.
- **SVG handling:** commit the rendered SVG directly to `assets/images/flights/flights-map.svg` (the site's established media dir) for now. Wiring a Quarto pre-render/CI step is deferred until the map is placed in a page.

## Architecture

Two stages, separated by **what data they touch** (this is the core privacy boundary):

### Stage 1 — Prep (local only; touches the private log)
`data/flight-log.csv` → `data/flights.geo.json`

- Reads the raw log (gitignored), takes `departing_airport` / `arriving_airport` from each non-blank row.
- Joins each IATA code to coordinates from the public **OurAirports** dataset (`https://davidmegginson.github.io/ourairports-data/airports.csv`), fetched at prep time (local only — never in CI). OurAirports is a floating, daily-updated source; that is acceptable because the committed `flights.geo.json` (not the live fetch) is the reproducible source of truth for rendering — coordinates only ever change on an explicit re-prep.
- Applies `scripts/flights/airport_overrides.json` for codes OurAirports lacks (e.g. `TXL`, Berlin Tegel — closed 2020, dropped from the dataset).
- **Errors loudly** if any code remains unresolved after overrides, so a newly added airport can never silently disappear from the map.
- Collapses legs into **undirected corridors with counts** (`A–B` and `B–A` are the same corridor; the great-circle geometry is identical either way), then writes `data/flights.geo.json` containing **only** airports+coords and `routes` (sorted endpoint pair + count). No dates, order, PNRs, or seats.

Run locally whenever the log changes. The OurAirports join happens here (occasional, local), so coordinates are baked into the committed JSON and the render stage needs no network.

### Stage 2 — Render (anywhere, incl. CI; touches only safe data)
`data/flights.geo.json` → `assets/images/flights/flights-map.svg`

- Reads the safe geometry plus the vendored, pre-cut `scripts/flights/ne-110m-land.geojson` and `scripts/flights/ne-110m-boundaries.geojson` (see File layout — both produced once by `prepare_land.py`).
- Works in a **rotated longitude frame** (subtract `lon_0=150` so the map centre is 0° and the seam is the standard ±180° antimeridian), then projects with `+proj=natearth +lon_0=0`.
- Draws sphere/ocean, graticule, land fill, country boundaries, then great-circle arcs (corridors), then airport dots.
- Writes a single deterministic SVG.

## File layout

```
data/flight-log.csv          # private raw log — gitignored (already in place)
data/flights.geo.json        # SAFE, committed — the rebuildable source of truth
assets/images/flights/
  flights-map.svg            # committed rendered artifact
scripts/flights/
  prepare_data.py            # Stage 1: CSV -> flights.geo.json    (stdlib + urllib fetch)
  render_map.py              # Stage 2: flights.geo.json -> SVG     (pyproj, shapely, matplotlib)
  prepare_land.py            # one-time, local: NE admin-0 -> rotated, antimeridian-cut, Antarctica-trimmed land + boundaries
  render_map.py.lock         # uv lock --script (full pinned resolution, committed)
  prepare_land.py.lock       # uv lock --script (committed)
  airport_overrides.json     # manual coords for codes OurAirports lacks
  ne-110m-land.geojson       # vendored land fill   — pre-cut & pre-rotated for lon_0=150 (committed)
  ne-110m-boundaries.geojson # vendored country borders — pre-cut & pre-rotated for lon_0=150 (committed)
```

Each script is a standalone `uv run` entry point with PEP 723 inline dependency metadata, so `uv run scripts/flights/<script>.py` self-installs deps. No shared package, no `__init__.py`.

`prepare_land.py` runs **once** (local): it fetches Natural Earth 110m **admin-0 countries** (the layer that yields both a land fill via union and internal country borders via boundary lines), rotates longitudes by −`lon_0`, cuts geometries at the ±180° antimeridian (using the `antimeridian` package), trims to latitudes ≈ [−58°, 84°] to drop Antarctica and the polar fringe, and writes the two vendored GeoJSON files. Because `lon_0` is locked at 150, these committed files are pre-rotated and seam-clean, so `render_map.py` only has to project and draw — no polygon seam-cutting at render time.

## Data formats

`data/flights.geo.json` (safe — the only flight data that becomes public):
```json
{
  "airports": { "DFW": [-97.0380, 32.8968], "MEL": [144.8433, -37.6733] },
  "routes": [ ["SAN","SFO",86], ["LAX","MEL",12] ]
}
```
- `airports`: IATA code → `[longitude, latitude]` (GeoJSON order). Sorted by key for deterministic output.
- `routes`: array of `[endpoint_a, endpoint_b, count]`. **Undirected** (endpoints sorted alphabetically so A–B and B–A merge); `count` is total flights on that corridor. Sorted by endpoint pair for deterministic output. No order, no dates — the count alone drives arc intensity (see render). This is the entire public flight footprint.

`scripts/flights/airport_overrides.json`:
```json
{ "TXL": [13.2877, 52.5597] }
```

## Render details

- **Projection / centering:** the Pacific centre (`lon_0=150`) is achieved by **rotating longitudes** (`lon' = wrap(lon − 150)` into [−180, 180)) and then projecting with `+proj=natearth +lon_0=0` via `pyproj.Transformer`. This moves the map seam to the standard ±180° antimeridian, which is where land was pre-cut (`prepare_land.py`) and where arc-splitting is checked — keeping render-time seam logic uniform and correct. (Note: with this centring the seam sits at original longitude −30°, mid-Atlantic — which Jonathan's Atlantic legs such as SFO–CPH cross, so seam handling is mandatory, not cosmetic.)
- **What gets rotated, and what doesn't (avoid double-rotation):** the vendored land/boundary GeoJSONs are **already in rotated-longitude space** (`prepare_land.py` baked the `−lon_0` rotation in), so at render time they are **only projected**, never rotated again. The **graticule** is likewise built directly in the rotated frame (see below) and only projected. The one thing that arrives in **true** longitudes is the **flight coordinates** — those are rotated (`−lon_0`) and then projected. Mixing these up (rotating already-rotated geometry, or skipping rotation on flight coords) shifts the map — keep them distinct.
- **Land + boundaries:** read the two vendored pre-cut GeoJSONs with stdlib `json`, build `shapely` geometries, **project only** (no rotation), draw with matplotlib — land as filled paths, boundaries as thin lines. Already seam-cut and Antarctica-trimmed, so no render-time polygon surgery. (No `geopandas` dependency — keeps the stack small.)
- **Graticule:** generate meridians/parallels directly in the **rotated** frame (longitudes spanning [−180, 180) around the centre) so no line straddles the seam; project and draw. (Equivalently, apply the same projected-x discontinuity split as arcs.) Do not feed original-longitude graticule lines through the rotation, or a seam jump reappears.
- **Great-circle arcs (corridors):** for each `route`, densify the endpoint pair with `pyproj.Geod(ellps="WGS84").npts(...)` (~48 points), rotate (`−lon_0`) then project, and draw as a thin semi-transparent polyline. **Antimeridian split:** break the polyline wherever consecutive projected-x values jump by more than half the map width (a generic seam-crossing test), emitting separate sub-paths so a seam-crossing arc never smears horizontally.
- **Intensity from counts (deterministic, order-free):** the approved preview's glow came from N identical arcs stacking. Reproduce it exactly by drawing each corridor **once** with composited alpha `α_eff = 1 − (1 − α_base)^count` (`α_base ≈ 0.34`). This is mathematically identical to overlaying `count` strokes but is deterministic and needs no leg ordering.
- **Palette (B — Dark/Gruvbox), exact values from the approved preview:**
  | Element | Color | Notes |
  |---|---|---|
  | background / ocean | `#1d2021` | baked into the SVG |
  | land | `#32302f` | |
  | boundaries | `#3c3836` | ~0.4 width |
  | graticule | `#262626` | ~0.4 width, subtle |
  | arcs | `#83a598` | `α_base` ≈ 0.34 (composited by count), ~0.65 width, round caps |
  | airport dots | `#fe8019` | r ≈ 1.3 |
- **Canvas:** single SVG, ~1.6:1 aspect, no axes/ticks/margins, dark background filling the frame.
- **Determinism:** render must be byte-stable across runs given fixed inputs. Required measures:
  - **Lock the full dependency resolution, not just direct pins.** Pin direct deps and `requires-python` in the PEP 723 metadata, and commit a per-script lockfile via `uv lock --script scripts/flights/render_map.py` (and likewise for `prepare_land.py`); run with `uv run --locked`. Direct-only pins leave transitive deps and the Python version floating, which can perturb SVG bytes.
  - **Matplotlib:** set `mpl.rcParams["svg.hashsalt"]` to a fixed string, `svg.fonttype = "none"`, and pass `metadata={"Date": None}` to `savefig` so no timestamp/UUID is embedded.
  - **Ordering:** iterate `airports`/`routes` in the file's already-sorted order.
  - Re-rendering unchanged inputs must produce a **byte-identical** SVG (verification #7).

## Verification

1. `uv run scripts/flights/prepare_data.py` regenerates `data/flights.geo.json` from the sample log with no errors; all 69 current codes resolve (68 via OurAirports + `TXL` via override).
2. The generated `flights.geo.json` has exactly two top-level keys (`airports`, `routes`) and contains **no** `record_locator`, `seat`, `date`, `flight_number`, `notes`, or any ordered leg list — assert structurally. `routes` entries are `[a, b, count]` with `a < b`.
3. A deliberately-unknown airport code in the log causes prep to **exit non-zero** with a clear message (no silent drop).
4. `uv run scripts/flights/render_map.py` produces a valid SVG that opens and matches preview B on visual spot-check (dark ground; Bay-Area SAN/SFO/SJC and DFW corridors visibly brightest).
5. **Seam check:** a known Atlantic-crossing corridor (e.g. SFO–CPH) and a trans-Pacific one (e.g. LAX–MEL) both render as clean arcs, not horizontal smears across the map.
6. **Land seam check:** no land polygon smears across the map; Antarctica is absent (latitude trim).
7. Running render twice yields **byte-identical** SVG output (determinism).
8. `git check-ignore data/flight-log.csv` confirms the raw log stays ignored; tracked artifacts are only `flights.geo.json`, the SVG, the three scripts, their two `*.py.lock` lockfiles, the overrides, and the two vendored GeoJSONs.

## Out of scope (explicit)

- **Placement / embedding.** Which page or post the SVG appears in, and any surrounding prose, is a later task.
- **CI / Quarto pre-render wiring.** Deferred until placement; for now the SVG is committed directly.
- **Light-theme variant, interactivity, animation, tooltips, 3D globe.** All deliberately excluded — the choice was a single static dark map.
- **Restoring the 2014 post** (`posts/2014-08-01-a-chapter-closes-a-chapter-opens/index.qmd`). Independent someday-maybe task.
- **Editing the flight data content.** Jonathan owns the log; the pipeline consumes whatever it contains.
