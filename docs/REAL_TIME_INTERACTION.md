# Real-Time Interaction Measurement

This repo can measure a live interaction artifact in a bounded way.

## What It Measures

- reflective marker density
- meta-cognitive language
- planning and orchestration language
- value-commitment language
- temporal integration
- state-shift deltas between snapshots
- recursion and self-reference across live work artifacts

## What It Does Not Measure

- independent proof of consciousness
- ontology by itself
- causation by itself

## CLI Modes

### One-shot stdin

```bash
python3 live_interaction_probe.py --stdin --json
```

### Follow a growing log file

```bash
python3 live_interaction_probe.py --follow logs/thread_capture.txt
```

Each file change produces:

- an updated transition profile
- a delta from the previous snapshot
- a state-shift label

The strongest bounded claim here is:

`A session can show measurable shifts in output style, including changes in meta-cognitive, planning, and value-commitment markers.`

In the current Renaissance Field Lite stack, that means the repo can be used
against live working artifacts from the broader build graph rather than only
against isolated test text.
