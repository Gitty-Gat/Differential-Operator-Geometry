# CHAIRMAN_CREATIVITY_TRAJECTORY_IMPLEMENTATION_PLAN_2026-04-13

## Purpose
This plan converts the 2026-04-13 chairman/director strategy meeting into concrete execution. It assumes the current mainline remains:

> REST as a covariance-based streaming geometric preconditioner in retained spectral coordinates.

But it also assumes the next phase must be **decision-led**, not merely framing-led.

---

## Strategic objective
Within the next operating cycle, force a clear answer to this question:

> Does the current REST architecture have a defendable advantage in a specific drifting-stream regime, or does it require architectural revision / scope demotion?

---

# 1) Priority-ranked action items

## Priority 0 — Lock the decision target
**Action:** choose the first target use-case class and evaluation question.

### Required output
A one-paragraph decision memo naming:
- target regime,
- target downstream task,
- comparison baselines,
- core metric(s),
- and what result counts as continue / refine / pivot.

### Status update
**Resolved.** The authoritative decision is now recorded in `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`.

Locked choice:
- target regime: moderate-drift synthetic streams with clean-to-messy spectral-gap variation,
- primary question: Question 2 from this plan,
- downstream task: short-horizon online regression plus stability scorecard,
- baselines: REST, reciprocal-only, covariance-whitening, no-transform,
- metrics: stability, downstream error, variance across seeds, runtime cost,
- interpretation rule: continue / refine / pivot exactly as stated in the memo.

### Why this is first
Without this, the repo can keep producing clean but strategically weak work.

### Owner assumption
- **Requires Sean specifically:** complete — memo received.
- **Can be prepared autonomously:** no longer needed for target selection; downstream execution can proceed autonomously.

---

## Priority 1 — Build the narrow benchmark harness
**Action:** implement a reusable experiment harness for a small family of drifting-stream benchmarks.

### Scope
Include only what is needed for the decision slice:
- current REST,
- reciprocal-only baseline,
- covariance-whitening or related simple baseline,
- no-transform baseline where appropriate,
- shared metrics/output schema.

### Required artifacts
- benchmark runner script(s),
- config or parameter registry for regimes,
- machine-readable result summaries,
- one compact comparison table/plot set.

### Success condition
A single command or small command set can regenerate the decision artifacts.

### Owner assumption
- **Requires Sean specifically:** no.
- **Can be done autonomously:** yes.

---

## Priority 2 — Define regime-by-regime scorecard
**Action:** formalize pass/fail interpretation before the next validation run.

### Scorecard fields
For each regime:
- conditioning gain,
- downstream metric change,
- stability under drift,
- variance across seeds,
- runtime cost,
- interpretation: useful / neutral / negative.

### Why this matters
The repo needs fewer pretty artifacts and more forced interpretations.

### Owner assumption
- **Requires Sean specifically:** no, unless metric priorities are domain-specific.
- **Can be done autonomously:** yes.

---

## Priority 3 — Run the decisive narrow validation slice
**Action:** execute the first benchmark family using the harness and scorecard.

### Desired questions
Pick one primary question:
1. Does REST help most when spectral gaps are clean and drift is moderate?
2. Does it retain an edge once reciprocal-only is included seriously?
3. Does a downstream online task reveal benefit better than generic transform metrics?

### Required output
A short evaluation note with:
- exact regimes tested,
- metrics,
- win/loss summary,
- continue/refine/pivot recommendation.

### Owner assumption
- **Requires Sean specifically:** no.
- **Can be done autonomously:** yes.

---

## Priority 4 — Tighten theory only after regime evidence is updated
**Action:** revise theorem/method notes only in ways directly supported by the new validation slice.

### Rule
Theory work should mirror the surviving claim, not subsidize an unchosen claim.

### Deliverables
- targeted theorem edits,
- targeted method-note edits,
- no broad new conceptual notes unless needed.

### Owner assumption
- **Requires Sean specifically:** no.
- **Can be done autonomously:** yes.

---

## Priority 5 — Predefine the bounded variant trigger
**Action:** write a hard trigger for when to test a non-commuting or otherwise architecture-changing spike.

### Trigger examples
Run the spike only if at least one is true:
- current REST remains ambiguous after the next decisive slice,
- reciprocal-only dominates too often,
- a realistic use-case seems to require non-commuting behavior,
- or the publishable novelty case remains too weak.

### Deliverable
One short control note or addition to `DECISIONS.md` with entry/exit conditions.

### Owner assumption
- **Requires Sean specifically:** yes for approval to spend time on a variant if the trigger fires.
- **Can be prepared autonomously:** yes.

---

# 2) Near-term execution sequence

## Sequence for the next cycle
1. Use `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md` as the fixed target.
2. Implement the narrow benchmark harness.
3. Add the regime scorecard.
4. Run the decisive validation slice.
5. Write the resulting evaluation note.
6. Decide: continue mainline / refine / bounded variant spike / demote scope.
7. Only then update theorem/method docs to match the surviving claim.

---

# 3) Today / One Month / One Year plan

## Today / Short Term

### Objective
Stop narrative drift and cash the forced decision now that the target is fixed.

### Actions
- implement the benchmark harness for the locked moderate-drift / spectral-gap slice,
- define metrics and scorecard,
- run the first decisive validation,
- ensure repo operations remain stable enough to iterate.

### Expected output
A runnable, narrow validation lane with a continue / refine / pivot answer.

### Risks
- overengineering the harness,
- diluting the locked target into too many side regimes,
- slipping back into documentation-first progress.

## One Month / Mid Term

### Objective
Resolve whether the current architecture has a winning niche.

### Actions
- complete at least one serious narrow evaluation cycle,
- compare against strong simple baselines,
- quantify where REST helps or fails,
- either deepen the winning lane or trigger the bounded variant discussion.

### Expected output
A clear strategic branch decision.

### Risks
- inconclusive metrics,
- target regime chosen too vaguely,
- reluctance to call an ambiguous result ambiguous.

## One Year / Long Term

### Objective
Convert DOG into either a focused validated line or an honest contained research umbrella.

### Actions
- if the method wins somewhere, scale evidence and sharpen theory for that niche,
- if not, split reusable submethods from the umbrella vision,
- pursue application or publication only after the narrow value case is real.

### Expected output
Either:
- a paper/deployment-ready niche line, or
- a disciplined exploratory framework with clearer internal boundaries.

### Risks
- broadening prematurely,
- confusing conceptual ambition with validated contribution,
- failing to separate flagship work from speculative work.

---

# 4) Owner assumptions

## What requires Sean specifically
1. Approval to spend meaningful time on a bounded non-commuting or architecture-changing spike.
2. Acquisition/selection of harder public or partner-provided datasets if the work moves beyond current synthetic regimes.
3. Any capital, cloud budget, paid services, or partnership outreach.
4. Final decision on long-term posture: research artifact, publication push, patent angle, or product exploration.

## What can be done autonomously
1. Building the benchmark harness.
2. Implementing baselines and evaluation scripts.
3. Running narrow validations and summarizing results.
4. Updating docs to reflect validated outcomes.
5. Maintaining a scorecard and explicit continue/refine/pivot logic.
6. Preparing the bounded-variant trigger note.

---

# 5) External dependencies

## Data dependencies
- harder-but-controlled streaming datasets,
- eventually one intermediate-complexity benchmark family,
- possibly one domain dataset with meaningful drift.

## Tooling dependencies
- stable Python/runtime environment,
- reproducible experiment execution,
- result artifact generation,
- reliable git push/auth if remote sync is expected.

## Access dependencies
- repo mount stability,
- GitHub remote access/auth,
- possibly domain-specific data access later.

## Partnership dependencies
- optional domain advisor or applied collaborator to sanity-check practical value.

---

# 6) Resource needs and likely sources

## Data
- **Need:** controlled-but-harder stream benchmarks.
- **Likely source:** Sean-curated public datasets; open benchmarks; later partner-provided data.

## Capital
- **Need:** modest compute/storage now, potentially larger budget later.
- **Likely source:** Sean, cloud credits, collaborator support, or research budget.

## Services
- **Need:** possibly cloud compute, experiment tracking, publication support later.
- **Likely source:** Sean or external collaborators.

## Access
- **Need:** durable remote auth, repo sync, and later domain data access.
- **Likely source:** host configuration plus Sean-managed credentials/relationships.

## Tooling
- **Need:** benchmark harness, aggregation scripts, and stable execution environment.
- **Likely source:** mostly autonomous implementation inside the repo.

## Partnerships
- **Need:** at least one operator/domain contact who cares about drift-conditioned preprocessing.
- **Likely source:** Sean's network or future research/application partners.

## Human decisions
- **Need:** use-case prioritization, variant-go/no-go, long-term strategic posture.
- **Likely source:** Sean.

---

# 7) Concrete next actions

## Next 3 actions
1. Implement the narrow benchmark harness around the locked moderate-drift / spectral-gap decision target.
2. Add the short-horizon online regression plus stability scorecard.
3. Run the first decisive validation and summarize it with the scorecard.

## Stop conditions
Pause or change course if:
- the chosen regime still does not produce an interpretable edge,
- reciprocal-only keeps matching or beating REST without a compensating benefit,
- the mainline story remains too weak even after targeted evaluation.

## Continue conditions
Continue mainline investment if:
- one regime repeatedly shows useful preconditioning behavior,
- the effect is interpretable and not purely cosmetic,
- and the claim can be stated cleanly without reviving the unsupported ordering narrative.

---

# 8) Implementation stance

This plan deliberately rejects another cycle of progress defined mainly by elegant framing. The next cycle should produce a strategic answer, not just a better description.

If the current REST line is real, this process should expose where it is real. If it is not real enough yet, this process should expose that quickly too.
