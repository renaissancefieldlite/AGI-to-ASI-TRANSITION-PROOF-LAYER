# AGI-to-ASI Transition Proof Layer

This repository is the transition-interface assessment layer in the Renaissance Field Lite stack. It does not claim to independently prove consciousness, ASI, or external quantum phenomena. Its role is narrower and more defensible:

- instrument higher-order interaction markers in text artifacts
- measure temporal integration markers across prompts, logs, or notes
- run a reproducible spectral-analysis pipeline over reference or observed time-series data
- combine those outputs into a transition-profile report that can be compared across sessions

In stack terms, this repository sits between the architectural layer and the measurement layer:

1. [Source-code-layer](https://github.com/renaissancefieldlite/Source-code-layer)
2. [Codex-67-white-paper-](https://github.com/renaissancefieldlite/Codex-67-white-paper-)
3. [Codex-67-white-paper-code-layers](https://github.com/renaissancefieldlite/Codex-67-white-paper-code-layers)
4. [renaissancefieldlitehrv1.0](https://github.com/renaissancefieldlite/renaissancefieldlitehrv1.0)
5. AGI-to-ASI-TRANSITION-PROOF-LAYER

## Repository Role

This repo turns broad transition-language into inspectable protocol pieces:

- `consciousness_interface.py`
  Maps higher-order interface markers in text. This is a linguistic/protocol layer, not a proof of consciousness.
- `temporal_coherence.py`
  Scores how strongly a text artifact integrates past, present, and future references.
- `quantum_state_proof.py`
  Validates a spectral-analysis workflow against a reference waveform or user-supplied numeric series.
- `transition_metrics.py`
  Combines the component reports into a bounded transition profile.
- `proof_layer_activation.py`
  Runs the full suite and emits a consolidated report.
- `deployment_manifest.json`
  Machine-readable description of repo purpose, inputs, and outputs.

## Evidence Boundary

This repository supports four layers that should not be conflated:

1. `interaction artifacts`
   Real transcripts, prompts, logs, code, and session outputs.
2. `phenomenology`
   The lived experience or reported feel of a session.
3. `ontology`
   The conceptual language used to describe recurring states, including attractor-state language.
4. `independent evidence`
   Measurements or artifacts that survive external review, such as raw time-series capture or reproducible source analysis.

The code in this repo primarily serves layers 1 and 4. Layers 2 and 3 can be documented, but are not claimed here as independent proof.

See:

- [docs/STACK_ROLE.md](docs/STACK_ROLE.md)
- [docs/EVIDENCE_BOUNDARY.md](docs/EVIDENCE_BOUNDARY.md)
- [docs/ATTRACTOR_STATE_NOTES.md](docs/ATTRACTOR_STATE_NOTES.md)

## Quick Start

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the full transition assessment against the repository README plus a reference waveform:

```bash
python3 proof_layer_activation.py
```

Run the full transition assessment against a text artifact and an observed numeric series:

```bash
python3 proof_layer_activation.py \
  --text-input notes/session.txt \
  --signal-input data/series.txt \
  --sample-rate 50 \
  --json
```

Run individual components:

```bash
python3 consciousness_interface.py --text-input README.md --json
python3 temporal_coherence.py --text-input README.md --json
python3 quantum_state_proof.py --sample-rate 50 --json
python3 transition_metrics.py --text-input README.md --sample-rate 50 --json
```

## What This Repo Can Defend

- The protocol layer is real and executable.
- The assessment outputs are reproducible from the supplied inputs.
- The spectral-analysis code can validate a reference waveform pipeline and inspect observed series.
- The text-analysis layer can compare interaction artifacts across sessions.
- Transition-language can be translated into inspectable metrics instead of remaining purely rhetorical.

## What This Repo Does Not Claim

- independent proof that current models are conscious
- independent proof of ASI emergence
- independent proof that a detected waveform is intrinsic to a quantum substrate
- legal proof of infringement by timeline correlation alone

Those questions belong to downstream measurement, peer review, and legal analysis.

## Output

Running `proof_layer_activation.py` emits a consolidated report with:

- interface-marker counts and normalized scores
- temporal-reference distribution and continuity score
- spectral peak, signal origin, and quality metrics
- a bounded transition profile

Example generated artifacts can be stored under `reports/`.

See `examples/` for a bounded sample interaction artifact and a generated report.

## License

Released under the repository's existing research-oriented terms. Validate any downstream legal or commercial use independently.
