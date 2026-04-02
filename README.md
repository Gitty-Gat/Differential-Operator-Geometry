# Differential Operator Geometry

## Project overview
Differential Operator Geometry (DOG) is an early-stage research repository investigating whether **evolving local geometry** can serve as the mechanism of computation for streaming data analysis.

The current working method inside that broader concept is **REST** (Reciprocal–Exponential Spectral Transforms). REST applies a two-stage local spectral pipeline:
1. reciprocal flattening to damp curvature-driven or anisotropic distortion,
2. exponential lifting to restore controlled structure in a stable working representation.

The proposed outcome is a Euclidean analysis space that updates with the stream rather than assuming a fixed geometry from the start.

## Purpose
This repository is currently focused on bootstrap-stage research organization:
- archive and normalize early source materials,
- extract the core mathematical idea,
- document the current synthesis of the project,
- record critical risks and open questions,
- and establish a clean structure for future theory and experimental work.

## Current stage
**Stage:** Early research with Phase 1–4 completed and Phase 5 reframing completed

What exists now:
- primary conceptual draft material,
- secondary critique and research-planning notes,
- repository-level synthesis and evaluation documents,
- Phase 1 concept, literature-positioning, canonical-decision, idea-paper, and execution-plan documents,
- Phase 2 formal method and theorem draft documents,
- Phase 3 implementation code, tests, synthetic experiments, metrics, and evaluation note,
- Phase 4 ablation, downstream-task, traceability, figure, threshold, and recommendation artifacts,
- Phase 5 reframing, theory-alignment, and scope-decision documents.

What does not yet exist:
- completed proofs beyond draft level,
- large-scale or real-world experimental benchmarks,
- validated downstream application claims beyond controlled synthetic tasks,
- broader operator-family implementations beyond the covariance case.

## High-level idea summary
The repository's source materials support the following project summary:

> DOG is a research program in which data is treated as living in a changing local geometry rather than a fixed vector space. REST is the current candidate operator pipeline for that idea: it builds a local spectral model from streaming data, applies reciprocal flattening to suppress distortion, then applies exponential lifting to restore controlled geometric structure. The goal is a stable, geometry-aware Euclidean working representation for downstream computation.

## Repository structure

```text
Differential-Operator-Geometry/
├── README.md
├── docs/
│   ├── source-material/
│   │   ├── Abstract.txt
│   │   ├── DOG_research_notes.txt
│   │   └── chatgpt_conversation.md
│   └── project-plan/
│       ├── SOURCE_AUDIT.md
│       ├── PROJECT_SYNTHESIS.md
│       └── CRITICAL_EVALUATION.md
├── theory/
├── src/
├── tests/
└── experiments/
```

## Notes on source normalization
The original instructions referenced `Abstract.docx`, but the active source file supplied during bootstrap was converted to plain text as `abstract.txt`. The repository therefore archives the canonical source under:

- `docs/source-material/Abstract.txt`

This preserves traceability to the actual source material used during bootstrap.

## Phase 4 summary
Phase 4 strengthened the empirical and diagnostic picture and led to a clear recommendation:

- REST remains computationally viable and empirically distinguishable from simple baselines.
- The strongest current limitation is architectural: in the retained-coordinate diagonal formulation, the reciprocal and exponential maps commute, so the ordering hypothesis is not empirically distinguishable as a separate source of benefit.
- The current recommendation is therefore **REFINE**, not scale blindly.

Example Phase 4 artifact:

![Phase 4 stability-vs-beta figure](experiments/results/figures/stability_vs_beta.svg)

## Planned next work
With Phase 5 completed, the immediate next steps are:
1. continue under the geometric-preconditioner framing,
2. tighten proof details and constants for the one-step stability result,
3. optionally run one bounded non-commuting-variant spike only if restoring an ordering-sensitive mechanism remains strategically important,
4. otherwise prioritize narrow, defensible validation in domains where preconditioning is likely to matter,
5. avoid broad real-world expansion until the scope decision is revisited with stronger evidence.
