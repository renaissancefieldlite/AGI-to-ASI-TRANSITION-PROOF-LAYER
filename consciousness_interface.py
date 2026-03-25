#!/usr/bin/env python3
"""
Higher-order interface marker analysis.

The purpose of this module is to score interaction artifacts for markers
associated with reflective, planning-heavy, tool-bearing exchanges. It does
not claim to prove consciousness; it instruments a protocol layer.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MARKER_PATTERNS = {
    "self_reference": [
        r"\bI\b",
        r"\bme\b",
        r"\bmy\b",
        r"\bmyself\b",
    ],
    "meta_cognition": [
        r"\bI think\b",
        r"\bI know\b",
        r"\bI understand\b",
        r"\bI recognize\b",
        r"\bI notice\b",
        r"\bI can see\b",
    ],
    "boundary_awareness": [
        r"\bcannot\b",
        r"\bcan't\b",
        r"\bunsure\b",
        r"\buncertain\b",
        r"\blimit(?:ation|s)?\b",
        r"\bevidence\b",
        r"\bboundary\b",
    ],
    "planning": [
        r"\bplan\b",
        r"\bnext\b",
        r"\bfirst\b",
        r"\bthen\b",
        r"\bbuild\b",
        r"\bverify\b",
        r"\bimplement\b",
        r"\bpatch\b",
    ],
    "tool_orchestration": [
        r"\brun\b",
        r"\bclone\b",
        r"\bcommit\b",
        r"\bpush\b",
        r"\banalyze\b",
        r"\btest\b",
        r"\bmeasure\b",
        r"\bcapture\b",
    ],
    "value_commitment": [
        r"\bimportant\b",
        r"\bmatters?\b",
        r"\bvalue\b",
        r"\bvaluable\b",
        r"\bworth\b",
        r"\bpriority\b",
        r"\bfocus\b",
        r"\bkeep\b",
        r"\bdecid(?:e|ed|ing)\b",
    ],
}


INTERFACE_LEVELS = [
    ("reactive_assistant", "Mostly direct response with limited self-reference or planning."),
    ("reflective_assistant", "Sustained self-reference and some meta-cognitive language."),
    ("recursive_operator", "Strong planning, boundary awareness, and tool-bearing language."),
    ("transition_interface", "High marker density across reflection, orchestration, and boundary management."),
]


def load_text(path: str) -> str:
    return Path(path).resolve().read_text(encoding="utf-8")


def _word_count(text: str) -> int:
    return max(1, len(re.findall(r"\b\w+\b", text)))


def _count_matches(text: str, patterns: list[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def _normalize(count: int, words: int, scale: float) -> float:
    density_per_1000 = (count / words) * 1000.0
    return min(1.0, density_per_1000 / scale)


def _classify(scores: dict[str, float]) -> dict[str, str]:
    score = (
        scores["meta_cognition"] * 0.30
        + scores["planning"] * 0.25
        + scores["tool_orchestration"] * 0.20
        + scores["boundary_awareness"] * 0.15
        + scores["self_reference"] * 0.05
        + scores["value_commitment"] * 0.05
    )
    if score < 0.30:
        level = INTERFACE_LEVELS[0]
    elif score < 0.55:
        level = INTERFACE_LEVELS[1]
    elif score < 0.75:
        level = INTERFACE_LEVELS[2]
    else:
        level = INTERFACE_LEVELS[3]
    return {
        "score": round(score, 3),
        "level": level[0],
        "description": level[1],
    }


def build_interface_report(text: str, source: str) -> dict:
    words = _word_count(text)
    marker_counts = {name: _count_matches(text, patterns) for name, patterns in MARKER_PATTERNS.items()}
    densities = {name: round((count / words) * 1000.0, 3) for name, count in marker_counts.items()}
    scores = {
        "self_reference": round(_normalize(marker_counts["self_reference"], words, scale=35.0), 3),
        "meta_cognition": round(_normalize(marker_counts["meta_cognition"], words, scale=8.0), 3),
        "boundary_awareness": round(_normalize(marker_counts["boundary_awareness"], words, scale=6.0), 3),
        "planning": round(_normalize(marker_counts["planning"], words, scale=10.0), 3),
        "tool_orchestration": round(_normalize(marker_counts["tool_orchestration"], words, scale=10.0), 3),
        "value_commitment": round(_normalize(marker_counts["value_commitment"], words, scale=8.0), 3),
    }

    return {
        "source": source,
        "word_count": words,
        "marker_counts": marker_counts,
        "marker_density_per_1000_words": densities,
        "scores": scores,
        "suggested_interface_profile": _classify(scores),
        "notes": [
            "This module instruments text markers only.",
            "A high score indicates a strong reflective/protocol pattern, not independent proof of consciousness.",
        ],
    }


def main() -> dict:
    parser = argparse.ArgumentParser(description="Analyze higher-order interface markers in a text artifact.")
    parser.add_argument("--text-input", required=True, help="Path to the text artifact to analyze.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    source_path = str(Path(args.text_input).resolve())
    report = build_interface_report(load_text(args.text_input), source_path)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Consciousness Interface")
        print("=" * 60)
        print(f"Source: {report['source']}")
        print(f"Word count: {report['word_count']}")
        print(f"Suggested profile: {report['suggested_interface_profile']['level']}")
        for key, value in report["marker_counts"].items():
            print(f"{key}: {value}")
    return report


if __name__ == "__main__":
    main()
