# PHASE4_THEORY_TO_EXPERIMENT_TRACEABILITY

## Purpose
This note maps the formal assumptions from the Phase 2 theorem draft to the current implementation controls and experiment diagnostics.

## Assumption-to-code mapping

| Theorem assumption | Implementation control | Diagnostic logged in Phase 4 |
| --- | --- | --- |
| PSD operator | Sliding-window covariance construction | covariance-based operator only |
| Bounded one-step drift | synthetic stream design + covariance updates | drift mean / drift max |
| Retained spectral gap | top-k eigendecomposition with monitored gap | spectral gap mean / spectral gap min |
| Bounded transform laws | explicit clipping on reciprocal and exponential weights | reciprocal / exponential clip rates |
| Controlled basis motion | retained eigenspace tracking | basis motion mean / basis motion max |

## Observed diagnostic ranges

| Experiment | Min spectral gap | Mean drift | Max drift | Mean basis motion | Reciprocal clip rate | Exponential clip rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| drifting_low_rank | 0.205677 | 0.238725 | 1.266937 | 0.007023 | 0.000000 | 0.000000 |
| rotating_anisotropic_gaussian | 0.405271 | 0.710120 | 2.969271 | 0.003127 | 0.000000 | 0.000000 |
| deforming_manifold | 0.000657 | 0.060784 | 0.112008 | 0.089739 | 0.000000 | 0.000000 |
| sparse_high_noise_failure_probe | 0.043981 | 0.738805 | 1.412981 | 0.312272 | 0.000000 | 0.000000 |

## Interpretation
- The covariance construction directly satisfies the PSD assumption.
- The experiments only partially satisfy the intended theorem regime, because spectral gaps can narrow and drift can spike in the harder streams.
- In the specific Phase 4 runs, clipping rates were effectively zero; this means the bounded-transform assumption held without active clipping intervention on these parameter settings. Clipping still remains an important safeguard for harder parameter regimes and future experiments.
- The theorem draft should therefore be interpreted as a local-regime result rather than a global explanation of all observed Phase 4 behavior.
