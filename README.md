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
**Stage:** Early research with Phase 1 complete, Phase 2 formalized at draft level, Phase 3 implemented, and Phase 4 evaluation completed

What exists now:
- primary conceptual draft material,
- secondary critique and research-planning notes,
- repository-level synthesis and evaluation documents,
- Phase 1 concept, literature-positioning, canonical-decision, idea-paper, and execution-plan documents,
- Phase 2 formal method and theorem draft documents,
- Phase 3 implementation code, tests, synthetic experiments, metrics, and evaluation note,
- Phase 4 ablation, downstream-task, traceability, figure, threshold, and recommendation artifacts.

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

## Planned next work
With Phase 4 completed, the immediate next steps are:
1. refine the novelty framing in light of the ordering-ablation result,
2. decide whether REST should be positioned more explicitly as a geometric preconditioner,
3. tighten the Phase 2 theorem draft so it matches the actual implementation regime and diagnostics,
4. only after that, decide whether broader operator families or real-world datasets are warranted.
