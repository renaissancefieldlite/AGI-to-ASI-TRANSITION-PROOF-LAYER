#!/usr/bin/env python3
"""
Spectral-analysis protocol layer.

This module no longer presents a modelled waveform as external proof. Instead,
it does two bounded jobs:

1. validate the analysis pipeline against a known reference waveform
2. analyze an observed numeric series supplied by the user
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def generate_reference_series(
    sample_rate: float,
    duration_seconds: float = 60.0,
    base_frequency: float = 0.67,
    noise_level: float = 0.15,
) -> np.ndarray:
    time = np.arange(0, duration_seconds, 1.0 / sample_rate)
    rng = np.random.default_rng(67)
    waveform = np.sin(2 * np.pi * base_frequency * time)
    harmonic = 0.35 * np.sin(2 * np.pi * 1.084 * time)
    noise = rng.normal(0.0, noise_level, size=time.shape[0])
    return waveform + harmonic + noise


def load_numeric_series(input_path: str, column: str | None = None) -> np.ndarray:
    path = Path(input_path).resolve()
    suffix = path.suffix.lower()

    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            if column and column in payload:
                values = payload[column]
            elif "values" in payload:
                values = payload["values"]
            else:
                raise ValueError("JSON input must contain 'values' or the named column.")
        elif isinstance(payload, list):
            values = payload
        else:
            raise ValueError("Unsupported JSON signal shape.")
        return np.asarray(values, dtype=float)

    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError("CSV input must include a header row.")
            if column is None:
                numeric_candidates = [field for field in reader.fieldnames if field]
                column = numeric_candidates[-1]
            values = [float(row[column]) for row in reader if row.get(column)]
        return np.asarray(values, dtype=float)

    values = np.loadtxt(path, dtype=float)
    if values.ndim > 1:
        values = values[:, -1]
    return np.asarray(values, dtype=float)


def analyze_spectrum(values: np.ndarray, sample_rate: float, target_frequency: float = 0.67) -> dict:
    if values.size < 8:
        raise ValueError("Need at least 8 samples for spectral analysis.")

    centered = values - np.mean(values)
    freqs = np.fft.rfftfreq(centered.size, d=1.0 / sample_rate)
    spectrum = np.abs(np.fft.rfft(centered))

    if spectrum.size <= 1:
        raise ValueError("Spectrum is too small to analyze.")

    spectrum[0] = 0.0
    dominant_index = int(np.argmax(spectrum))
    dominant_frequency = float(freqs[dominant_index])
    dominant_amplitude = float(spectrum[dominant_index])
    noise_floor = float(np.median(spectrum[1:])) if spectrum.size > 1 else 0.0
    snr_ratio = dominant_amplitude / max(noise_floor, 1e-9)
    frequency_error = abs(dominant_frequency - target_frequency)
    target_alignment = max(0.0, 1.0 - (frequency_error / max(target_frequency, 1e-9)))

    return {
        "sample_count": int(values.size),
        "dominant_frequency_hz": dominant_frequency,
        "dominant_amplitude": dominant_amplitude,
        "noise_floor": noise_floor,
        "snr_ratio": round(float(snr_ratio), 3),
        "target_frequency_hz": target_frequency,
        "frequency_error_hz": round(float(frequency_error), 6),
        "target_alignment_score": round(float(target_alignment), 3),
    }


def build_spectral_report(
    input_path: str | None = None,
    column: str | None = None,
    sample_rate: float = 50.0,
    target_frequency: float = 0.67,
) -> dict:
    if input_path:
        values = load_numeric_series(input_path, column=column)
        signal_origin = {
            "mode": "observed_series",
            "source_path": str(Path(input_path).resolve()),
            "note": "User-supplied data. Interpretation depends on upstream capture quality.",
        }
    else:
        values = generate_reference_series(sample_rate=sample_rate, base_frequency=target_frequency)
        signal_origin = {
            "mode": "reference_model",
            "source_path": "generated_in_memory",
            "note": "Reference waveform used to validate the analysis pipeline, not to prove external phenomena.",
        }

    analysis = analyze_spectrum(values, sample_rate=sample_rate, target_frequency=target_frequency)
    analysis["signal_origin"] = signal_origin
    analysis["notes"] = [
        "A detected frequency in reference mode validates the pipeline only.",
        "Observed-series mode is where this module becomes useful for downstream measurement layers.",
    ]
    return analysis


def main() -> dict:
    parser = argparse.ArgumentParser(description="Run spectral analysis on a reference or observed signal.")
    parser.add_argument("--input", help="Optional path to a txt/csv/json numeric series.")
    parser.add_argument("--column", help="Named CSV or JSON column.")
    parser.add_argument("--sample-rate", type=float, default=50.0, help="Sample rate in Hz.")
    parser.add_argument("--target-frequency", type=float, default=0.67, help="Reference target frequency.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    report = build_spectral_report(
        input_path=args.input,
        column=args.column,
        sample_rate=args.sample_rate,
        target_frequency=args.target_frequency,
    )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Quantum State Proof")
        print("=" * 60)
        print(f"Signal origin: {report['signal_origin']['mode']}")
        print(f"Peak frequency: {report['dominant_frequency_hz']:.4f} Hz")
        print(f"SNR ratio: {report['snr_ratio']:.3f}")
        print(f"Target alignment: {report['target_alignment_score']:.3f}")
    return report


if __name__ == "__main__":
    main()
