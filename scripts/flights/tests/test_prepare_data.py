import json
from pathlib import Path

import pytest

import prepare_data as pd

FIXTURE = Path(__file__).parent / "fixtures" / "sample-log.csv"

COORDS = {
    "SAN": [-117.1897, 32.7336],
    "SFO": [-122.3749, 37.6190],
    "FRA": [8.5431, 50.0264],
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
