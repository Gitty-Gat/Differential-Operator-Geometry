# CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28

## Status
Locked DOG decision slice executed.

## Locked question
> Does REST retain a defendable edge in moderate-drift synthetic streams with clean-to-messy spectral-gap variation once reciprocal-only is treated as a serious baseline?

## Benchmark harness
- Script: `experiments/synthetic/run_decision_slice.py`
- Metrics JSON: `experiments/results/decision_slice_metrics.json`
- Regimes: clean_gap, medium_gap, messy_gap
- Baselines: REST, reciprocal-only, covariance-whitening, no-transform
- Task: temporal short-horizon regression from each representation to the next primary latent coordinate

## Scorecard schema
Each regime records:
- stability mean and seed variance,
- downstream regression error mean and seed variance,
- transform runtime mean and seed variance,
- REST-vs-reciprocal downstream-error ratio,
- REST-vs-reciprocal stability ratio,
- useful / neutral / negative interpretation.

## Regime results

### clean_gap
moderate drift with a clear dominant spectral direction

- mean spectral gap: 0.561452
- minimum spectral gap: 0.098224
- mean REST condition proxy: 1.773566
- scorecard interpretation: **NEUTRAL**
- REST / reciprocal downstream-error ratio: 0.992933
- REST / reciprocal stability ratio: 1.628387

| Method | Stability mean | Stability seed var | Downstream error mean | Downstream error seed var | Runtime ms mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| rest | 1.469671 | 0.004863 | 1.333938 | 0.145344 | 0.023063 |
| reciprocal_only | 0.902532 | 0.001818 | 1.343432 | 0.163615 | 0.007273 |
| covariance_whitening | 1.171654 | 0.004874 | 1.344849 | 0.168866 | 0.004150 |
| no_transform | 1.521355 | 0.010914 | 1.295838 | 0.080285 | 0.001782 |

### medium_gap
moderate drift with a present but less dominant spectral gap

- mean spectral gap: 0.606645
- minimum spectral gap: 0.092776
- mean REST condition proxy: 1.383437
- scorecard interpretation: **NEUTRAL**
- REST / reciprocal downstream-error ratio: 1.000134
- REST / reciprocal stability ratio: 1.599447

| Method | Stability mean | Stability seed var | Downstream error mean | Downstream error seed var | Runtime ms mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| rest | 1.393297 | 0.004110 | 1.138691 | 0.149026 | 0.020904 |
| reciprocal_only | 0.871111 | 0.002064 | 1.138538 | 0.169037 | 0.006552 |
| covariance_whitening | 1.120048 | 0.004780 | 1.133116 | 0.188549 | 0.003789 |
| no_transform | 1.215407 | 0.004965 | 1.123634 | 0.109170 | 0.001563 |

### messy_gap
moderate drift with weak / messy top-two separation

- mean spectral gap: 0.600025
- minimum spectral gap: 0.122810
- mean REST condition proxy: 1.183495
- scorecard interpretation: **NEUTRAL**
- REST / reciprocal downstream-error ratio: 0.998613
- REST / reciprocal stability ratio: 1.553411

| Method | Stability mean | Stability seed var | Downstream error mean | Downstream error seed var | Runtime ms mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| rest | 1.318603 | 0.002706 | 1.084879 | 0.214440 | 0.020806 |
| reciprocal_only | 0.848844 | 0.001725 | 1.086386 | 0.219762 | 0.006500 |
| covariance_whitening | 1.105196 | 0.005985 | 1.086634 | 0.223511 | 0.003691 |
| no_transform | 1.040896 | 0.003962 | 1.079297 | 0.205530 | 0.001567 |

## Continue / Refine / Pivot decision
**Decision: PIVOT**

Reciprocal-only matches or beats REST across the locked regimes on both downstream error and stability, so the current architecture does not earn mainline continuation from this slice.

## Interpretation
The locked slice does not support continuing the current REST architecture as-is. Reciprocal-only is too competitive, so the next strategic step should be bounded architectural revision or scope demotion rather than broader validation.

## Post-PIVOT claim control
- Current REST status: reference implementation, not validated continuation.
- Hard baseline for next slices: reciprocal-only.
- Protocol: `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md`.
- Stop/refine if reciprocal-only remains enough.
- Do not use theorem prose as a substitute for benchmark evidence.

## Command
```bash
PYTHONPATH=src .venv/bin/python experiments/synthetic/run_decision_slice.py
```
