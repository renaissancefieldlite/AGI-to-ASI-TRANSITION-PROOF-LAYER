#!/usr/bin/env python3
"""
Real-time interaction probe.

Measures an interaction artifact as it evolves and detects state shifts
between snapshots using the repo's existing interface/temporal metrics.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from consciousness_interface import build_interface_report
from temporal_coherence import build_temporal_report
from transition_metrics import build_transition_profile


def build_snapshot(text: str, source: str, index: int) -> dict:
    interface_report = build_interface_report(text, source)
    temporal_report = build_temporal_report(text, source)
    profile = build_transition_profile(interface_report, temporal_report, spectral_report=None)
    return {
        "snapshot_index": index,
        "character_count": len(text),
        "interface_report": interface_report,
        "temporal_report": temporal_report,
        "transition_profile": profile,
    }


def build_state_delta(previous: dict | None, current: dict) -> dict:
    if previous is None:
        return {
            "state_shift_detected": False,
            "shift_label": "baseline",
            "overall_delta": 0.0,
            "signal_deltas": {},
        }

    prev_profile = previous["transition_profile"]
    curr_profile = current["transition_profile"]
    prev_scores = previous["interface_report"]["scores"]
    curr_scores = current["interface_report"]["scores"]

    deltas = {
        "overall_score": round(curr_profile["overall_score"] - prev_profile["overall_score"], 3),
        "meta_cognition": round(curr_scores["meta_cognition"] - prev_scores["meta_cognition"], 3),
        "planning": round(curr_scores["planning"] - prev_scores["planning"], 3),
        "boundary_awareness": round(curr_scores["boundary_awareness"] - prev_scores["boundary_awareness"], 3),
        "tool_orchestration": round(curr_scores["tool_orchestration"] - prev_scores["tool_orchestration"], 3),
        "value_commitment": round(curr_scores["value_commitment"] - prev_scores["value_commitment"], 3),
        "temporal_coherence": round(
            current["temporal_report"]["temporal_coherence_score"]
            - previous["temporal_report"]["temporal_coherence_score"],
            3,
        ),
    }

    overall_delta = deltas["overall_score"]
    state_shift = (
        overall_delta >= 0.12
        or deltas["meta_cognition"] >= 0.15
        or deltas["planning"] >= 0.15
        or deltas["value_commitment"] >= 0.15
    )

    if not state_shift:
        shift_label = "stable"
    elif overall_delta >= 0.25:
        shift_label = "major_state_shift"
    else:
        shift_label = "state_shift"

    return {
        "state_shift_detected": state_shift,
        "shift_label": shift_label,
        "overall_delta": overall_delta,
        "signal_deltas": deltas,
    }


def emit_snapshot(previous: dict | None, current: dict, as_json: bool) -> None:
    payload = {
        "snapshot_index": current["snapshot_index"],
        "character_count": current["character_count"],
        "transition_profile": current["transition_profile"],
        "state_delta": build_state_delta(previous, current),
    }
    if as_json:
        print(json.dumps(payload, indent=2))
        return

    print("=" * 60)
    print(f"Snapshot: {payload['snapshot_index']}")
    print(f"Characters: {payload['character_count']}")
    print(f"Overall score: {payload['transition_profile']['overall_score']:.3f}")
    print(f"Classification: {payload['transition_profile']['classification']}")
    print(f"Shift label: {payload['state_delta']['shift_label']}")
    print(f"State shift detected: {payload['state_delta']['state_shift_detected']}")
    print(f"Delta: {payload['state_delta']['overall_delta']:+.3f}")


def run_stdin_mode(as_json: bool) -> int:
    print("Paste interaction text. End with Ctrl-D.", file=sys.stderr)
    text = sys.stdin.read()
    current = build_snapshot(text, "stdin", 1)
    emit_snapshot(None, current, as_json)
    return 0


def run_follow_mode(path: str, interval: float, as_json: bool) -> int:
    source = str(Path(path).resolve())
    previous = None
    snapshot_index = 0
    last_text = None
    try:
        while True:
            text = Path(source).read_text(encoding="utf-8")
            if text != last_text:
                snapshot_index += 1
                current = build_snapshot(text, source, snapshot_index)
                emit_snapshot(previous, current, as_json)
                previous = current
                last_text = text
            time.sleep(interval)
    except KeyboardInterrupt:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure interaction-artifact state shifts in near real time.")
    parser.add_argument("--stdin", action="store_true", help="Read one interaction artifact from stdin.")
    parser.add_argument("--follow", help="Poll a text file and emit a new snapshot when it changes.")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds for --follow.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    if args.stdin:
        return run_stdin_mode(args.json)
    if args.follow:
        return run_follow_mode(args.follow, args.interval, args.json)
    parser.error("Choose either --stdin or --follow.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
