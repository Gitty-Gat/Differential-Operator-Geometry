# PHASE4_DOWNSTREAM_TASK_NOTE

## Purpose
This note records the first controlled downstream-task checks for the canonical covariance-based REST representation.

## Tasks used
1. Change-point sensitivity on an abrupt regime-switch stream
2. Regime clustering separability on the same stream
3. Short-horizon forecasting proxy on the drifting low-rank stream

## Results

### Change-point sensitivity

| Representation | Contrast score |
| --- | ---: |
| rest | 0.757039 |
| raw | 0.607050 |
| reciprocal_only | 0.883912 |
| exponential_only | 0.535767 |
| exp_then_reciprocal | 0.757039 |

### Regime clustering separability

| Representation | Fisher ratio |
| --- | ---: |
| rest | 0.057461 |
| raw | 0.044285 |
| reciprocal_only | 0.102778 |
| exponential_only | 0.022381 |
| exp_then_reciprocal | 0.057461 |

### Short-horizon forecasting proxy

| Representation | One-step MSE |
| --- | ---: |
| rest | 5.034453 |
| raw | 4.951410 |
| reciprocal_only | 1.657859 |
| exponential_only | 16.015731 |

## Takeaway
These downstream tasks are intentionally simple. Their role is not to prove broad application dominance, but to test whether the REST representation changes task-relevant behavior relative to simpler baselines in a controlled setting.
