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
