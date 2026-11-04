#!/usr/bin/env python3
"""
Periodically fetch and store rider position snapshots
from the CriticalMaps API.

Each snapshot is saved as a separate CSV file named <timestamp>.csv
inside the output directory.

Usage:
    # ./criticalmaps-data/, 30s interval:
    python record_criticalmaps.py
    python record_criticalmaps.py --out-dir ./my-ride
    python record_criticalmaps.py --interval 60 --duration 7200
"""

import argparse
import csv
import json
import signal
import time
from types import FrameType
from typing import Any
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

API_URL = "https://api-cdn.criticalmaps.net/locations"
MIN_INTERVAL = 10

def fetch_positions() -> dict[str, Any]:
    req = urllib.request.Request(
        API_URL, method="GET",
        headers={"Content-Type": "application/json",
                 "Accept": "application/json",
                 "User-Agent": "criticalmaps-recorder/1.0"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def save_csv(
        out_dir: Path,
        ts: int,
        positions: dict[str, Any],
) -> Path:
    path = out_dir / f"{datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H%M%S.csv")}"
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["device", "latitude", "longitude"])
        for info in positions:
            writer.writerow([info["device"][:16],  # truncate hashes to save space
                             info["latitude"]  / 1_000_000,
                             info["longitude"] / 1_000_000])
    return path


def record(interval: int, duration: int | None, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    stop = False
    count = 0

    def on_sigint(sig: int, frame: FrameType | None) -> None:
        nonlocal stop
        print("\nInterrupted – exiting.")
        stop = True

    signal.signal(signal.SIGINT, on_sigint)
    print(
        f"Recording to {out_dir}/  (interval={interval}s"
        + (f", duration={duration}s)" if duration else ", until Ctrl-C)")
    )

    while not stop:
        if duration and (time.monotonic() - start) >= duration:
            print("Duration reached.")
            break

        ts = int(datetime.now(UTC).timestamp())
        try:
            positions = fetch_positions()
            path = save_csv(out_dir, ts, positions)
            count += 1
            isodate = datetime.fromtimestamp(ts).isoformat()
            print(
                f"  {isodate}  –  {len(positions)} rider(s)  →  {path.name}"
            )
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            print(f"  {isodate}  –  fetch error: {exc}")

        deadline = time.monotonic() + interval
        while not stop and time.monotonic() < deadline:
            time.sleep(0.25)

    print(f"Done. {count} file(s) saved to {out_dir}/")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record CriticalMaps position data."
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("criticalmaps-data"),
        help="Output directory (created if needed, "
             "default: ./criticalmaps-data)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Seconds between snapshots (default: 30)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Stop after this many seconds (default: run forever)",
    )
    args = parser.parse_args()

    if args.interval < MIN_INTERVAL:
        raise SystemExit(f"Interval must be at least {MIN_INTERVAL} seconds.")

    record(args.interval, args.duration, args.out_dir)


if __name__ == "__main__":
    main()
