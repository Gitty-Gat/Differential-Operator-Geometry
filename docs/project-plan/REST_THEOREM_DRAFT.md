# REST_THEOREM_DRAFT

## Purpose
This note gives a first rigorous theorem draft for the canonical covariance-based REST setting:
- streaming observations `x_t \in \mathbb{R}^d`,
- a symmetric positive semidefinite local operator `L_t`,
- a retained rank-`k` eigendecomposition,
- a retained-coordinate REST output interpreted as a **geometric preconditioner**.

The goal here is not to prove the full long-horizon behavior of REST. The goal is to state one precise, conservative single-step perturbation theorem in the canonical covariance-based setting actually implemented in the repository.

---

## 1. Symbol table

### Data and operator objects
- `x_t \in \mathbb{R}^d`: observation at time `t`
- `\mu_t \in \mathbb{R}^d`: windowed mean
- `\tilde{x}_t := x_t - \mu_t`: centered observation
- `L_t \in \mathbb{R}^{d\times d}`: symmetric positive semidefinite local operator at time `t`
- `k \in \{1,\dots,d\}`: retained rank

### Spectral objects
- `\lambda_{t,1} \ge \cdots \ge \lambda_{t,d} \ge 0`: eigenvalues of `L_t`
- `\Lambda_t := \operatorname{diag}(\lambda_{t,1},\dots,\lambda_{t,k}) \in \mathbb{R}^{k\times k}`: retained eigenvalue matrix
- `U_t = [u_{t,1},\dots,u_{t,k}] \in \mathbb{R}^{d\times k}`: retained orthonormal eigenbasis
- `P_t := U_tU_t^\top`: orthogonal projector onto the retained eigenspace

### Coordinates and transforms
- `c_t := U_t^\top\tilde{x}_t \in \mathbb{R}^k`: retained spectral coordinates
- `D_{\mathrm{inv}}(\Lambda_t, r_t) \in \mathbb{R}^{k\times k}`: reciprocal flattening diagonal map
- `D_{\exp}(\Lambda_t, r_t, \beta) \in \mathbb{R}^{k\times k}`: exponential lift diagonal map
- `W_t := D_{\exp}(\Lambda_t, r_t, \beta)D_{\mathrm{inv}}(\Lambda_t, r_t) \in \mathbb{R}^{k\times k}`: composite diagonal weight matrix
- `z_t := W_t c_t \in \mathbb{R}^k`: REST retained-coordinate output
- `T_t := W_tU_t^\top \in \mathbb{R}^{k\times d}`: retained-coordinate transform, so `z_t = T_t\tilde{x}_t`

### Parameters
- `r_t > 0`: reciprocal damping / ridge scale
- `\beta \ge 0`: exponential lift gain
- `\phi(\lambda; r)`: shaping function used in the exponential lift
- `a_{\min}, a_{\max}` with `0 < a_{\min} \le a_{\max} < \infty`: clipping bounds for reciprocal weights
- `b_{\min}, b_{\max}` with `0 < b_{\min} \le b_{\max} < \infty`: clipping bounds for exponential weights
- `\delta`: one-step operator drift bound
- `\gamma > 0`: retained spectral gap lower bound

---

## 2. Canonical retained-coordinate REST definition
For each time `t`, let

```math
L_t = U_t\Lambda_tU_t^\top + U_{t,\perp}\Lambda_{t,\perp}U_{t,\perp}^\top
```

with eigenvalues ordered nonincreasingly. Define the retained coordinates

```math
c_t := U_t^\top\tilde{x}_t.
```

REST then applies two diagonal maps in the retained basis.

### 2.1 Reciprocal flattening operator
Define the unclipped reciprocal weight

```math
\widetilde{a}(\lambda; r_t) := (\lambda + r_t)^{-1/2}.
```

Define the clipped reciprocal weight

```math
a(\lambda; r_t)
:= \operatorname{clip}(\widetilde{a}(\lambda; r_t), a_{\min}, a_{\max}),
```

where

```math
\operatorname{clip}(y,\ell,u) := \min\{u,\max\{\ell,y\}\}.
```

Then

```math
D_{\mathrm{inv}}(\Lambda_t, r_t)
:= \operatorname{diag}(a(\lambda_{t,1};r_t),\dots,a(\lambda_{t,k};r_t)).
```

### 2.2 Exponential lift operator
Let `\phi(\lambda; r_t)` be a prescribed scalar shaping function. Define the unclipped exponential weight

```math
\widetilde{b}(\lambda; r_t, \beta) := \exp(\beta\,\phi(\lambda; r_t)).
```

Define the clipped exponential weight

```math
b(\lambda; r_t, \beta)
:= \operatorname{clip}(\widetilde{b}(\lambda; r_t, \beta), b_{\min}, b_{\max}).
```

Then

```math
D_{\exp}(\Lambda_t, r_t, \beta)
:= \operatorname{diag}(b(\lambda_{t,1};r_t,\beta),\dots,b(\lambda_{t,k};r_t,\beta)).
```

### 2.3 Composite retained-coordinate transform
The composite diagonal weight matrix is

```math
W_t := D_{\exp}(\Lambda_t, r_t, \beta)D_{\mathrm{inv}}(\Lambda_t, r_t).
```

The REST output is

```math
z_t := W_t c_t
     = D_{\exp}(\Lambda_t, r_t, \beta)D_{\mathrm{inv}}(\Lambda_t, r_t)U_t^\top\tilde{x}_t.
```

Equivalently, define the ambient-to-retained transform

```math
T_t := W_tU_t^\top,
```

so that

```math
z_t = T_t\tilde{x}_t.
```

This note treats `z_t` and `T_t` as the primary formal outputs. In Phase 5, the recommended interpretation is that `T_t` is a retained-coordinate preconditioning map rather than evidence that transform ordering is independently meaningful in the current diagonal setting.

---

## 3. Assumptions for the first theorem
We impose the following assumptions for a single-step perturbation result.

### Assumption A1: PSD operator
For each `t`,

```math
L_t = L_t^\top \succeq 0.
```

### Assumption A2: One-step bounded drift
For consecutive times `t-1` and `t`,

```math
\|L_t - L_{t-1}\|_2 \le \delta.
```

### Assumption A3: Retained spectral gap
For both `s \in \{t-1,t\}`, the retained eigenspace is separated by a uniform gap:

```math
\lambda_{s,k} - \lambda_{s,k+1} \ge \gamma > 0,
```

with the convention `\lambda_{s,d+1}:=0` if needed when `k=d`.

### Assumption A4: Controlled ridge scale
There exist constants

```math
0 < r_{\min} \le r_s \le r_{\max} < \infty
\qquad\text{for } s\in\{t-1,t\}.
```

If a bound depending on `|r_t-r_{t-1}|` is needed, assume additionally

```math
|r_t-r_{t-1}| \le \delta_r.
```

### Assumption A5: Bounded and Lipschitz scalar weights
For `r \in [r_{\min}, r_{\max}]`, define

```math
f(\lambda,r) := a(\lambda;r),
g(\lambda,r) := b(\lambda;r,\beta),
h(\lambda,r) := g(\lambda,r)f(\lambda,r).
```

Assume there exist finite constants `M_h, L_\lambda, L_r` such that over the spectral range of interest,

```math
|h(\lambda,r)| \le M_h,
```

and

```math
|h(\lambda,r)-h(\lambda',r')|
\le L_\lambda|\lambda-\lambda'| + L_r|r-r'|.
```

This is automatic for many practical choices once clipping is imposed and the spectral/ridge domain is restricted.

### Assumption A6: Bounded input norm for coordinate-output comparison
When bounding output vectors rather than operators, assume

```math
\|\tilde{x}\|_2 \le R
```

for the input vector under consideration.

---

## 4. Basic diagonal bounds
Since

```math
W_t = \operatorname{diag}(h(\lambda_{t,1},r_t),\dots,h(\lambda_{t,k},r_t)),
```

we have

```math
\|W_t\|_2 = \max_{1\le i\le k}|h(\lambda_{t,i},r_t)| \le M_h.
```

Also, by Weyl's inequality,

```math
|\lambda_{t,i} - \lambda_{t-1,i}| \le \|L_t-L_{t-1}\|_2 \le \delta
\qquad (1\le i\le k).
```

Hence

```math
\|W_t - W_{t-1}\|_2
\le L_\lambda\delta + L_r|r_t-r_{t-1}|.
```

This elementary diagonal bound is the spectral-weight part of the final theorem.

---

## 5. Single-step perturbation/stability theorem
### Theorem 1 (single-step stability of the retained-coordinate geometric preconditioner)
Let

```math
T_s := D_{\exp}(\Lambda_s,r_s,\beta)D_{\mathrm{inv}}(\Lambda_s,r_s)U_s^\top
= W_sU_s^\top
\qquad\text{for } s\in\{t-1,t\}.
```

Under Assumptions A1–A5, there exists an absolute constant `C_{\mathrm{gap}} > 0` such that whenever

```math
\|L_t-L_{t-1}\|_2 \le \delta,
\qquad
\lambda_{s,k}-\lambda_{s,k+1} \ge \gamma > 0 \quad (s=t-1,t),
```

one has

```math
\|T_t - T_{t-1}\|_2
\le
L_\lambda\delta + L_r|r_t-r_{t-1}|
+
C_{\mathrm{gap}}M_h\frac{\delta}{\gamma}.
```

In particular, if the ridge scale is held fixed across one step, `r_t = r_{t-1}`, then

```math
\|T_t - T_{t-1}\|_2
\le
L_\lambda\delta + C_{\mathrm{gap}}M_h\frac{\delta}{\gamma}.
```

Therefore the retained-coordinate geometric preconditioner is single-step stable in operator norm: its change is controlled linearly by the one-step operator drift and inversely by the retained spectral gap.

### Corollary 1 (single-step output perturbation for a fixed centered input)
Under the same assumptions, for any centered input vector `\tilde{x} \in \mathbb{R}^d`,

```math
\|T_t\tilde{x} - T_{t-1}\tilde{x}\|_2
\le \|T_t-T_{t-1}\|_2\,\|\tilde{x}\|_2.
```

If Assumption A6 holds, then

```math
\|T_t\tilde{x} - T_{t-1}\tilde{x}\|_2
\le
R\Big(L_\lambda\delta + L_r|r_t-r_{t-1}| + C_{\mathrm{gap}}M_h\frac{\delta}{\gamma}\Big).
```

---

## 6. Proof outline
This is a proof outline, not yet a fully expanded line-by-line proof.

### Step 1: Split the transform difference
Write

```math
T_t - T_{t-1}
=
W_tU_t^\top - W_{t-1}U_{t-1}^\top
=
(W_t-W_{t-1})U_t^\top + W_{t-1}(U_t^\top-U_{t-1}^\top).
```

Hence

```math
\|T_t-T_{t-1}\|_2
\le
\|W_t-W_{t-1}\|_2\,\|U_t^\top\|_2
+
\|W_{t-1}\|_2\,\|U_t-U_{t-1}\|_2.
```

Since `U_t` has orthonormal columns, `\|U_t^\top\|_2 = 1`, so

```math
\|T_t-T_{t-1}\|_2
\le \|W_t-W_{t-1}\|_2 + \|W_{t-1}\|_2\,\|U_t-U_{t-1}\|_2.
```

### Step 2: Control the diagonal part
By the Lipschitz assumption on `h` and Weyl's inequality,

```math
\|W_t-W_{t-1}\|_2
=
\max_{1\le i\le k}|h(\lambda_{t,i},r_t)-h(\lambda_{t-1,i},r_{t-1})|
\le L_\lambda\delta + L_r|r_t-r_{t-1}|.
```

Also,

```math
\|W_{t-1}\|_2 \le M_h.
```

### Step 3: Control the eigenspace motion
Under the spectral-gap assumption and bounded operator perturbation, a standard eigenspace perturbation result gives

```math
\|P_t - P_{t-1}\|_2 \le C\frac{\delta}{\gamma}
```

for an absolute constant `C`. Passing from projector distance to a bound on orthonormal bases requires a basis-alignment step; after alignment one obtains

```math
\|U_t - U_{t-1}\|_2 \le C_{\mathrm{gap}}\frac{\delta}{\gamma}.
```

### Step 4: Combine the estimates
Substituting the previous bounds into the splitting inequality yields

```math
\|T_t-T_{t-1}\|_2
\le
L_\lambda\delta + L_r|r_t-r_{t-1}| + M_hC_{\mathrm{gap}}\frac{\delta}{\gamma},
```

which is the stated claim.

The corollary follows immediately by multiplying by `\|\tilde{x}\|_2`.

---

## 7. Remarks on interpretation
### 7.1 What this theorem does show
This theorem shows that, in the canonical covariance-based retained-coordinate setting, the one-step geometric preconditioner induced by REST does not change arbitrarily fast when:
- the local operator changes by a small amount in spectral norm,
- the retained eigenspace remains separated by a nontrivial gap,
- the reciprocal/exponential weights are clipped and Lipschitz-controlled.

So the theorem supports a narrow but useful statement: REST is not just a heuristic reweighting; under standard perturbation assumptions, its one-step transform varies continuously and quantitatively.

### 7.2 Why clipping matters
Without clipping, either the reciprocal part or the exponential part can become poorly controlled:
- reciprocal weights can blow up when `\lambda` is small and `r` is too small,
- exponential weights can grow rapidly if `\beta\phi(\lambda;r)` is large.

Clipping is therefore not a cosmetic implementation detail. In this first theorem, it is one of the mechanisms that makes a finite perturbation bound straightforward.

### 7.3 Why the theorem is intentionally modest
This theorem is local in time and does not claim:
- long-horizon accumulation control,
- asymptotic convergence,
- near-isometry,
- robustness to vanishing spectral gaps,
- superiority over PCA, whitening, or other baselines,
- or that reciprocal-then-exponential ordering is itself a distinct tested mechanism in the present diagonal formulation.

Those may become later questions, but they are not established here.

---

## 8. What is still unproved
The following are **not** proved by the present draft and should not be claimed as consequences of Theorem 1:
- repeated-update stability over long horizons,
- angle preservation,
- near-isometry,
- convergence under nonstationary drift,
- optimality of the reciprocal-then-exponential ordering,
- empirical benefit over baselines,
- or the existence of a non-commuting ordering effect in the current retained-coordinate diagonal architecture.

The current theorem is deliberately a first foothold, not the finished theory.
