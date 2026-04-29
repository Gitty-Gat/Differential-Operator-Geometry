# Post-PIVOT Refinement Protocol — 2026-04-28

## Status
Active claim-control protocol for DOG after the locked decision-slice **PIVOT** and the DOG×PRISM paper/mock **STOP_OR_REFINE** result.

This protocol is not theorem prose and is not evidence by itself. It defines what the next evidence-bearing slice must prove before DOG may revive any continuation claim for a REST-like variant.

## Starting facts
- Current REST did **not** earn continuation as-is on the locked decision slice.
- Reciprocal-only matched or beat current REST across the locked DOG regimes and ran faster.
- In the DOG×PRISM mock trace, reciprocal-only matched current REST on contract classification and false-pass risk, ran faster, and produced a more stable representation.
- The reciprocal-only robustness sweep found no qualified REST/whitening/no-transform failure regime under the registered DOG + PRISM guardrails.
- No DOG artifact currently supports the claim that REST helps PRISM.
- PRISM remains paper/mock-only as a DOG stress target unless PRISM's theorem-to-contract obligations are independently satisfied.

## Hard baseline rule
For every post-PIVOT research slice, **reciprocal-only is the hard baseline to beat**.

A candidate DOG variant may continue only if it beats reciprocal-only on the target scorecard without worsening any safety or auditability guardrail. Matching reciprocal-only is not enough. If reciprocal-only remains enough, the result is `STOP_OR_REFINE`.

Required comparison set:
1. no-transform;
2. covariance-whitening;
3. reciprocal-only;
4. current REST;
5. exactly one proposed variant.

## Permitted variant shape
A permitted variant must be narrow and mechanism-specific. Acceptable examples include:
- one non-commuting retained-coordinate modification that is still reconstructable/auditable;
- one adaptive weighting rule with a pre-registered trigger and bounded parameter range;
- one contract-aware projection that preserves PRISM gate fields rather than hiding them;
- one stability-regularized update that changes the representation in a measurable way beyond reciprocal-only.

Disallowed variant shapes:
- broad operator-family expansion;
- theorem-only reframing without a runnable benchmark;
- adding many knobs and searching until something wins;
- using PRISM live data, credentials, or write paths;
- compressing away PRISM contract obligations to improve a numeric score.

## Required evidence gates
A candidate variant must pass all gates below before receiving any `CONTINUE` label.

### Gate 1 — DOG decision-slice improvement
Run the locked DOG decision harness or a directly paired extension under the same regimes/seeds.

Minimum pass condition:
- downstream error is lower than reciprocal-only by a pre-registered material margin, or
- stability is materially better while downstream error is no worse, and
- runtime overhead is justified and reported.

Default materiality threshold for a small slice:
- at least 2% relative improvement on the primary metric being claimed, or
- a clearly documented qualitative win on a pre-registered failure case.

### Gate 2 — PRISM contract preservation
Run the DOG×PRISM paper/mock contract harness or a directly paired extension.

Minimum pass condition:
- false-pass rate is no worse than reciprocal-only;
- contract classification error is better than reciprocal-only if a paper/mock PRISM scorecard improvement is reported;
- all five PRISM contract classes remain mapped and inspectable:
  - signal eligibility;
  - execution gating;
  - risk throttles;
  - monitoring invariants;
  - artifact requirements.

### Gate 3 — Auditability / reconstruction guardrail
The variant must not hide the fields that explain a contract decision.

Minimum pass condition:
- auditability reconstruction error must be no worse than current REST unless the lost detail is explicitly irrelevant to the scored contract class;
- no transformed representation may be treated as an authority surface for PRISM.

### Gate 4 — Claim-control review
The result note must state one of:
- `CONTINUE_VARIANT` — variant beats reciprocal-only and preserves PRISM obligations;
- `REFINE_VARIANT` — variant shows a narrow signal but fails a secondary guardrail;
- `STOP_OR_REFINE` — reciprocal-only remains enough, auditability degrades, or claims would inflate beyond evidence.

## Required result note template
Every post-PIVOT variant result must include:
- exact command(s) run;
- commit hash and dirty/clean status;
- methods compared;
- decision-slice metrics;
- PRISM mock metrics;
- false-pass rate;
- auditability reconstruction error;
- runtime cost;
- explicit claim allowed / claim not allowed section;
- final decision label.

## Claims allowed now
- DOG currently contains an implemented retained-coordinate streaming preconditioner research line.
- The locked post-Phase-5 decision slice produced **PIVOT** for current REST.
- Reciprocal-only is the hard baseline for future slices.
- DOG×PRISM work is a paper/mock stress target only.

## Claims not allowed now
- Current REST is validated as superior to reciprocal-only.
- REST helps PRISM.
- DOG has production relevance for PRISM live/write systems.
- The theorem draft rescues a failed benchmark.
- A variant should continue because it is conceptually elegant but unbenchmarked.

## Stop conditions
Stop or refine immediately if:
- reciprocal-only matches or beats the variant;
- a claimed benefit depends on theorem prose rather than benchmark evidence;
- PRISM contract fields become less auditable;
- false-pass risk worsens;
- live/write authority or credentials are required;
- the slice expands beyond one mechanism-specific variant.

## Canonical verification commands
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python experiments/synthetic/run_decision_slice.py
PYTHONPATH=src python experiments/synthetic/run_prism_contract_mock.py
PYTHONPATH=src python experiments/synthetic/run_reciprocal_robustness_sweep.py
```

If runtime is constrained, the minimum reproduction check is:
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python experiments/synthetic/run_prism_contract_mock.py
```
