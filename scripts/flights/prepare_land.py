# /// script
# requires-python = "==3.12.*"
# dependencies = ["shapely==2.0.6", "antimeridian==0.4.0", "numpy>=1.26"]
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
import numpy as np  # noqa: F401 (used implicitly via shapely.transform arrays)
from shapely import box
from shapely import transform as shapely_transform
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

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
    """Shift every longitude by -LON0 using shapely 2.x vectorized transform.

    The callback receives an (N, 2) array of [lon, lat] and returns the same shape.
    """
    def _shift(coords):
        out = coords.copy()
        out[:, 0] = (coords[:, 0] - LON0 + 180.0) % 360.0 - 180.0
        return out

    return shapely_transform(geom, _shift)


def _prep(geom):
    """Rotate into the lon_0 frame, antimeridian-cut, then trim polar latitudes."""
    rotated = _rotate(geom)
    # antimeridian v0.4.0 fix_shape returns a GeoJSON-style dict — wrap back to shapely.
    fixed = shape(antimeridian.fix_shape(rotated))  # splits polygons crossing +/-180
    return fixed.intersection(box(-180, LAT_MIN, 180, LAT_MAX))


def main() -> None:
    with urllib.request.urlopen(NE_URL) as resp:  # noqa: S310 (trusted public data)
        fc = json.load(resp)
    geoms = []
    for f in fc["features"]:
        g = shape(f["geometry"])
        # Drop features entirely below the trim (Antarctica). Its polar
        # circumglobal ring otherwise mis-winds through antimeridian.fix_shape
        # into a world-filling polygon that collapses the land union to a bbox.
        if g.bounds[3] < LAT_MIN:
            continue
        prepped = _prep(g)
        if not prepped.is_empty:
            geoms.append(prepped)

    land = unary_union(geoms)
    boundaries = unary_union([g.boundary for g in geoms])

    LAND_OUT.write_text(json.dumps(mapping(land), sort_keys=True) + "\n")
    BOUNDARIES_OUT.write_text(json.dumps(mapping(boundaries), sort_keys=True) + "\n")
    print(f"Wrote {LAND_OUT.name} and {BOUNDARIES_OUT.name}")


if __name__ == "__main__":
    main()
