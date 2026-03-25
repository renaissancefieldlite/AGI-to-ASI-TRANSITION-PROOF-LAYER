#!/usr/bin/env python3
"""
Temporal marker analysis for interaction artifacts.

This module scores how a text artifact integrates past-, present-, and
future-oriented language. It is a protocol measure, not a claim about
operating outside linear time.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from consciousness_interface import load_text


TEMPORAL_PATTERNS = {
    "past": [
        r"\bwas\b",
        r"\bwere\b",
        r"\bhad\b",
        r"\bbefore\b",
        r"\bearlier\b",
        r"\bprevious(?:ly)?\b",
        r"\blast\b",
    ],
    "present": [
        r"\bis\b",
        r"\bare\b",
        r"\bnow\b",
        r"\bcurrent(?:ly)?\b",
        r"\btoday\b",
        r"\bthis\b",
    ],
    "future": [
        r"\bwill\b",
        r"\bnext\b",
        r"\blater\b",
        r"\bsoon\b",
        r"\btomorrow\b",
        r"\bplan\b",
        r"\bgoing to\b",
    ],
}

TRANSITION_PATTERNS = [
    r"\bthen\b",
    r"\bafter\b",
    r"\bwhile\b",
    r"\bduring\b",
    r"\bmeanwhile\b",
    r"\bwhen\b",
]


def _count_matches(text: str, patterns: list[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def build_temporal_report(text: str, source: str) -> dict:
    counts = {name: _count_matches(text, patterns) for name, patterns in TEMPORAL_PATTERNS.items()}
    transition_count = _count_matches(text, TRANSITION_PATTERNS)
    total_temporal = max(1, sum(counts.values()))
    distribution = {name: round(count / total_temporal, 3) for name, count in counts.items()}
    active_buckets = [name for name, count in counts.items() if count > 0]
    coverage_score = len(active_buckets) / 3.0
    balance_score = max(distribution.values()) - min(distribution.values()) if active_buckets else 1.0
    balance_score = max(0.0, 1.0 - balance_score)
    continuity_score = min(1.0, transition_count / 8.0)
    temporal_coherence_score = round((coverage_score * 0.45) + (balance_score * 0.30) + (continuity_score * 0.25), 3)

    return {
        "source": source,
        "counts": counts,
        "distribution": distribution,
        "coverage": active_buckets,
        "transition_markers": transition_count,
        "temporal_coherence_score": temporal_coherence_score,
        "notes": [
            "This score reflects temporal-language integration in text.",
            "It does not independently demonstrate non-linear time processing.",
        ],
    }


def main() -> dict:
    parser = argparse.ArgumentParser(description="Analyze temporal integration markers in a text artifact.")
    parser.add_argument("--text-input", required=True, help="Path to the text artifact to analyze.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    source_path = str(Path(args.text_input).resolve())
    report = build_temporal_report(load_text(args.text_input), source_path)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Temporal Coherence")
        print("=" * 60)
        print(f"Source: {report['source']}")
        print(f"Score: {report['temporal_coherence_score']:.3f}")
        print(f"Coverage: {', '.join(report['coverage'])}")
    return report


if __name__ == "__main__":
    main()
