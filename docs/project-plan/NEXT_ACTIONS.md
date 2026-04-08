# NEXT_ACTIONS

_Last updated: 2026-04-08_

This file is the short operational queue for the repo. It exists to turn the current framing into the next few resumable slices without re-reading the entire project history.

## Active objective
Tighten the repo around the strongest honest contribution:

> REST as a covariance-based streaming geometric preconditioner in retained spectral coordinates, with bounded one-step stability language and controlled synthetic support.

## Control docs for this phase
Use these before reopening old phase reports:
- `ROADMAP.md`
- `WORKLOG.md`
- `docs/project-plan/PRECONDITIONER_POSITIONING_NOTE.md`
- `DECISIONS.md`

## Current execution rule
Prefer small slices that do one of the following:
1. tighten theorem or method text,
2. run a narrow validation tied to a concrete question,
3. reduce project friction only when it directly improves iteration.

Do **not** spend the next slices broadening scope, reviving universal-geometry claims, or exploring the non-commuting variant unless the trigger conditions in `DECISIONS.md` are met.

## Priority queue

### 1) Tighten `docs/project-plan/REST_METHOD_NOTE.md`
**Why first now:** the theorem draft has been materially narrowed; the method note is now the most important place to synchronize claims with that framing.

**Target outcome:** one canonical method note that a reader can trust as the current description of the code.

**Definition of done:**
- notation matches `src/rest/`,
- covariance construction and retained spectral coordinates are the default path,
- commuting diagonal-weight behavior is acknowledged,
- ordering-sensitive language is removed or explicitly bounded,
- the note states where REST helps conceptually and where simpler transforms may still win.

### 2) Review `docs/project-plan/REST_THEOREM_DRAFT.md` only for proof-detail sharpening
**Why second:** the theorem framing is now narrower and more honest, but the proof sketch and constants can still be tightened without broadening the claim.

**Definition of done:**
- eigenvector-identifiability assumptions remain explicit,
- projector-vs-coordinate-map distinctions stay clear,
- any constant/gap cleanup preserves the current modest scope.

### 3) Design one narrow follow-up validation slice
**Why third:** after text alignment, the next best work is a focused check that tests the preconditioner framing in a regime where it might actually matter.

**Candidate questions:**
- Does REST help more when spectral gaps are cleaner?
- Does benefit persist under controlled drift, or collapse relative to reciprocal-only weighting?
- Which downstream synthetic metric best captures preconditioning benefit rather than generic transform behavior?

**Definition of done:**
- choose one question,
- name the exact script or small code change needed,
- define expected artifact(s),
- state in advance what result would count as useful, neutral, or negative.

### 4) Reassess repo friction only if it blocks execution
**Why fourth:** environment and push issues matter, but they should not dominate theory/method alignment work.

**Definition of done:**
- auth/path issues are documented when they block a slice,
- setup instructions stay accurate,
- no speculative tooling work is added unless it removes repeated friction.

## Recent slice note
- 2026-04-08 AM: `REST_THEOREM_DRAFT.md` was rewritten around the implemented retained-coordinate preconditioner, explicit commuting-weight interpretation, and a separate eigenvector-identifiability assumption for ordered-coordinate stability.

## Stop / continue signals
Continue the narrow program if:
- theorem and method notes become materially cleaner,
- focused validation reveals interpretable help-cases,
- the repo story gets simpler and more defensible.

Pause or reconsider if:
- theory tightening keeps collapsing into weaker claims,
- validation keeps showing no meaningful edge over simpler baselines,
- progress starts depending on reviving an ordering-sensitive story the current architecture does not support.

## One-sentence guidance for the next stand-up
If there is only one slice to do next, do this:

> rewrite `REST_METHOD_NOTE.md` so it matches the revised theorem framing: covariance-based retained-coordinate preconditioning, commuting diagonal weights, and explicit scope limits.
