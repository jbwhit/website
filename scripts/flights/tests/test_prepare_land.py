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


def test_prep_splits_seam_crossing_polygon_and_trims_lat():
    # A box at original lon -40..-20 straddles the rotated seam (original -30 -> +/-180),
    # so _prep must antimeridian-split it into a MultiPolygon. This exercises the real
    # rotate -> fix_shape -> trim path (and would fail if the antimeridian API is wrong).
    from shapely.geometry import Polygon

    poly = Polygon([(-40, 10), (-20, 10), (-20, 30), (-40, 30)])
    out = pl._prep(poly)
    assert not out.is_empty
    assert out.is_valid
    assert out.geom_type == "MultiPolygon"
    minx, miny, maxx, maxy = out.bounds
    # Split output legitimately includes seam coordinates at exactly +/-180.
    assert -180.0 <= minx and maxx <= 180.0
    assert miny >= pl.LAT_MIN and maxy <= pl.LAT_MAX


def test_prep_trims_below_antarctica_cut():
    # A polygon entirely below LAT_MIN should be trimmed away to empty.
    from shapely.geometry import Polygon

    deep_south = Polygon([(10, -80), (20, -80), (20, -70), (10, -70)])
    assert pl._prep(deep_south).is_empty
