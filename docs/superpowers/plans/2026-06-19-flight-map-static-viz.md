# Static Flight-Map Visualization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python/uv pipeline that turns a private flight log into a committed, deterministic dark-themed static SVG world map of all flights.

**Architecture:** Three standalone `uv run` scripts. `prepare_data.py` (local) reads the private CSV, joins airport coordinates, and writes a safe `flights.geo.json` (airports + undirected corridor counts — no dates/PNR/seat). `prepare_land.py` (one-time, local) vendors pre-rotated, antimeridian-cut, Antarctica-trimmed land + boundary GeoJSONs. `render_map.py` (anywhere) reads the safe JSON + vendored land and renders one byte-stable SVG via pyproj + matplotlib, working in a rotated-longitude frame so the Pacific-centered Natural Earth map has no seam smears.

**Tech Stack:** Python 3.12 via uv (PEP 723 inline deps + `uv lock --script`), pytest, pyproj, shapely, matplotlib, the `antimeridian` package. Full design: `docs/superpowers/specs/2026-06-19-flight-map-static-viz-design.md`.

---

## File Structure

```
data/flight-log.csv                     # private raw log (gitignored, already present)
data/flights.geo.json                   # OUTPUT of prepare_data — safe, committed
assets/images/flights/flights-map.svg   # OUTPUT of render_map — committed
scripts/flights/
  prepare_data.py        # CSV -> flights.geo.json (stdlib + urllib)
  prepare_land.py        # NE admin-0 -> vendored land+boundary GeoJSON (shapely, antimeridian, urllib)
  render_map.py          # flights.geo.json + land -> SVG (pyproj, shapely, matplotlib)
  render_map.py.lock      # uv lock --script (committed)
  prepare_land.py.lock    # uv lock --script (committed)
  airport_overrides.json # manual coords for codes OurAirports lacks
  ne-110m-land.geojson    # vendored land fill (pre-rotated for lon_0=150)
  ne-110m-boundaries.geojson # vendored borders (pre-rotated for lon_0=150)
  conftest.py             # empty — puts scripts/flights on sys.path for tests
  tests/
    test_prepare_data.py
    test_prepare_land.py
    test_render_map.py
    fixtures/sample-log.csv # tiny hand-built CSV for prep tests
```

**Constants** (shared values; each script defines its own copy — these are tiny scripts, not a package):
- `LON0 = 150` (Pacific centre)
- `LAT_MIN, LAT_MAX = -58, 84` (Antarctica/polar trim)
- Palette B: `OCEAN="#1d2021" LAND="#32302f" BOUNDARY="#3c3836" GRATICULE="#262626" ARC="#83a598" DOT="#fe8019"`; `ALPHA_BASE=0.34`, `ARC_WIDTH=0.65`, `DOT_R=1.3`, `BOUNDARY_WIDTH=0.4`, `GRATICULE_WIDTH=0.4`.

**Test runner:** tests import the script modules directly (the scripts guard `main()` behind `if __name__ == "__main__"`). `scripts/flights/conftest.py` (empty) makes pytest prepend `scripts/flights` to `sys.path`. Run with the deps the imported modules need:
- prepare_data tests: `uv run --with pytest pytest scripts/flights/tests/test_prepare_data.py -v`
- prepare_land tests: `uv run --with pytest --with shapely --with antimeridian pytest scripts/flights/tests/test_prepare_land.py -v`
- render_map tests: `uv run --with pytest --with pyproj --with shapely --with matplotlib pytest scripts/flights/tests/test_render_map.py -v`

---

## Task 1: Test scaffold + prepare_data core (CSV → safe geometry)

**Files:**
- Create: `scripts/flights/conftest.py`
- Create: `scripts/flights/airport_overrides.json`
- Create: `scripts/flights/tests/fixtures/sample-log.csv`
- Create: `scripts/flights/prepare_data.py`
- Create: `scripts/flights/tests/test_prepare_data.py`

- [ ] **Step 1: Create the empty conftest and the overrides file**

`scripts/flights/conftest.py`:
```python
# Present so pytest prepends scripts/flights to sys.path, letting tests
# import prepare_data / prepare_land / render_map directly.
```

`scripts/flights/airport_overrides.json`:
```json
{
  "TXL": [13.2877, 52.5597]
}
```

- [ ] **Step 2: Create the test fixture CSV**

`scripts/flights/tests/fixtures/sample-log.csv` (header matches the real log; includes a duplicate corridor, a reversed corridor, the TXL override case, and a trailing blank row):
```csv
order,date_takeoff,flight_number,departing_airport,departure_time,arriving_airport,arrival_time,date_landing,seat,record_locator,notes
1,2020-01-01,AA1,SAN,9:00:00,SFO,10:30:00,2020-01-01,12A,ABC123,work
2,2020-01-05,AA2,SFO,18:00:00,SAN,19:30:00,2020-01-05,14C,ABC123,
3,2020-02-01,AA3,SAN,9:00:00,SFO,10:30:00,2020-02-01,,,
4,2020-03-01,LH7,FRA,8:00:00,TXL,9:00:00,2020-03-01,2A,,
5,,,,,,,,,,
```

- [ ] **Step 3: Write the failing tests**

`scripts/flights/tests/test_prepare_data.py`:
```python
import json
from pathlib import Path

import pytest

import prepare_data as pd

FIXTURE = Path(__file__).parent / "fixtures" / "sample-log.csv"

# Minimal coord table standing in for the OurAirports fetch.
COORDS = {
    "SAN": [-117.1897, 32.7336],
    "SFO": [-122.3749, 37.6190],
    "FRA": [8.5431, 50.0264],
    # TXL intentionally absent -> must come from overrides
}
OVERRIDES = {"TXL": [13.2877, 52.5597]}


def test_parse_log_skips_blank_rows_and_keeps_order():
    legs = pd.parse_log(FIXTURE)
    assert legs == [("SAN", "SFO"), ("SFO", "SAN"), ("SAN", "SFO"), ("FRA", "TXL")]


def test_resolve_coords_applies_overrides():
    codes = {"SAN", "SFO", "FRA", "TXL"}
    resolved = pd.resolve_coords(codes, COORDS, OVERRIDES)
    assert resolved["TXL"] == [13.2877, 52.5597]
    assert resolved["SAN"] == [-117.1897, 32.7336]


def test_resolve_coords_raises_on_unknown():
    with pytest.raises(SystemExit):
        pd.resolve_coords({"SAN", "ZZZ"}, COORDS, OVERRIDES)


def test_build_routes_is_undirected_sorted_and_counted():
    legs = [("SAN", "SFO"), ("SFO", "SAN"), ("SAN", "SFO"), ("FRA", "TXL")]
    routes = pd.build_routes(legs)
    # SAN-SFO appears 3x (both directions merge), FRA-TXL once; sorted by pair
    assert routes == [["FRA", "TXL", 1], ["SAN", "SFO", 3]]


def test_build_geojson_has_only_safe_keys():
    legs = pd.parse_log(FIXTURE)
    coords = pd.resolve_coords({c for leg in legs for c in leg}, COORDS, OVERRIDES)
    geo = pd.build_geojson(legs, coords)
    assert set(geo.keys()) == {"airports", "routes"}
    blob = json.dumps(geo)
    for leaked in ("ABC123", "12A", "2020", "AA1", "work"):
        assert leaked not in blob
    assert geo["airports"] == dict(sorted(coords.items()))
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `uv run --with pytest pytest scripts/flights/tests/test_prepare_data.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'prepare_data'`.

- [ ] **Step 5: Implement prepare_data.py**

`scripts/flights/prepare_data.py`:
```python
# /// script
# requires-python = "==3.12.*"
# dependencies = []
# ///
"""Stage 1: private flight-log CSV -> safe data/flights.geo.json.

Run locally (touches the private log):
    uv run scripts/flights/prepare_data.py
"""
from __future__ import annotations

import csv
import json
import sys
import urllib.request
from pathlib import Path

OURAIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_CSV = REPO_ROOT / "data" / "flight-log.csv"
OUT_JSON = REPO_ROOT / "data" / "flights.geo.json"
OVERRIDES_JSON = Path(__file__).with_name("airport_overrides.json")


def parse_log(csv_path: Path) -> list[tuple[str, str]]:
    """Return [(dep, arr), ...] for every row with both airports, in file order."""
    legs: list[tuple[str, str]] = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            dep = (row.get("departing_airport") or "").strip()
            arr = (row.get("arriving_airport") or "").strip()
            if dep and arr:
                legs.append((dep, arr))
    return legs


def fetch_ourairports() -> dict[str, list[float]]:
    """Fetch the public OurAirports table -> {IATA: [lon, lat]}."""
    with urllib.request.urlopen(OURAIRPORTS_URL) as resp:  # noqa: S310 (trusted public CSV)
        text = resp.read().decode("utf-8")
    coords: dict[str, list[float]] = {}
    for row in csv.DictReader(text.splitlines()):
        iata = (row.get("iata_code") or "").strip()
        if not iata:
            continue
        try:
            coords[iata] = [
                round(float(row["longitude_deg"]), 4),
                round(float(row["latitude_deg"]), 4),
            ]
        except (KeyError, ValueError):
            continue
    return coords


def resolve_coords(
    codes: set[str], fetched: dict[str, list[float]], overrides: dict[str, list[float]]
) -> dict[str, list[float]]:
    """Resolve every code; overrides win. Exit non-zero if any code is unresolved."""
    resolved: dict[str, list[float]] = {}
    missing: list[str] = []
    for code in codes:
        if code in overrides:
            resolved[code] = list(overrides[code])
        elif code in fetched:
            resolved[code] = list(fetched[code])
        else:
            missing.append(code)
    if missing:
        sys.exit(
            f"ERROR: no coordinates for {sorted(missing)}. "
            f"Add them to {OVERRIDES_JSON.name} and re-run."
        )
    return resolved


def build_routes(legs: list[tuple[str, str]]) -> list[list]:
    """Collapse legs into undirected [a, b, count] with a < b, sorted by pair."""
    counts: dict[tuple[str, str], int] = {}
    for dep, arr in legs:
        key = tuple(sorted((dep, arr)))
        counts[key] = counts.get(key, 0) + 1
    return [[a, b, counts[(a, b)]] for (a, b) in sorted(counts)]


def build_geojson(
    legs: list[tuple[str, str]], coords: dict[str, list[float]]
) -> dict:
    """Assemble the safe public geometry: sorted airports + undirected routes."""
    return {
        "airports": dict(sorted(coords.items())),
        "routes": build_routes(legs),
    }


def main() -> None:
    legs = parse_log(LOG_CSV)
    codes = {c for leg in legs for c in leg}
    overrides = json.loads(OVERRIDES_JSON.read_text())
    coords = resolve_coords(codes, fetch_ourairports(), overrides)
    geo = build_geojson(legs, coords)
    OUT_JSON.write_text(json.dumps(geo, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUT_JSON} ({len(geo['airports'])} airports, {len(geo['routes'])} routes)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run --with pytest pytest scripts/flights/tests/test_prepare_data.py -v`
Expected: PASS (5 passed).

- [ ] **Step 7: Generate the real flights.geo.json and sanity-check**

Run: `uv run scripts/flights/prepare_data.py`
Expected: `Wrote .../data/flights.geo.json (69 airports, N routes)`.
Run: `uv run --with pytest python -c "import json;d=json.load(open('data/flights.geo.json'));print(sorted(d));print(len(d['airports']),len(d['routes']))"`
Expected: `['airports', 'routes']` and `69` airports.
Run: `grep -c -E 'record_locator|seat|date|notes|2020|ABC' data/flights.geo.json`
Expected: `0`.

- [ ] **Step 8: Commit**

```bash
git add scripts/flights/conftest.py scripts/flights/airport_overrides.json \
        scripts/flights/prepare_data.py scripts/flights/tests/test_prepare_data.py \
        scripts/flights/tests/fixtures/sample-log.csv data/flights.geo.json
git commit -m "feat(flights): prepare_data — private log to safe geometry JSON"
```

---

## Task 2: prepare_land.py — vendor rotated, seam-cut land + boundaries

**Files:**
- Create: `scripts/flights/prepare_land.py`
- Create: `scripts/flights/tests/test_prepare_land.py`
- Output (committed): `scripts/flights/ne-110m-land.geojson`, `scripts/flights/ne-110m-boundaries.geojson`

- [ ] **Step 1: Write the failing tests** (pure helpers — rotation + trim)

`scripts/flights/tests/test_prepare_land.py`:
```python
import pytest

import prepare_land as pl


def test_wrap_lon_rotates_into_range():
    # Pacific centre 150: original -30 (the seam) maps to the -180 boundary
    assert pl.wrap_lon(-30.0, 150) == pytest.approx(-180.0, abs=1e-6)
    assert pl.wrap_lon(150.0, 150) == pytest.approx(0.0, abs=1e-6)
    assert pl.wrap_lon(151.0, 150) == pytest.approx(1.0, abs=1e-6)
    assert pl.wrap_lon(-179.0, 150) == pytest.approx(31.0, abs=1e-6)


def test_wrap_lon_result_always_in_half_open_range():
    for lon in range(-180, 181, 7):
        r = pl.wrap_lon(float(lon), 150)
        assert -180.0 <= r < 180.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run --with pytest --with shapely --with antimeridian pytest scripts/flights/tests/test_prepare_land.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'prepare_land'`.

- [ ] **Step 3: Implement prepare_land.py**

`scripts/flights/prepare_land.py`:
```python
# /// script
# requires-python = "==3.12.*"
# dependencies = ["shapely==2.0.6", "antimeridian==0.4.0"]
# ///
"""One-time, local: build pre-rotated, antimeridian-cut, Antarctica-trimmed
land + boundary GeoJSONs for lon_0=150, vendored next to render_map.py.

    uv run scripts/flights/prepare_land.py
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import antimeridian
from shapely import box
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union

LON0 = 150
LAT_MIN, LAT_MAX = -58, 84
# Natural Earth 110m admin-0 countries (yields both land fill and borders).
NE_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
    "geojson/ne_110m_admin_0_countries.geojson"
)
HERE = Path(__file__).parent
LAND_OUT = HERE / "ne-110m-land.geojson"
BOUNDARIES_OUT = HERE / "ne-110m-boundaries.geojson"


def wrap_lon(lon: float, lon0: int) -> float:
    """Shift longitude into the rotated frame: result in [-180, 180)."""
    return ((lon - lon0 + 180.0) % 360.0) - 180.0


def _rotate(geom):
    return transform(lambda xs, ys, z=None: ([wrap_lon(x, LON0) for x in xs], list(ys)), geom)


def _prep(geom):
    """Rotate into the lon_0 frame, antimeridian-cut, then trim polar latitudes."""
    rotated = _rotate(geom)
    fixed = antimeridian.fix_geometry(rotated)  # splits polygons crossing +/-180
    return fixed.intersection(box(-180, LAT_MIN, 180, LAT_MAX))


def main() -> None:
    with urllib.request.urlopen(NE_URL) as resp:  # noqa: S310 (trusted public data)
        fc = json.load(resp)
    geoms = [_prep(shape(f["geometry"])) for f in fc["features"]]
    geoms = [g for g in geoms if not g.is_empty]

    land = unary_union(geoms)
    boundaries = unary_union([g.boundary for g in geoms])

    LAND_OUT.write_text(json.dumps(mapping(land), sort_keys=True) + "\n")
    BOUNDARIES_OUT.write_text(json.dumps(mapping(boundaries), sort_keys=True) + "\n")
    print(f"Wrote {LAND_OUT.name} and {BOUNDARIES_OUT.name}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest --with shapely --with antimeridian pytest scripts/flights/tests/test_prepare_land.py -v`
Expected: PASS.

- [ ] **Step 5: Generate the vendored GeoJSONs**

Run: `uv run scripts/flights/prepare_land.py`
Expected: `Wrote ne-110m-land.geojson and ne-110m-boundaries.geojson`.
Run: `uv run --with pytest --with shapely python -c "import json; from shapely.geometry import shape; g=shape(json.load(open('scripts/flights/ne-110m-land.geojson'))); print('valid', g.is_valid); b=g.bounds; print('lat span', round(b[1]), round(b[3]))"`
Expected: `valid True` and a latitude span within roughly `-58 .. 84` (Antarctica trimmed).

- [ ] **Step 6: Commit**

```bash
git add scripts/flights/prepare_land.py scripts/flights/tests/test_prepare_land.py \
        scripts/flights/ne-110m-land.geojson scripts/flights/ne-110m-boundaries.geojson
git commit -m "feat(flights): prepare_land — vendor rotated seam-cut land + boundaries"
```

---

## Task 3: render_map.py geometry helpers (pure functions)

**Files:**
- Create: `scripts/flights/render_map.py` (helpers + stubbed `main`)
- Create: `scripts/flights/tests/test_render_map.py`

- [ ] **Step 1: Write the failing tests**

`scripts/flights/tests/test_render_map.py`:
```python
import pytest

import render_map as rm


def test_wrap_lon_matches_rotation_convention():
    assert rm.wrap_lon(-30.0, 150) == pytest.approx(-180.0, abs=1e-6)
    assert rm.wrap_lon(150.0, 150) == pytest.approx(0.0, abs=1e-6)


def test_alpha_eff_compositing():
    assert rm.alpha_eff(0.34, 1) == pytest.approx(0.34)
    # Two stacked strokes: 1 - (1-0.34)^2
    assert rm.alpha_eff(0.34, 2) == pytest.approx(1 - 0.66 ** 2)
    assert rm.alpha_eff(0.34, 10) < 1.0


def test_split_on_seam_breaks_large_x_jumps():
    # x jumps from 9 to -9 (gap 18) with max_jump 10 -> two segments
    pts = [(0, 0), (9, 1), (-9, 1), (-8, 2)]
    segs = rm.split_on_seam(pts, max_jump=10)
    assert [len(s) for s in segs] == [2, 2]


def test_split_on_seam_keeps_continuous_path():
    pts = [(0, 0), (1, 1), (2, 2)]
    assert rm.split_on_seam(pts, max_jump=10) == [pts]


def test_great_circle_endpoints_and_density():
    arc = rm.great_circle([-122.37, 37.62], [144.84, -37.67], n=48)
    assert len(arc) == 48
    assert arc[0] == pytest.approx([-122.37, 37.62], abs=1e-6)
    assert arc[-1] == pytest.approx([144.84, -37.67], abs=1e-6)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run --with pytest --with pyproj --with shapely --with matplotlib pytest scripts/flights/tests/test_render_map.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'render_map'`.

- [ ] **Step 3: Implement render_map.py helpers (with a stub main)**

`scripts/flights/render_map.py`:
```python
# /// script
# requires-python = "==3.12.*"
# dependencies = ["pyproj==3.6.1", "shapely==2.0.6", "matplotlib==3.9.2"]
# ///
"""Stage 2: data/flights.geo.json + vendored land -> static dark SVG.

    uv run --locked scripts/flights/render_map.py
"""
from __future__ import annotations

import json
from pathlib import Path

from pyproj import Geod

LON0 = 150
LAT_MIN, LAT_MAX = -58, 84
OCEAN, LAND, BOUNDARY = "#1d2021", "#32302f", "#3c3836"
GRATICULE, ARC, DOT = "#262626", "#83a598", "#fe8019"
ALPHA_BASE, ARC_WIDTH, DOT_R = 0.34, 0.65, 1.3
BOUNDARY_WIDTH, GRATICULE_WIDTH = 0.4, 0.4

_GEOD = Geod(ellps="WGS84")


def wrap_lon(lon: float, lon0: int) -> float:
    """Shift longitude into the rotated frame: result in [-180, 180)."""
    return ((lon - lon0 + 180.0) % 360.0) - 180.0


def alpha_eff(base: float, count: int) -> float:
    """Composited opacity of `count` identical strokes (source-over)."""
    return 1.0 - (1.0 - base) ** count


def great_circle(a: list[float], b: list[float], n: int = 48) -> list[list[float]]:
    """Densify the great circle a->b into n true-longitude [lon, lat] points."""
    inter = _GEOD.npts(a[0], a[1], b[0], b[1], n - 2)
    return [[a[0], a[1]], *[[lon, lat] for lon, lat in inter], [b[0], b[1]]]


def split_on_seam(xy: list[tuple[float, float]], max_jump: float) -> list[list]:
    """Break a projected polyline wherever x jumps more than max_jump (seam)."""
    segments: list[list] = []
    current = [xy[0]]
    for prev, cur in zip(xy, xy[1:]):
        if abs(cur[0] - prev[0]) > max_jump:
            segments.append(current)
            current = [cur]
        else:
            current.append(cur)
    segments.append(current)
    return segments


def main() -> None:  # pragma: no cover (covered by Task 4 integration test)
    raise NotImplementedError
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest --with pyproj --with shapely --with matplotlib pytest scripts/flights/tests/test_render_map.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/flights/render_map.py scripts/flights/tests/test_render_map.py
git commit -m "feat(flights): render_map geometry helpers (rotation, arcs, seam split, alpha)"
```

---

## Task 4: render_map.py drawing + determinism (produces the SVG)

**Files:**
- Modify: `scripts/flights/render_map.py` (replace stub `main`, add `render`)
- Modify: `scripts/flights/tests/test_render_map.py` (add integration tests)
- Output (committed): `assets/images/flights/flights-map.svg`

- [ ] **Step 1: Write the failing integration tests**

Append to `scripts/flights/tests/test_render_map.py`:
```python
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SVG = REPO / "assets" / "images" / "flights" / "flights-map.svg"


def test_render_produces_valid_svg(tmp_path):
    out = tmp_path / "map.svg"
    rm.render(REPO / "data" / "flights.geo.json", out)
    text = out.read_text()
    assert text.lstrip().startswith("<?xml") or text.lstrip().startswith("<svg")
    assert "</svg>" in text
    assert "1d2021" in text.lower()  # ocean color baked in


def test_render_is_byte_deterministic(tmp_path):
    a, b = tmp_path / "a.svg", tmp_path / "b.svg"
    rm.render(REPO / "data" / "flights.geo.json", a)
    rm.render(REPO / "data" / "flights.geo.json", b)
    assert a.read_bytes() == b.read_bytes()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run --with pytest --with pyproj --with shapely --with matplotlib pytest scripts/flights/tests/test_render_map.py -v`
Expected: FAIL (`render` not defined / `NotImplementedError`).

- [ ] **Step 3: Implement `render` and `main`**

In `scripts/flights/render_map.py`, add imports at top of the file (after `from pyproj import Geod`):
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pyproj import Transformer
from shapely.geometry import shape

HERE = Path(__file__).parent
LAND_GEOJSON = HERE / "ne-110m-land.geojson"
BOUNDARIES_GEOJSON = HERE / "ne-110m-boundaries.geojson"
_TRANSFORMER = Transformer.from_crs("EPSG:4326", "+proj=natearth +lon_0=0", always_xy=True)
```

Replace the stub `main` with:
```python
def _project(lon_rot: float, lat: float) -> tuple[float, float]:
    return _TRANSFORMER.transform(lon_rot, lat)


def _polys(geom):
    """Yield exterior coordinate rings for (Multi)Polygon geometries."""
    if geom.geom_type == "Polygon":
        yield list(geom.exterior.coords)
    elif geom.geom_type == "MultiPolygon":
        for p in geom.geoms:
            yield list(p.exterior.coords)


def _lines(geom):
    """Yield coordinate sequences for (Multi)LineString geometries."""
    if geom.geom_type == "LineString":
        yield list(geom.coords)
    elif geom.geom_type == "MultiLineString":
        for ls in geom.geoms:
            yield list(ls.coords)


def render(data_path: Path, out_path: Path) -> None:
    # Determinism: fixed hashsalt, no font glyph IDs, no embedded date.
    mpl.rcParams["svg.hashsalt"] = "flights-map"
    mpl.rcParams["svg.fonttype"] = "none"

    data = json.loads(Path(data_path).read_text())
    land = shape(json.loads(LAND_GEOJSON.read_text()))       # already rotated
    boundaries = shape(json.loads(BOUNDARIES_GEOJSON.read_text()))  # already rotated

    fig, ax = plt.subplots(figsize=(12.8, 8.0))
    fig.patch.set_facecolor(OCEAN)
    ax.set_facecolor(OCEAN)
    ax.set_axis_off()
    ax.set_aspect("equal")

    # Land fill (project only — vendored geometry is pre-rotated).
    for ring in _polys(land):
        xs, ys = zip(*[_project(x, y) for x, y in ring])
        ax.fill(xs, ys, facecolor=LAND, edgecolor="none", zorder=1)
    # Country boundaries.
    bsegs = [[_project(x, y) for x, y in seq] for seq in _lines(boundaries)]
    ax.add_collection(LineCollection(bsegs, colors=BOUNDARY, linewidths=BOUNDARY_WIDTH, zorder=2))

    # Graticule: built directly in the rotated frame (meridians/parallels in [-180,180)).
    grat = []
    for lon in range(-180, 180, 30):
        grat.append([_project(lon, lat) for lat in range(LAT_MIN, LAT_MAX + 1, 5)])
    for lat in range(-60, 91, 30):
        grat.append([_project(lon, lat) for lon in range(-180, 181, 5)])
    ax.add_collection(LineCollection(grat, colors=GRATICULE, linewidths=GRATICULE_WIDTH, zorder=0))

    # Compute seam threshold from the projected map width.
    minx, _ = _project(-179.999, 0)
    maxx, _ = _project(179.999, 0)
    max_jump = (maxx - minx) * 0.5

    # Flight arcs (true-lon great circle -> rotate -> project -> seam-split).
    airports = data["airports"]
    for a_code, b_code, count in data["routes"]:
        arc = great_circle(airports[a_code], airports[b_code], n=48)
        xy = [_project(wrap_lon(lon, LON0), lat) for lon, lat in arc]
        for seg in split_on_seam(xy, max_jump):
            if len(seg) < 2:
                continue
            xs, ys = zip(*seg)
            ax.plot(xs, ys, color=ARC, linewidth=ARC_WIDTH,
                    alpha=alpha_eff(ALPHA_BASE, count), solid_capstyle="round", zorder=3)

    # Airport dots.
    dxy = [_project(wrap_lon(lon, LON0), lat) for lon, lat in airports.values()]
    ax.scatter([p[0] for p in dxy], [p[1] for p in dxy], s=DOT_R ** 2 * 3,
               c=DOT, edgecolors="none", zorder=4)

    ax.autoscale_view()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, format="svg", facecolor=OCEAN, metadata={"Date": None})
    plt.close(fig)


def main() -> None:
    out = HERE.parents[1] / "assets" / "images" / "flights" / "flights-map.svg"
    render(HERE.parents[1] / "data" / "flights.geo.json", out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest --with pyproj --with shapely --with matplotlib pytest scripts/flights/tests/test_render_map.py -v`
Expected: PASS (all tests). If the determinism test fails, check that no `id="..."`/date varies between runs and that `svg.hashsalt` is set before `savefig`.

- [ ] **Step 5: Render the committed SVG**

Run: `uv run scripts/flights/render_map.py`
Expected: `Wrote .../assets/images/flights/flights-map.svg`.

- [ ] **Step 6: MANUAL visual verification** (spec verification #4–#6)

Open `assets/images/flights/flights-map.svg` in a browser. Confirm:
- Dark ground; Bay-Area (SAN/SFO/SJC) and DFW corridors are visibly the brightest (high counts → high `alpha_eff`).
- A trans-Pacific arc (LAX–MEL) and an Atlantic arc (SFO–CPH) are clean curves, **not** horizontal smears.
- No land polygon smears across the map; Antarctica is absent.
If any smear appears, the seam handling is wrong — stop and report rather than committing.

- [ ] **Step 7: Commit**

```bash
git add scripts/flights/render_map.py scripts/flights/tests/test_render_map.py \
        assets/images/flights/flights-map.svg
git commit -m "feat(flights): render_map drawing + deterministic SVG output"
```

---

## Task 5: Lock dependencies + full verification sweep

**Files:**
- Create: `scripts/flights/render_map.py.lock`, `scripts/flights/prepare_land.py.lock`

- [ ] **Step 1: Generate committed script lockfiles**

Run:
```bash
uv lock --script scripts/flights/render_map.py
uv lock --script scripts/flights/prepare_land.py
ls scripts/flights/*.lock
```
Expected: `render_map.py.lock` and `prepare_land.py.lock` exist.

- [ ] **Step 2: Verify locked render still works and stays deterministic**

Run:
```bash
uv run --locked scripts/flights/render_map.py
cp assets/images/flights/flights-map.svg /tmp/map1.svg
uv run --locked scripts/flights/render_map.py
diff -q /tmp/map1.svg assets/images/flights/flights-map.svg
```
Expected: `uv run --locked` succeeds both times; `diff` reports no differences (byte-identical).

- [ ] **Step 3: Privacy + ignore sweep** (spec verification #2, #8)

Run:
```bash
git check-ignore data/flight-log.csv
python3 -c "import json;d=json.load(open('data/flights.geo.json'));assert set(d)=={'airports','routes'};assert all(len(r)==3 and r[0]<r[1] for r in d['routes']);print('shape OK')"
grep -c -iE 'record_locator|seat|notes|flight_number|20[0-2][0-9]-[0-1][0-9]-[0-3][0-9]' data/flights.geo.json
git status --short
```
Expected: raw log path printed (ignored); `shape OK`; grep count `0`; `git status` shows only the intended tracked artifacts (no `data/flight-log.csv`).

- [ ] **Step 4: Run the full test suite**

Run: `uv run --with pytest --with pyproj --with shapely --with antimeridian --with matplotlib pytest scripts/flights/tests/ -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/flights/render_map.py.lock scripts/flights/prepare_land.py.lock
git commit -m "chore(flights): commit uv script lockfiles for deterministic render"
```

---

## Notes for the implementer

- **Do not** `git add data/flight-log.csv` — it is gitignored and contains PNRs/seats. If `git status` ever shows it, stop.
- The `antimeridian`, `pyproj`, `shapely`, `matplotlib` versions in the PEP 723 headers are starting pins; if `uv` resolves a newer compatible version, that's fine — the committed `*.lock` files are the source of determinism. Keep the headers and lockfiles in sync (`uv lock --script` after any header edit).
- Placement of the SVG into a page and CI/pre-render wiring are **out of scope** (separate task per the spec).
- If the manual visual check in Task 4 reveals a seam smear, the bug is almost certainly in the rotate-vs-project split (land must be projected only; flight coords + graticule rotated) — re-read the spec's "What gets rotated" bullet before touching anything.
```
