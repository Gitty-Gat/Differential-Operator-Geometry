# Reciprocal-Only Adversarial Failure Search — 2026-04-28

**2026-04-30 stand-down note:** PRISM guardrails in this historical search are archived evidence only. Future DOG work should not expand PRISM-specific integration gates unless explicitly reauthorized.

## Status
Executed narrow adversarial search. Reciprocal-only remains the current winning baseline; this slice searches for its failures rather than trying to rescue REST.

## Claim boundary
Synthetic DOG evidence plus PRISM paper/mock guardrails only. No PRISM live-use claim. No theorem prose in place of benchmark evidence.

## Registered failure criteria
Reciprocal-only is flagged as failing a DOG adversarial case if it crosses any of:
- normalized downstream MSE > `1.0`;
- downstream error / best method error >= `1.1`;
- stability > `1.5`;
- stability / best method stability >= `1.25`.

A DOG method is promising only if it beats reciprocal-only on downstream error, stability, and runtime while also preserving PRISM false-pass and auditability guardrails.

## Coverage
- DOG adversarial cases: `5`
- Seeds per case: `5`
- PRISM paper/mock adversarial guardrail scenarios: `4`

## Decision
**FAILURES_FOUND_NO_DOG_RESCUE**

The search found reciprocal-only failure criteria, but no current DOG method beat reciprocal-only while preserving PRISM guardrails. Recommend stopping current REST rescue and refocusing on baseline characterization or a pre-registered new variant only.

## Reciprocal-only failure cases
- `switching_lag`: flags `absolute_downstream_failure`; reciprocal normalized MSE `1.016386`, stability `1.070927`
- `outlier_bursts`: flags `absolute_downstream_failure`; reciprocal normalized MSE `1.023815`, stability `1.090509`
- `low_variance_target`: flags `absolute_downstream_failure`; reciprocal normalized MSE `1.005505`, stability `1.164468`
- `eigenvalue_collapse`: flags `absolute_downstream_failure`; reciprocal normalized MSE `1.009409`, stability `0.876737`

## Promising DOG candidates
None. No current REST/whitening/no-transform path earns a follow-up claim from this search.

## Case scorecard
| Case | Reciprocal failed? | Recip norm MSE | Recip stability | Best DOG-side candidate |
| --- | ---: | ---: | ---: | --- |
| switching_lag | true | 1.016386 | 1.070927 | none |
| outlier_bursts | true | 1.023815 | 1.090509 | none |
| low_variance_target | true | 1.005505 | 1.164468 | none |
| eigenvalue_collapse | true | 1.009409 | 0.876737 | none |
| reciprocal_clip_stress | false | 0.986889 | 1.001192 | none |

## PRISM guardrail summary
| Method | Guardrail OK all scenarios | Max false-pass delta | Max auditability delta |
| --- | ---: | ---: | ---: |
| rest | true | 0.000000 | 0.000000 |
| covariance_whitening | true | 0.000000 | 0.000000 |
| no_transform | false | 0.790698 | -0.005313 |

## Recommendation
Stop trying to rescue current REST from this evidence. Refocus on reciprocal-only characterization, scope demotion, or a separately pre-registered new variant if one is genuinely motivated.

## Commands
```bash
PYTHONPATH=src python experiments/synthetic/run_reciprocal_adversarial_search.py
PYTHONPATH=src python -m unittest discover -s tests -v
```
