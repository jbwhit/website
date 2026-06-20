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
