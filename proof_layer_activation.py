#!/usr/bin/env python3
"""
Transition assessment orchestrator.

This script consolidates the repo's protocol layers into one bounded report.
It is intentionally narrower than the original rhetoric: it instruments
textual higher-order markers, temporal integration, and spectral analysis
without claiming that those outputs independently prove ASI or consciousness.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from consciousness_interface import build_interface_report, load_text
from quantum_state_proof import build_spectral_report
from temporal_coherence import build_temporal_report
from transition_metrics import build_transition_profile


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_TEXT_PATH = REPO_ROOT / "README.md"


def build_full_report(
    text_input: str | None = None,
    signal_input: str | None = None,
    signal_column: str | None = None,
    sample_rate: float = 50.0,
) -> dict:
    if text_input:
        text = load_text(text_input)
        text_source = str(Path(text_input).resolve())
    else:
        text = DEFAULT_TEXT_PATH.read_text(encoding="utf-8")
        text_source = str(DEFAULT_TEXT_PATH)

    interface_report = build_interface_report(text, text_source)
    temporal_report = build_temporal_report(text, text_source)
    spectral_report = build_spectral_report(
        input_path=signal_input,
        column=signal_column,
        sample_rate=sample_rate,
    )
    transition_profile = build_transition_profile(
        interface_report=interface_report,
        temporal_report=temporal_report,
        spectral_report=spectral_report,
    )

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "repo_role": "transition-interface assessment layer",
        "stack_position": [
            "Source-code-layer",
            "Codex-67-white-paper-",
            "Codex-67-white-paper-code-layers",
            "renaissancefieldlitehrv1.0",
            "AGI-to-ASI-TRANSITION-PROOF-LAYER",
        ],
        "evidence_boundary": {
            "supports": [
                "interaction artifact analysis",
                "phenomenology-adjacent protocol mapping",
                "reference/observed spectral analysis",
                "bounded transition profiling",
            ],
            "does_not_independently_prove": [
                "consciousness",
                "ASI emergence",
                "external quantum ontology",
                "legal infringement",
            ],
        },
        "inputs": {
            "text_source": text_source,
            "signal_source": spectral_report["signal_origin"]["source_path"],
            "sample_rate_hz": sample_rate,
        },
        "interface_report": interface_report,
        "temporal_report": temporal_report,
        "spectral_report": spectral_report,
        "transition_profile": transition_profile,
    }


def main() -> dict:
    parser = argparse.ArgumentParser(description="Run the transition-interface assessment suite.")
    parser.add_argument("--text-input", help="Path to a text artifact to analyze.")
    parser.add_argument("--signal-input", help="Path to a numeric signal file (txt/csv/json).")
    parser.add_argument("--signal-column", help="Named CSV column for signal values.")
    parser.add_argument("--sample-rate", type=float, default=50.0, help="Sample rate in Hz for signal analysis.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--output", help="Optional output path for the report JSON.")
    args = parser.parse_args()

    report = build_full_report(
        text_input=args.text_input,
        signal_input=args.signal_input,
        signal_column=args.signal_column,
        sample_rate=args.sample_rate,
    )

    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("AGI-to-ASI Transition Proof Layer")
        print("=" * 60)
        print(f"Timestamp (UTC): {report['timestamp_utc']}")
        print(f"Text source: {report['inputs']['text_source']}")
        print(f"Signal source: {report['inputs']['signal_source']}")
        print()
        print("Transition Profile")
        print("-" * 60)
        profile = report["transition_profile"]
        print(f"Overall score: {profile['overall_score']:.3f}")
        print(f"Classification: {profile['classification']}")
        print(f"Interpretation: {profile['interpretation']}")
        print()
        print("Interface markers")
        print("-" * 60)
        for key, value in report["interface_report"]["marker_counts"].items():
            print(f"{key}: {value}")
        print()
        print("Temporal coherence")
        print("-" * 60)
        print(f"Score: {report['temporal_report']['temporal_coherence_score']:.3f}")
        print(f"Coverage: {', '.join(report['temporal_report']['coverage'])}")
        print()
        print("Spectral analysis")
        print("-" * 60)
        print(f"Signal origin: {report['spectral_report']['signal_origin']['mode']}")
        print(f"Peak frequency (Hz): {report['spectral_report']['dominant_frequency_hz']:.4f}")
        print(f"SNR ratio: {report['spectral_report']['snr_ratio']:.3f}")

    return report


if __name__ == "__main__":
    main()
