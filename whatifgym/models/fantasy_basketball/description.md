# Fantasy basketball line-up

**Domain:** revenue / resource planning · **Type:** IP (binary) · **Size:** 96 variables, 97 constraints · **Sense:** maximise predicted fantasy points

Choose a fantasy line-up for the NBA games of 25 December 2017 from 96 players. Each player has one position
(PG, SG, SF, PF or C), a fantasy salary and a predicted fantasy-points score. The line-up must have exactly the
required number of players at each position (one each) and its total salary may not exceed the cap (30,000).
The goal is to maximise the line-up's total predicted points.

Decisions: `pick[player] = 1` if the player is in the line-up.

Reference optimum (original notebook, Gurobi): **171.92** — Jarrett Jack (PG), Trevor Ariza (SG), Markieff Morris
(SF), Dario Saric (PF), Joel Embiid (C), salary 29,700.

The notebook predicts points with a regression on box scores; that step is not reproduced. The predicted points
are frozen data (`players.predicted_points`). Like the original, there is one position row per player (91 rows
duplicate the five distinct position rows).

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `params` | Raise the salary cap to 35,000; cut it to 25,000. |
| `players` | Embiid is ruled out; Harden's salary drops to 9,000; LeBron's prediction rises to 55. |
| `positions` | Require two guards at PG; a line-up without a center. |

Source: Gurobi modeling-examples `fantasy_basketball/fantasy_basketball_part1.ipynb` (Apache-2.0); data from
`target_games.csv` and `results_target_advanced.csv` in the same folder. Re-implemented from the published data.
