from pathlib import Path

import pytest

import render_map as rm

REPO = Path(__file__).resolve().parents[3]


def test_wrap_lon_matches_rotation_convention():
    assert rm.wrap_lon(-30.0, 150) == pytest.approx(-180.0, abs=1e-6)
    assert rm.wrap_lon(150.0, 150) == pytest.approx(0.0, abs=1e-6)


def test_alpha_eff_compositing():
    assert rm.alpha_eff(0.34, 1) == pytest.approx(0.34)
    # Two stacked strokes: 1 - (1-0.34)^2
    assert rm.alpha_eff(0.34, 2) == pytest.approx(1 - 0.66**2)
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


def _max_jump():
    minx, _ = rm._project(-179.999, 0)
    maxx, _ = rm._project(179.999, 0)
    return (maxx - minx) * 0.5


def test_atlantic_route_splits_with_no_internal_seam_jump():
    # SFO -> CPH crosses the rotated seam; it must split into >=2 segments, and
    # every returned segment must be internally smooth (no x-jump > max_jump).
    arc = rm.great_circle([-122.37, 37.62], [12.57, 55.62], n=48)
    xy = [rm._project(rm.wrap_lon(lon, rm.LON0), lat) for lon, lat in arc]
    segs = rm.split_on_seam(xy, _max_jump())
    assert len(segs) >= 2
    for seg in segs:
        for (x0, _), (x1, _) in zip(seg, seg[1:]):
            assert abs(x1 - x0) <= _max_jump()


def test_local_route_not_split():
    # SAN -> SFO stays well clear of the seam -> single segment.
    arc = rm.great_circle([-117.19, 32.73], [-122.37, 37.62], n=48)
    xy = [rm._project(rm.wrap_lon(lon, rm.LON0), lat) for lon, lat in arc]
    assert len(rm.split_on_seam(xy, _max_jump())) == 1
