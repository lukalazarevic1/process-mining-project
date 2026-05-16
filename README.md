# Process Mining Project

MSc Computer Science, Process Mining course, University of Camerino.
Supervisor: Prof. Barbara Re.

Comparison of the Alpha Miner and the Inductive Miner on the Sepsis Cases
event log (Mannhardt, 2016, 4TU.ResearchData), using PM4Py.

## Scripts

- `01_explore.py` imports the log and prints general statistics
- `02_discovery.py` applies the Alpha Miner and Inductive Miner, saves Petri nets
- `03_conformance.py` computes fitness (token-based and alignment-based) and precision
- `04_extra_stats.py` computes trace length statistics and most frequent variants

## Requirements

- Python 3.10+
- pm4py
- graphviz (system binary and Python package)

## Usage

Run each script from the project root:

    python3 01_explore.py
    python3 02_discovery.py
    python3 03_conformance.py
    python3 04_extra_stats.py
