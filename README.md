# Process Mining Project

MSc Computer Science, Process Mining course, University of Camerino.
Supervisor: Prof. Barbara Re.

Comparison of the Alpha Miner and the Inductive Miner on the Sepsis Cases
event log (Mannhardt, 2016, 4TU.ResearchData), using PM4Py.
The project addresses **objective (c)** of the course project guidelines:
_compare the results of two algorithms using a tool_.

## Scripts

- `01_explore.py` — imports the log and prints general statistics
  (number of cases, events, activities, start/end activities, variants)
- `02_discovery.py` — applies the Alpha Miner and Inductive Miner and saves
  the resulting Petri nets as `alpha_petri.png` and `inductive_petri.png`
- `03_conformance.py` — computes log fitness (token-based replay and
  alignment-based replay) and precision (escaping-edges) for both models,
  and prints a summary table
- `04_extra_stats.py` — computes trace length statistics (min, median,
  mean, max) and lists the five most frequent variants
- `05_diagnostic.py` — extracts the per-trace diagnostic information used
  in the worked example of the report (token-replay output of the Alpha
  model and the optimal alignment of the Inductive model for the first
  trace)
- `06_worked_example_diagnostics.py` — produces the per-trace alignment
  cost, worst-case cost (`bwc`), and precision diagnostics used in the
  worked example of Section 4.3.4 of the report; also runs an
  easy-soundness check on both nets and re-verifies the aggregate Alpha
  Miner metrics
- `07_alpha_verification.py` — re-verifies the aggregate Alpha Miner
  metrics and computes the generalisation (token-based) and simplicity
  dimensions for both models (reported as the two additional rows of
  Table 4 in the report)

## Requirements

- Python 3.10+
- pm4py
- graphviz (system binary and Python package)

The Sepsis Cases event log (`Sepsis Cases - Event Log.xes.gz`) must be
placed in the project root. It is publicly available from the
4TU.ResearchData repository under the DOI
10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460.

## Usage

Run the scripts from the project root, in numbered order:

    python3 01_explore.py
    python3 02_discovery.py
    python3 03_conformance.py
    python3 04_extra_stats.py
    python3 05_diagnostic.py
    python3 06_worked_example_diagnostics.py
    python3 07_alpha_verification.py

Approximate runtimes on a standard laptop:

- `01`, `02`, `04`, `05` — a few seconds each
- `03_conformance.py` — around seven minutes (alignment-based fitness
  on the Inductive Miner net is the slow step)
- `06_worked_example_diagnostics.py` — around seven minutes (same
  alignment computation, plus the per-trace diagnostic extraction)
- `07_alpha_verification.py` — around one minute

## Outputs

- `alpha_petri.png`, `inductive_petri.png` — discovered Petri nets
  (also shown as Figures in the report's appendix)
- Console output of `03_conformance.py` — full conformance summary table
  (token-based fitness, alignment-based fitness, precision, percentage
  of fully fitting traces) for both algorithms
- `worked_example_output_v3.txt` — captured output of
  `06_worked_example_diagnostics.py`, including the alignment cost,
  worst-case cost, fitness, visited-states count, and full alignment
  moves for the first trace of the log
- `generalisation_simplicity_output.txt` — captured output of
  `07_alpha_verification.py`, including the four Alpha Miner aggregate
  metrics and the generalisation and simplicity values for both
  algorithms
