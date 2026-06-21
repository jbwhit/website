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
    for lat in range(-45, 76, 15):  # parallels kept within the trimmed [LAT_MIN, LAT_MAX] band
        grat.append([_project(lon, lat) for lon in range(-180, 180, 5)])
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


# Each safe dataset -> its committed SVG. The 2014 snapshot backs the restored
# 2014 post; the full history backs the 2026 post.
SNAPSHOTS = {
    "flights.geo.json": "flights-map.svg",
    "flights.geo.2014.json": "flights-map-2014.svg",
}


def main() -> None:
    data_dir = HERE.parents[1] / "data"
    out_dir = HERE.parents[1] / "assets" / "images" / "flights"
    for data_name, svg_name in SNAPSHOTS.items():
        out = out_dir / svg_name
        render(data_dir / data_name, out)
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
