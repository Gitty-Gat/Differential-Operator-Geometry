# Reciprocal-Only Robustness / Failure-Regime Sweep — 2026-04-28

**2026-04-30 stand-down note:** PRISM guardrails in this historical sweep are archived evidence only. Future DOG work should not expand PRISM-specific integration gates unless explicitly reauthorized.

## Status
Executed post-PIVOT robustness slice. Reciprocal-only is the hard baseline.

## Claim boundary
No theorem prose in place of benchmark evidence. No claim that REST helps PRISM. This is synthetic DOG evidence plus paper/mock PRISM guardrail evidence only.

## Protocol
The sweep reuses the locked DOG decision-slice evaluator across additional seed/regime/scenario combinations, then checks PRISM paper/mock false-pass and auditability guardrails across multiple mock configurations.

A non-reciprocal method counts as a qualified reciprocal-only failure case only when all of the following hold:
- downstream error ratio vs reciprocal-only <= `0.98`;
- stability ratio vs reciprocal-only <= `1.1`;
- runtime ratio vs reciprocal-only <= `3.0`;
- PRISM mock false-pass risk is not worse than reciprocal-only;
- PRISM mock auditability loss is not worse than reciprocal-only;
- PRISM mock contract fields are not obscured.

## DOG sweep coverage
- Scenarios: `7`
- Regimes per scenario: `5`
- Seeds per scenario/regime: `7`
- Scenario/regime summaries: `35`

## PRISM guardrail coverage
- Paper/mock scenarios: `4`
- Guardrails: false-pass delta, auditability delta, contract-obscurity flag

## Decision
**RECIPROCAL_BASELINE_REMAINS_ENOUGH**

No method beat reciprocal-only on the material DOG win rule while also satisfying PRISM mock false-pass and auditability guardrails across the sweep.

## Qualified reciprocal-only failure cases
None under the registered materiality + PRISM-guardrail rule.

## DOG downstream-only signals that failed at least one guardrail
### no_transform
- `locked_default` / `clean_gap`: error ratio `0.960419`, stability ratio `1.651413`, runtime ratio `0.242789`
- `locked_default` / `extreme_gap`: error ratio `0.960976`, stability ratio `2.059651`, runtime ratio `0.247464`
- `high_observation_noise` / `clean_gap`: error ratio `0.965032`, stability ratio `1.642411`, runtime ratio `0.249252`
- `high_observation_noise` / `extreme_gap`: error ratio `0.968342`, stability ratio `2.055014`, runtime ratio `0.242775`
- `short_window` / `clean_gap`: error ratio `0.972524`, stability ratio `1.690494`, runtime ratio `0.242747`
- `long_window` / `clean_gap`: error ratio `0.969970`, stability ratio `1.663519`, runtime ratio `0.243223`
- `long_window` / `extreme_gap`: error ratio `0.963780`, stability ratio `2.129980`, runtime ratio `0.241612`
- `higher_rank_noise` / `clean_gap`: error ratio `0.960087`, stability ratio `1.521130`, runtime ratio `0.250521`
- `higher_rank_noise` / `extreme_gap`: error ratio `0.949795`, stability ratio `1.890025`, runtime ratio `0.246036`

## PRISM method guardrails
| Method | Guardrail OK all scenarios | Max contract-error delta | Max false-pass delta | Max auditability delta | Max stability ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| rest | true | 0.000000 | 0.000000 | 0.000000 | 1.170654 |
| covariance_whitening | true | 0.000000 | 0.000000 | 0.000000 | 9.097571 |
| no_transform | false | 0.681818 | 0.818182 | -0.004663 | 0.633391 |

## Interpretation
Reciprocal-only remains enough for this robustness slice. Some methods may show downstream-only wins, but no method earns a post-PIVOT continuation claim unless it also clears stability, runtime, false-pass, and auditability guardrails.

## Commands
```bash
PYTHONPATH=src python experiments/synthetic/run_reciprocal_robustness_sweep.py
PYTHONPATH=src python -m unittest discover -s tests -v
```
