# Wedding seating (set partitioning)

**Domain:** packing / assignment / covering · **Type:** IP (binary, column-enumerated) · **Size:** 3 213 variables, 18 constraints · **Sense:** minimise unhappiness

Seventeen guests must be seated at no more than five tables of at most four people. Every subset of guests that
fits a table is enumerated as a candidate table (a column) with an "unhappiness" score equal to the rank spread
between its first and last guest; the model picks a set of tables so that each guest sits at exactly one of them.
It is the textbook example of set partitioning — the same structure as crew pairing, vehicle-route selection and
shift-pattern selection — and the only base model whose columns are generated from the data.

Decisions: `x[table] = 1` if that candidate table is used.

Reference optimum (original PuLP example on CBC, HiGHS and SCIP): **12**.

## What-if surface

| Table / param | Typical scenario questions |
|---|---|
| `params.max_tables` | Only four tables fit in the room — how much unhappiness does that cost? |
| `params.max_table_size` | Tables seat five; tables seat three. |
| `guests` | Guest H accepts after all (rank 8); two guests cancel; re-rank the guest list by friendship group. |

Solvers: PuLP formulation on HiGHS / SCIP / CBC, plus a native OR-Tools CP-SAT formulation (`build_cpsat`).
Note that CP-SAT needs a few seconds to prove optimality here while the MIP solvers need well under a second.

Source: PuLP `examples/wedding.py` (MIT, Stuart Mitchell 2009), documented as the case study
"A Set Partitioning Problem". Re-implemented from the published data.
