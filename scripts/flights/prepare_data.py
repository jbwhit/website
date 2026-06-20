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
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
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
            f"Add them to {OVERRIDES_JSON} and re-run."
        )
    return resolved


def build_routes(legs: list[tuple[str, str]]) -> list[list]:
    """Collapse legs into undirected [a, b, count] with a < b, sorted by pair."""
    counts: dict[tuple[str, str], int] = {}
    for dep, arr in legs:
        key = tuple(sorted((dep, arr)))
        counts[key] = counts.get(key, 0) + 1
    return [[a, b, n] for (a, b), n in sorted(counts.items())]


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
