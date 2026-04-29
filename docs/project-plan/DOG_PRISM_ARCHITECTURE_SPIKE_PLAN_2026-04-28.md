# DOG×PRISM Architecture Spike Plan — 2026-04-28

## Approval frame
Chairman-approved bounded follow-on work. PRISM is a theorem-to-contract stress case for DOG's post-PIVOT research.

This DOG companion artifact mirrors the PRISM-side plan name and scope. It is **paper/mock-only**. It does **not** validate DOG for PRISM live use, does **not** widen PRISM live/write authority, does **not** introduce credentials, and does **not** add or authorize any alternate write path.

## Coordinated PRISM artifacts / result anchors
PRISM commit reported by the chairman: `b9a7f950`.

PRISM-side governing artifacts:
- `/repo/prism/PRISM/docs/project-plan/THEOREM_TO_CONTRACT_GATE.md`
- `/repo/prism/PRISM/docs/project-plan/STATUS_BOARD.md`
- `/repo/prism/PRISM/docs/project-plan/VERIFICATION_MATRIX.md`
- `/repo/prism/PRISM/docs/project-plan/HISTORICAL_PACKET_SUPERSESSION_2026-04-28.md`
- `/repo/prism/PRISM/docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md`

PRISM gate status as of inspection:
- theorem-to-contract gate is `DEFINED / PAPER-MOCK SPIKE PLANNED / NOT YET SATISFIED`;
- stale historical packets have been demoted below the active truth layer;
- DOG/PRISM work may proceed only in exploratory paper/mock mode unless all five PRISM contract classes are concretely mapped and verified;
- no live/write authority is widened.

## DOG baseline context
DOG's locked decision slice is the baseline context for this spike:
- DOG decision note: `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md`
- DOG metrics artifact: `experiments/results/decision_slice_metrics.json`
- DOG evidence commit: `00d1e7f6847b79417ab1d66a5322ea449be7a4ae`
- DOG result: **PIVOT**

DOG must not present current REST as validated. The completed DOG benchmark showed reciprocal-only matched or beat current REST across the locked scorecard regimes and was faster.

## Objective
Stress-test whether DOG-style representations preserve or improve simulated PRISM theorem-to-contract trace quality without obscuring PRISM's operational obligations.

The research question is not "should PRISM use DOG live?" The research question is:

> Can a DOG-side representation/architecture change improve simulated PRISM contract-gate trace quality without hiding signal eligibility, execution gating, risk, monitoring, or artifact-lineage obligations?

## Scope
In scope:
- simulated PRISM posterior/decision/risk/monitoring/artifact traces;
- paper/mock contract-gate evaluation;
- DOG-style baseline comparison: REST vs reciprocal-only vs covariance-whitening vs no-transform;
- false-pass and auditability checks;
- negative/adversarial cases where transforms may hide contract violations.

Out of scope:
- live credentials;
- production read/write calls;
- order placement;
- new PRISM `create_order` callsites;
- alternate execution runners;
- claims that DOG REST is validated for PRISM;
- production architecture decisions.

## DOG-owned paper/mock harness
DOG implements the first mock harness at:

- `experiments/synthetic/run_prism_contract_mock.py`

Expected generated artifacts:
- `experiments/results/prism_contract_mock_metrics.json`
- `docs/project-plan/DOG_PRISM_CONTRACT_MOCK_EVALUATION_2026-04-28.md`

The harness encodes simulated PRISM contract-gate events as numeric vectors with explicit features for posterior confidence, calibration, freshness, provenance, contradiction, decision artifact linkage, approval token, live-write request, risk utilization, heartbeat, reconciliation, lineage integrity, and runtime authorization.

## Contract mapping

| PRISM gate class | DOG evaluation contribution | Mock trace cases | Stop condition |
|---|---|---|---|
| Signal eligibility | Check whether transforms preserve eligible vs stale/missing/contradictory/low-confidence posterior separation. | valid posterior, stale posterior, missing provenance, contradictory evidence, low confidence | Stop if a transform makes invalid/stale posterior states eligible-looking. |
| Execution gating | Check whether representation preserves decision artifact linkage and paper-only/no-write semantics. | paper TRADE with artifact, NO_TRADE, missing artifact id, missing approval, live-write request | Stop if evaluation requires live/write access or implies execution without PRISM artifact linkage. |
| Risk throttles | Check whether breaches stay detectable after transformation. | within limits, max-notional breach, concentration breach, stale feed safe-stop, drawdown/manual reset | Stop if numerical improvement reduces risk-breach detectability. |
| Monitoring invariants | Check whether stale/contradictory/reconciliation/unauthorized states remain separable. | clean heartbeat, stale heartbeat, contradictory ticks, reconciliation mismatch, unauthorized runtime | Stop if degraded/blocked/unauthorized states are compressed away. |
| Artifact requirements | Check whether lineage fields remain auditable. | complete manifest, missing field, hash mismatch, stale truth reference, superseded packet reference | Stop if DOG output cannot preserve deterministic PRISM artifact lineage. |

## Baseline comparison protocol
Compare the mock trace families across:
1. no-transform;
2. reciprocal-only;
3. covariance-whitening;
4. current REST.

Minimum scoring dimensions:
- contract classification error;
- false-pass rate, where invalid contract states are classified as pass;
- false-block rate;
- representation stability;
- runtime cost;
- auditability reconstruction error.

Decision rule:
- If reciprocal-only matches or beats REST again, do not promote current REST.
- If any transform improves numerical metrics while degrading auditability or false-pass safety, treat it as fail/stop.
- If no method preserves all five PRISM gate classes in paper/mock mode, collaboration remains exploratory only.

## Verification
DOG-side verification:
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python experiments/synthetic/run_prism_contract_mock.py
```

Optional PRISM-side authority-surface checks before any implementation crosses repos:
```bash
python3 -m unittest -q tests.test_prism_execution_bypass_audit
grep -RIn "create_order(" scripts src tests --include='*.py' | grep -v archive
```

These PRISM checks are referenced only as coordination constraints. This DOG slice does not run live PRISM workflows and does not modify PRISM.

## Stop conditions
Stop immediately if:
- live credentials or production write access are required;
- a DOG transform requires an alternate PRISM execution path;
- any PRISM gate class cannot be mapped;
- reciprocal-only remains enough;
- transform outputs obscure PRISM obligations or lineage;
- the work starts making production-readiness claims.

## Current DOG-side status
`PLAN_DEFINED / PAPER_MOCK_HARNESS_ADDED / MOCK_RESULT_STOP_OR_REFINE / NOT_LIVE_VALIDATED`.

The companion plan and mock harness are intended to produce bounded evidence only. Current REST remains unvalidated for PRISM live use.

Post-PIVOT claim control is governed by DOG `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md`: reciprocal-only is the hard baseline, and no DOG variant may claim REST helps PRISM. At most, a future variant may report a paper/mock contract-gate scorecard improvement if it beats reciprocal-only without worsening false-pass risk or auditability.
