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
OVERRIDES_JSON = Path(__file__).with_name("airport_overrides.json")

# Safe datasets to emit. Each value is a date cutoff (ISO "YYYY-MM-DD") or None
# for the full history. Cutoffs let a dated post show only the flights it could
# have shown at the time — dates are read from the private log but never published.
SNAPSHOTS: dict[Path, str | None] = {
    REPO_ROOT / "data" / "flights.geo.json": None,
    REPO_ROOT / "data" / "flights.geo.2014.json": "2014-08-01",
}


def parse_log(csv_path: Path, cutoff: str | None = None) -> list[tuple[str, str]]:
    """Return [(dep, arr), ...] for every row with both airports, in file order.

    If `cutoff` (an ISO "YYYY-MM-DD" string) is given, include only flights whose
    `date_takeoff` is on or before it; rows without a usable date are excluded.
    ISO dates sort lexicographically, so a plain string compare is correct.
    """
    legs: list[tuple[str, str]] = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            dep = (row.get("departing_airport") or "").strip()
            arr = (row.get("arriving_airport") or "").strip()
            if not (dep and arr):
                continue
            if cutoff is not None:
                date = (row.get("date_takeoff") or "").strip()
                if not date or date > cutoff:
                    continue
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
    overrides = json.loads(OVERRIDES_JSON.read_text())
    fetched = fetch_ourairports()
    for out_path, cutoff in SNAPSHOTS.items():
        legs = parse_log(LOG_CSV, cutoff)
        codes = {c for leg in legs for c in leg}
        coords = resolve_coords(codes, fetched, overrides)
        geo = build_geojson(legs, coords)
        out_path.write_text(json.dumps(geo, indent=2, sort_keys=True) + "\n")
        label = "full history" if cutoff is None else f"through {cutoff}"
        print(
            f"Wrote {out_path.name} [{label}] "
            f"({len(geo['airports'])} airports, {len(geo['routes'])} routes)"
        )


if __name__ == "__main__":
    main()
