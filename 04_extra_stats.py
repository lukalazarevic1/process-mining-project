import pm4py
import pandas as pd

log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")

trace_lengths = log.groupby("case:concept:name").size()
print("Average trace length:", trace_lengths.mean())
print("Median trace length:", trace_lengths.median())
print("Min trace length:", trace_lengths.min())
print("Max trace length:", trace_lengths.max())


variants = pm4py.get_variants(log)
top_variants = sorted(variants.items(), key=lambda x: len(x[1]) if hasattr(x[1], '__len__') else x[1], reverse=True)[:5]
print("\nTop 5 most common variants (by frequency):")
for v, traces in top_variants:
    count = len(traces) if hasattr(traces, '__len__') else traces
    print(f"  {count} cases: {v}")