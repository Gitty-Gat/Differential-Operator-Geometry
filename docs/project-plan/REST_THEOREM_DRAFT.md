# REST_THEOREM_DRAFT

## 2026-04-30 status
This theorem draft is a scope-control artifact for the current REST reference implementation. It does **not** override the locked PIVOT, robustness sweep, adversarial search, or reciprocal-only scope-demotion note.

Use it only to keep proof language aligned with the implemented retained-coordinate preconditioner. It is not evidence that current REST beats reciprocal-only, should continue as-is, or helps PRISM.

## Purpose
This note gives a tighter theorem draft for the **canonical covariance-based REST implementation actually present in this repository**. The goal is deliberately narrow:

- work in the sliding-covariance PSD setting used by the code,
- state the retained-coordinate transform exactly as `src/rest/core.py` computes it,
- prove only a **single-step stability / perturbation statement**,
- and avoid implying a non-commuting ordering mechanism that the current diagonal architecture does not support.

The point of this draft is not to finish the full theory or rescue a failed scorecard. The point is to make theorem language match the strongest honest claim the repo can presently defend.

---

## 1. Implementation anchor
The current reference code path in `src/rest/core.py` does the following at a single time step:

1. build or receive a symmetric PSD covariance operator,
2. compute a top-`k` eigendecomposition,
3. project the centered sample into retained spectral coordinates,
4. apply a clipped reciprocal weight law,
5. apply a clipped exponential weight law,
6. multiply those diagonal weights coordinatewise.

In code notation:

- `basis_t = U_t`,
- `eigenvalues_t = (\lambda_{t,1},\dots,\lambda_{t,k})`,
- `coordinates = U_t^\top \tilde x_t`,
- `inv_weights = reciprocal_weights(eigenvalues_t, r_t, ...)`,
- `exp_weights = exponential_weights(eigenvalues_t, r_t, \beta, ...)`,
- `composite = inv_weights * exp_weights`,
- `rest_coordinates = composite * coordinates`.

So the implemented retained-coordinate map is

```math
T_t := W_t U_t^\top,
\qquad
z_t := T_t \tilde x_t,
```

where `W_t` is diagonal.

Two details matter for interpretation:

- the default shaping law is `\phi(\lambda; r) = \lambda / (\lambda + r)`,
- and because both weight stages are diagonal spectral functions of the same retained eigenvalues, they **commute in the current architecture**.

That means this theorem draft is about the stability of the **composite retained-coordinate preconditioner**, not about proving that reciprocal-then-exponential ordering has an independently meaningful non-commuting effect.

---

## 2. Canonical retained-coordinate definition
Let `L_t \in \mathbb{R}^{d\times d}` be the local symmetric PSD operator at time `t`, interpreted in the active implementation as a sliding-window covariance matrix.

Write the ordered eigendecomposition as

```math
L_t = U_t \Lambda_t U_t^\top + U_{t,\perp}\Lambda_{t,\perp}U_{t,\perp}^\top,
```

with

```math
\lambda_{t,1} \ge \cdots \ge \lambda_{t,d} \ge 0,
\qquad
\Lambda_t := \operatorname{diag}(\lambda_{t,1},\dots,\lambda_{t,k}),
\qquad
U_t \in \mathbb{R}^{d\times k}.
```

For a centered sample `\tilde x_t := x_t - \mu_t`, define the retained coordinates

```math
c_t := U_t^\top \tilde x_t \in \mathbb{R}^k.
```

### 2.1 Reciprocal weights
With ridge scale `r_t > 0`, define

```math
a(\lambda; r_t)
:= \operatorname{clip}((\lambda + r_t)^{-1/2}, a_{\min}, a_{\max}).
```

The corresponding diagonal map is

```math
D_{\mathrm{inv}}(\Lambda_t, r_t)
:= \operatorname{diag}(a(\lambda_{t,1}; r_t),\dots,a(\lambda_{t,k}; r_t)).
```

### 2.2 Exponential weights
Let `\phi(\lambda; r)` be the scalar shaping law. In the default implementation,

```math
\phi(\lambda; r) = \frac{\lambda}{\lambda + r}.
```

Define

```math
b(\lambda; r_t, \beta)
:= \operatorname{clip}(\exp(\beta\,\phi(\lambda; r_t)), b_{\min}, b_{\max}).
```

The corresponding diagonal map is

```math
D_{\exp}(\Lambda_t, r_t, \beta)
:= \operatorname{diag}(b(\lambda_{t,1}; r_t, \beta),\dots,b(\lambda_{t,k}; r_t, \beta)).
```

### 2.3 Composite weight law
Define the composite scalar weight law

```math
h(\lambda, r_t)
:= a(\lambda; r_t)\,b(\lambda; r_t, \beta),
```

and the diagonal composite matrix

```math
W_t
:= D_{\exp}(\Lambda_t, r_t, \beta)D_{\mathrm{inv}}(\Lambda_t, r_t)
= \operatorname{diag}(h(\lambda_{t,1}, r_t),\dots,h(\lambda_{t,k}, r_t)).
```

Because both factors are diagonal in the same retained eigenbasis, this product is the only object that matters for the current theorem.

### 2.4 Implemented transform
The implemented retained-coordinate REST map is

```math
T_t := W_t U_t^\top,
\qquad
z_t := T_t \tilde x_t = W_t U_t^\top \tilde x_t.
```

This note interprets `T_t` as a **retained-coordinate geometric preconditioner**.

---

## 3. Assumptions
We separate assumptions needed for three different things:

- stability of eigenvalues,
- stability of the retained subspace,
- stability of the **ordered coordinate map** actually used by the code.

### Assumption A1: PSD covariance operator
For each relevant time `s`,

```math
L_s = L_s^\top \succeq 0.
```

### Assumption A2: One-step operator drift bound
For consecutive times `t-1` and `t`,

```math
\|L_t - L_{t-1}\|_2 \le \delta.
```

### Assumption A3: Retained rank is separated from the tail
For both `s \in \{t-1,t\}`,

```math
\lambda_{s,k} - \lambda_{s,k+1} \ge \gamma_{\mathrm{tail}} > 0.
```

This is the usual condition needed to keep the retained `k`-dimensional eigenspace well defined.

### Assumption A4: Ordered retained eigenvectors are identifiable
To control the exact coordinate map `T_s = W_s U_s^\top` rather than only the projector `P_s = U_s U_s^\top`, assume the retained eigenpairs are not internally ambiguous. A convenient sufficient condition is:

```math
\lambda_{s,i} - \lambda_{s,i+1} \ge \gamma_{\mathrm{vec}} > 0
\qquad (i = 1,\dots,k),
```

for both `s \in \{t-1,t\}` with the convention that the `i = k` case is already included in A3.

Interpretation:
- A3 prevents the retained subspace from colliding with the discarded tail.
- A4 prevents uncontrolled rotations **inside** the retained subspace.

Without A4, a subspace theorem is still reasonable, but an ordered-coordinate theorem for `U_t^\top` is generally too strong.

### Assumption A5: Bounded ridge scale
There exist constants

```math
0 < r_{\min} \le r_s \le r_{\max} < \infty
\qquad (s \in \{t-1,t\}).
```

When needed, also assume

```math
|r_t - r_{t-1}| \le \delta_r.
```

### Assumption A6: Bounded and Lipschitz composite weight law
Assume that over the spectral/ridge domain visited by the implementation there exist finite constants `M_h`, `L_\lambda`, and `L_r` such that

```math
|h(\lambda, r)| \le M_h,
```

and

```math
|h(\lambda, r) - h(\lambda', r')|
\le L_\lambda |\lambda - \lambda'| + L_r |r-r'|.
```

This is natural for the clipped implementation used in the repo.

### Assumption A7: Bounded centered input norm (only for output-vector bounds)
When passing from operator stability to a bound on output vectors, assume

```math
\|\tilde x\|_2 \le R.
```

---

## 4. Immediate consequences of the implementation form
Because `W_t` is diagonal with entries `h(\lambda_{t,i}, r_t)`,

```math
\|W_t\|_2 \le M_h.
```

Also, by Weyl's inequality and A2,

```math
|\lambda_{t,i} - \lambda_{t-1,i}| \le \delta
\qquad (1 \le i \le k).
```

Therefore,

```math
\|W_t - W_{t-1}\|_2
\le L_\lambda \delta + L_r |r_t-r_{t-1}|.
```

This is the weight-variation part of the theorem and is the cleanest part of the current analysis because it follows directly from the clipped scalar laws used in code.

---

## 5. Main theorem target
### Theorem 1 (single-step stability of the implemented retained-coordinate preconditioner)
Let

```math
T_s := W_s U_s^\top
\qquad (s \in \{t-1,t\})
```

be the retained-coordinate transform defined above. Under Assumptions A1-A6, after fixing eigenvector signs consistently across the two steps (equivalently, using the closest sign convention for each simple ordered eigenvector), and for sufficiently small `\delta` relative to `\gamma_*`, there exists a constant `C_{\mathrm{basis}} > 0` depending only on the chosen eigenvector perturbation estimate and the retained dimension `k` such that

```math
\|T_t - T_{t-1}\|_2
\le
L_\lambda \delta + L_r |r_t-r_{t-1}|
+ C_{\mathrm{basis}} M_h \frac{\delta}{\gamma_*},
```

where

```math
\gamma_* := \min\{\gamma_{\mathrm{tail}}, \gamma_{\mathrm{vec}}\}.
```

In the common case where the ridge scale is held fixed across one step,

```math
r_t = r_{t-1},
```

this simplifies to

```math
\|T_t - T_{t-1}\|_2
\le
L_\lambda \delta
+ C_{\mathrm{basis}} M_h \frac{\delta}{\gamma_*}.
```

### Corollary 1 (single-step output perturbation for a fixed centered input)
Under the same assumptions, for any centered input vector `\tilde x \in \mathbb{R}^d`,

```math
\|T_t \tilde x - T_{t-1} \tilde x\|_2
\le \|T_t - T_{t-1}\|_2 \, \|\tilde x\|_2.
```

If A7 also holds, then

```math
\|T_t \tilde x - T_{t-1} \tilde x\|_2
\le
R\left(
L_\lambda \delta + L_r |r_t-r_{t-1}| + C_{\mathrm{basis}} M_h \frac{\delta}{\gamma_*}
\right).
```

### What this theorem is claiming
The claim is local and modest:

- if the covariance operator moves by only `\delta` in one step,
- if the retained eigenspace stays separated from the tail,
- if the retained ordered eigenvectors remain identifiable,
- and if the clipped composite weight law stays bounded and Lipschitz,

then the implemented retained-coordinate map `T_t` changes by a controlled amount.

This is exactly a **single-step stability statement for a geometric preconditioner**.

---

## 6. Why Assumption A4 is doing real work
A4 is not a cosmetic addition. It is the piece that prevents the theorem from quietly overclaiming.

If only A3 holds, then one still has a standard projector-level bound of the form

```math
\|P_t - P_{t-1}\|_2 \lesssim \frac{\delta}{\gamma_{\mathrm{tail}}},
\qquad
P_s := U_s U_s^\top.
```

That controls the retained **subspace**.

But the implemented object `T_s = W_s U_s^\top` depends on an **ordered basis**, not just on the subspace. If eigenvalues inside the retained block are repeated or nearly repeated, the basis can rotate within that block while the subspace stays stable. In that situation a bound on `P_t - P_{t-1}` does **not** automatically imply a clean bound on `T_t - T_{t-1}`.

So the right honest split is:

- with A3 alone: projector/subspace stability is justified,
- with A3 + A4: ordered-coordinate transform stability is justified.

That distinction matches the implementation more faithfully than the older draft.

---

## 7. Proof outline
This remains a proof outline rather than a finished line-by-line proof.

### Step 1: Split the transform difference
Write

```math
T_t - T_{t-1}
=
W_t U_t^\top - W_{t-1} U_{t-1}^\top
=
(W_t - W_{t-1}) U_t^\top + W_{t-1}(U_t^\top - U_{t-1}^\top).
```

Hence

```math
\|T_t - T_{t-1}\|_2
\le
\|W_t - W_{t-1}\|_2
+
\|W_{t-1}\|_2 \, \|U_t - U_{t-1}\|_2,
```

because `\|U_t^\top\|_2 = 1`.

### Step 2: Control the diagonal weight variation
By the Lipschitz property in A6 and Weyl's inequality,

```math
\|W_t - W_{t-1}\|_2
\le L_\lambda \delta + L_r |r_t-r_{t-1}|.
```

Also,

```math
\|W_{t-1}\|_2 \le M_h.
```

### Step 3: Control ordered eigenvector motion
Under A2-A4, after sign-aligning the ordered eigenvectors between steps, standard eigenvector perturbation results for simple ordered eigenpairs give

```math
\|U_t - U_{t-1}\|_2
\le C_{\mathrm{basis}} \frac{\delta}{\gamma_*}.
```

At this level of generality, the theorem does not need the sharpest possible constant. It only needs the dependence on operator drift and eigengap scale to be stated honestly.

### Step 4: Combine the estimates
Substituting the previous two bounds into the splitting inequality yields

```math
\|T_t - T_{t-1}\|_2
\le
L_\lambda \delta + L_r |r_t-r_{t-1}|
+ C_{\mathrm{basis}} M_h \frac{\delta}{\gamma_*}.
```

The output-vector corollary follows immediately by multiplying by `\|\tilde x\|_2`.

---

## 8. Interpretation and non-claims
### 8.1 What the theorem does support
This theorem draft supports the following repo-level statement:

> In the covariance-based retained-coordinate setting implemented here, REST defines a clipped spectral preconditioner whose one-step transform varies continuously under bounded operator drift, with explicit dependence on eigengap scale and weight-law bounds.

That is a real and useful theorem target.

### 8.2 What it does not support
This draft does **not** justify claims about:

- long-horizon stability under many updates,
- near-isometry,
- angle preservation,
- asymptotic convergence,
- broad operator-family generalization,
- empirical superiority over simpler baselines,
- superiority over reciprocal-only,
- justification for continuing current REST as-is after PIVOT,
- any PRISM-facing claim,
- or a distinct non-commuting ordering mechanism in the current retained-coordinate diagonal architecture.

### 8.3 Why the commuting point matters
Because the reciprocal and exponential stages are both diagonal spectral functions of the same retained eigenvalues, the current architecture is algebraically commuting at the retained-coordinate level. So the theorem should be read as a theorem about the **composite preconditioner** `W_t`, not as evidence that “reciprocal then exponential” is already a separately validated mechanism.

### 8.4 Strongest honest takeaway
The strongest honest short summary is now:

> Current REST is a covariance-based retained-coordinate streaming preconditioner with a plausible one-step stability story, preserved as a reference implementation; reciprocal-only is the hard baseline and current evidence-supported center of gravity after PIVOT / robustness / adversarial results.

That is narrower than the early framing, but it matches the code, the completed scorecards, and the 2026-04-30 scope-demotion direction much better.
