# Airline planning after flight disruption

**Domain:** network routing · **Type:** IP (binary) · **Size:** 1,930 variables, 536 constraints · **Sense:** minimise lost revenue

A snowstorm cuts airport capacity on 7 January 2006 (ROADEF 2009 / Amadeus data). The plan has 222 flights between
ORY, CDG, LYS and NCE, flown by 21 aircraft. Each flight can only be flown by its assigned aircraft. Each aircraft
needs a route for the day: it starts at its start airport, takes a chain of its flights and ends at its end-of-day
airport. One flight can follow another if it leaves from the airport where the first one landed and departs
strictly after the first one arrives. An aircraft may also stay on the ground all day. At each airport, operated
departures and arrivals are each capped at `capacity_share` (0.5) times the normal day's count. The goal is to
cancel flights so that the lost ticket revenue is as small as possible.

Decisions: `operate[aircraft, flight] = 1` if the flight is flown; `connect[aircraft, flight, next_flight] = 1` if
the aircraft flies `next_flight` right after `flight` (`source` = start of day, `sink` = end of day).

Reference optimum (original notebook, Gurobi): **561,087** lost out of 1,878,476 booked. 51 revenue flights are
flown, carrying 6,570 passengers. Only 77 flights have bookings; the rest have revenue 0 and may be flown or not. Even with no disruption
(share 1) 492,049.5 is lost, because on the 4-airport cut many aircraft cannot chain their flights from their start
to their end airport.

The original's quirks are reproduced. Each aircraft's source and sink pseudo-flights have origin = end airport
and destination = start airport, and they count in the capacity rows, both as operated flights and in the
normal-day totals. A flight departing at 00:00 cannot be an aircraft's first flight. Times are minutes after
midnight. The day's start and end (00:00 and 23:59) are structural constants. The notebook's single disruption
level is a per-airport column here, 0.5 everywhere.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `airports` | NCE closes (share 0); CDG recovers to 80%; LYS can handle only 30%. |
| `flights` | Flight 4576's revenue doubles; flight 3103 leaves an hour later; drop flight 4264 from the plan. |
| `aircraft` | A321#2 is grounded; A318#4 must end the day at CDG instead. |

Source: Gurobi modeling-examples `aviation_planning/airlineplanning.ipynb` (Apache-2.0); data from `data/*.csv` in
the same folder, reduced to the notebook's 4 top airports, revenue summed per flight. Re-implemented from the published data.
