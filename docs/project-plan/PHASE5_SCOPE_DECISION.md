# PHASE5_SCOPE_DECISION

## Status
**Phase 5 scope decision: NARROW and REFINE before any broad expansion**

## Decision summary
The repository should not broaden aggressively to real-world datasets yet.

The correct immediate scope is:
1. continue under the **geometric preconditioner** framing,
2. keep the covariance-based implementation as the canonical active path,
3. treat the non-commuting-variant idea as a bounded optional spike rather than the main line,
4. defer broad real-world expansion until theorem/code alignment is tighter and the contribution framing is cleaner.

## Why this is the right decision
This decision follows directly from the current evidence:
- Phase 3 showed that REST is implementable and testable.
- Phase 4 showed that REST is viable but not dominant across all important synthetic conditions.
- Phase 4 also showed that the current ordering claim is structurally weakened by commutativity in the retained-coordinate diagonal architecture.
- Phase 5 therefore should reduce ambition temporarily rather than expanding on a partially unstable contribution story.

## What to continue doing
The repo should continue investing in:
- the preconditioner framing,
- theorem tightening,
- controlled validation in narrow settings where preconditioning plausibly matters,
- and careful documentation of where the method helps versus fails.

## What to defer
The repo should defer:
- broad real-world dataset campaigns,
- broader operator-family expansion,
- graph/Jacobian architecture diversification,
- and strong novelty claims around stage ordering.

## Non-commuting variant decision
The non-commuting variant should remain a **short bounded spike**, not the main path.

### Use this rule
Pursue the spike only if one of the following becomes strategically necessary:
1. the project still depends on restoring an ordering-based novelty claim,
2. the preconditioner framing proves too weak to justify future publication or deployment directions,
3. a simple non-commuting change appears capable of restoring distinct behavior without large complexity costs.

If not, keep the spike deferred.

## Near-term recommended path
The recommended next sequence is:
1. finish aligning theorem language and implementation evidence,
2. stabilize the preconditioner framing in all active docs,
3. run only narrow additional validations that test where geometric preconditioning helps,
4. revisit broader expansion after those targeted checks.

## Scope conclusion
Phase 5 resolves the repo's immediate strategic question as follows:

> REST should continue forward as a covariance-based streaming geometric preconditioner, under a narrowed and more defensible scope, until stronger evidence justifies either broader validation or architectural revision.
