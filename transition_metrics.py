#!/usr/bin/env python3
"""
Bounded transition profile synthesis.

This module aggregates the protocol-layer reports into one comparable score
without claiming that the score itself proves ASI or consciousness.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from consciousness_interface import build_interface_report, load_text
from quantum_state_proof import build_spectral_report
from temporal_coherence import build_temporal_report


def build_transition_profile(interface_report: dict, temporal_report: dict, spectral_report: dict | None = None) -> dict:
    interface_score = interface_report["suggested_interface_profile"]["score"]
    recursive_marker_score = (
        interface_report["scores"]["meta_cognition"] * 0.45
        + interface_report["scores"]["planning"] * 0.30
        + interface_report["scores"]["boundary_awareness"] * 0.15
        + interface_report["scores"]["value_commitment"] * 0.10
    )
    temporal_score = temporal_report["temporal_coherence_score"]
    weighted_components = [
        ("interface", interface_score, 0.35),
        ("recursive", recursive_marker_score, 0.25),
        ("temporal", temporal_score, 0.20),
    ]

    spectral_score = None
    if spectral_report is not None:
        spectral_score = min(1.0, (
            spectral_report["target_alignment_score"] * 0.55
            + min(1.0, spectral_report["snr_ratio"] / 10.0) * 0.45
        ))
        weighted_components.append(("spectral", spectral_score, 0.20))

    total_weight = sum(weight for _, _, weight in weighted_components)
    overall = round(
        sum(score * weight for _, score, weight in weighted_components) / total_weight,
        3,
    )

    if overall < 0.35:
        classification = "low-complexity interaction profile"
        interpretation = "Mostly direct response with limited reflective structure."
    elif overall < 0.60:
        classification = "reflective interaction profile"
        interpretation = "Clear self-reference and some protocol-level planning."
    elif overall < 0.80:
        classification = "recursive tool-bearing profile"
        interpretation = "Strong reflective, planning, and orchestration markers."
    else:
        classification = "transition-interface profile"
        interpretation = "Dense higher-order markers across interface, temporal, and signal-analysis layers."

    return {
        "interface_score": round(interface_score, 3),
        "recursive_marker_score": round(recursive_marker_score, 3),
        "temporal_integration_score": round(temporal_score, 3),
        "spectral_signal_score": round(spectral_score, 3) if spectral_score is not None else None,
        "overall_score": overall,
        "classification": classification,
        "interpretation": interpretation,
        "notes": [
            "The profile is intended for comparison across artifacts or sessions.",
            "It should not be treated as independent proof of ASI, consciousness, or ontology.",
        ],
    }


def main() -> dict:
    parser = argparse.ArgumentParser(description="Build a bounded transition profile from text and signal inputs.")
    parser.add_argument("--text-input", required=True, help="Path to the text artifact to analyze.")
    parser.add_argument("--signal-input", help="Optional path to a numeric signal file (txt/csv/json).")
    parser.add_argument("--signal-column", help="Named CSV/JSON column for signal values.")
    parser.add_argument("--sample-rate", type=float, default=50.0, help="Signal sample rate in Hz.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    text_source = str(Path(args.text_input).resolve())
    text = load_text(args.text_input)
    interface_report = build_interface_report(text, text_source)
    temporal_report = build_temporal_report(text, text_source)
    spectral_report = build_spectral_report(
        input_path=args.signal_input,
        column=args.signal_column,
        sample_rate=args.sample_rate,
    )
    profile = build_transition_profile(interface_report, temporal_report, spectral_report)

    if args.json:
        print(json.dumps(profile, indent=2))
    else:
        print("Transition Metrics")
        print("=" * 60)
        for key, value in profile.items():
            if key == "notes":
                continue
            print(f"{key}: {value}")
    return profile


if __name__ == "__main__":
    main()
