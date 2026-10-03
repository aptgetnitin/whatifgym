# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|
| `cowork-opus` | 60 | 1.000 | 1.100 | 1.00 | 1.00 (60) | 1.00 (28) | 1.00 (16) | 1.00 (16) | – |
| `cowork-sonnet` | 60 | 0.983 | 1.083 | 1.00 | 0.98 (60) | 1.00 (28) | 1.00 (16) | 0.94 (16) | – |

## By base model

| base model | `cowork-opus` | `cowork-sonnet` |
|---|---|---|
| `factory_planning` | 1.00 (60) | 0.98 (60) |

## By template (where the misses are)

### `cowork-opus`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | combo | 1.00 (16) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |

### `cowork-sonnet`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | combo | 0.94 (16) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |
|---|---|---|---|---|---|
| `cowork-opus` | 0 | 0 | 0 | 0 | 0 |
| `cowork-sonnet` | 1 | 0 | 0 | 0 | 0 |
