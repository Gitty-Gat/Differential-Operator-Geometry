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
**Stage:** Early research / bootstrap with Phase 1 planning completed

What exists now:
- primary conceptual draft material,
- secondary critique and research-planning notes,
- repository-level synthesis and evaluation documents,
- Phase 1 concept, literature-positioning, canonical-decision, and idea-paper planning documents,
- a Phase 2 formalization plan.

What does not yet exist:
- formal proofs,
- implementation code,
- experimental benchmarks,
- validated empirical claims.

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
With Phase 1 now completed at the documentation level, the immediate next steps are:
1. formalize the canonical covariance-based REST formulation,
2. standardize notation and write the method note,
3. prove one rigorous single-step stability/distortion result,
4. implement minimal synthetic benchmarks,
5. evaluate the method against baseline streaming approaches.
