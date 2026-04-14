# Differential Operator Geometry

## Project overview
Differential Operator Geometry (DOG) is a research repository centered on the current, narrower REST line:

> **REST as a covariance-based streaming geometric preconditioner in retained spectral coordinates, with partial one-step stability formalization and controlled synthetic support.**

The broader "geometry as the mechanism of computation" motivation remains part of the project history, but it is **not** the main claim presently supported by the repository.

In the active implementation, REST should be understood primarily as a retained-coordinate spectral preconditioning pipeline built from streaming covariance structure. In that setting, the reciprocal and exponential components act as commuting diagonal reweightings, so the repo does **not** currently claim that stage ordering is independently established as the key source of benefit.

## Purpose
This repository is currently focused on a disciplined narrowed research program:
- maintain the covariance-based REST implementation as the canonical path,
- document the strongest honest contribution and its limits,
- tighten method/theorem language so it matches the implemented operator,
- preserve synthetic evaluation artifacts and compact empirical lessons,
- and support a few targeted follow-up validation slices before any broader expansion.

## Current stage
**Stage:** Active narrowed research program after Phase 5 reframing

What exists now:
- a covariance-based REST implementation under `src/rest/`,
- tests, synthetic experiments, metrics, and generated figures,
- Phase 4 empirical notes showing mixed-but-real viability under controlled drift,
- Phase 5 reframing documents that narrow the contribution to the retained-coordinate preconditioner view,
- repo control docs (`PROJECT_STATUS.md`, `ROADMAP.md`, `WORKLOG.md`, `NEXT_ACTIONS.md`) that keep future slices honest and small.

What does not yet exist:
- a completed proof beyond draft level,
- support for a strong ordering-sensitive novelty claim in the active architecture,
- large-scale or real-world benchmark validation,
- broad operator-family generalization beyond the covariance case.

## High-level idea summary
The current repo-level summary is:

> DOG studies REST as a covariance-based streaming geometric preconditioner built in retained spectral coordinates. The main question is whether that preconditioning view yields useful behavior in some controlled streaming regimes, together with a modest one-step stability story, rather than whether it proves a universal geometry-first mechanism of computation.

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
1. tighten `docs/project-plan/REST_METHOD_NOTE.md` so it matches the implemented retained-coordinate covariance path,
2. review `docs/project-plan/REST_THEOREM_DRAFT.md` only for bounded proof-detail or constant cleanup,
3. run one narrow validation slice tied to a concrete preconditioning question,
4. revisit the non-commuting variant only if the trigger conditions in `DECISIONS.md` are met,
5. avoid broad real-world expansion until the narrowed contribution is better supported.

## Project control
- Status: [`PROJECT_STATUS.md`](PROJECT_STATUS.md)
- Setup: [`SETUP.md`](SETUP.md)
- Decisions: [`DECISIONS.md`](DECISIONS.md)
- Roadmap: [`ROADMAP.md`](ROADMAP.md)
- Worklog: [`WORKLOG.md`](WORKLOG.md)
- Short queue: [`docs/project-plan/NEXT_ACTIONS.md`](docs/project-plan/NEXT_ACTIONS.md)
- Positioning note: [`docs/project-plan/PRECONDITIONER_POSITIONING_NOTE.md`](docs/project-plan/PRECONDITIONER_POSITIONING_NOTE.md)
