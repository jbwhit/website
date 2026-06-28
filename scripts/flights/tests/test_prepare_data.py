import json
from pathlib import Path

import pytest

import prepare_data

FIXTURE = Path(__file__).parent / "fixtures" / "sample-log.csv"

COORDS = {
    "SAN": [-117.1897, 32.7336],
    "SFO": [-122.3749, 37.6190],
    "FRA": [8.5431, 50.0264],
}
OVERRIDES = {"TXL": [13.2877, 52.5597]}


def test_parse_log_skips_blank_rows_and_keeps_order():
    legs = prepare_data.parse_log(FIXTURE)
    assert legs == [("SAN", "SFO"), ("SFO", "SAN"), ("SAN", "SFO"), ("FRA", "TXL")]


def test_parse_log_cutoff_filters_by_date():
    # Fixture dates: rows 1,2 are 2020-01; rows 3,4 are 2020-02 / 2020-03.
    legs = prepare_data.parse_log(FIXTURE, cutoff="2020-01-31")
    assert legs == [("SAN", "SFO"), ("SFO", "SAN")]


def test_resolve_coords_applies_overrides():
    codes = {"SAN", "SFO", "FRA", "TXL"}
    resolved = prepare_data.resolve_coords(codes, COORDS, OVERRIDES)
    assert resolved["TXL"] == [13.2877, 52.5597]
    assert resolved["SAN"] == [-117.1897, 32.7336]


def test_resolve_coords_raises_on_unknown():
    with pytest.raises(SystemExit, match="ZZZ"):
        prepare_data.resolve_coords({"SAN", "ZZZ"}, COORDS, OVERRIDES)


def test_resolve_coords_override_beats_fetched():
    resolved = prepare_data.resolve_coords({"TXL"}, {"TXL": [0.0, 0.0]}, OVERRIDES)
    assert resolved["TXL"] == [13.2877, 52.5597]


def test_build_routes_is_undirected_sorted_and_counted():
    legs = [("SAN", "SFO"), ("SFO", "SAN"), ("SAN", "SFO"), ("FRA", "TXL")]
    routes = prepare_data.build_routes(legs)
    assert routes == [["FRA", "TXL", 1], ["SAN", "SFO", 3]]


def test_build_geojson_has_only_safe_keys():
    legs = prepare_data.parse_log(FIXTURE)
    coords = prepare_data.resolve_coords(
        {c for leg in legs for c in leg}, COORDS, OVERRIDES
    )
    geo = prepare_data.build_geojson(legs, coords)
    assert set(geo.keys()) == {"airports", "routes"}
    blob = json.dumps(geo)
    for leaked in ("ABC123", "12A", "2020", "AA1", "work"):
        assert leaked not in blob
    assert geo["airports"] == dict(sorted(coords.items()))
