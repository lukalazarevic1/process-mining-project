import pm4py
from collections import Counter


log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")


print("Number of traces:", log["case:concept:name"].nunique())
print("Number of events:", len(log))


activity_counts = log["concept:name"].value_counts().to_dict()
print("\nActivity counts:")
for activity, count in activity_counts.items():
    print(f"  {activity}: {count}")


start_activities = pm4py.get_start_activities(log)
end_activities = pm4py.get_end_activities(log)
print("\nNumber of start activities:", len(start_activities))
print("Start activities:", start_activities)
print("\nNumber of end activities:", len(end_activities))
print("End activities:", end_activities)


variants = pm4py.get_variants(log)
print("\nNumber of variants:", len(variants))


# === Directly-follows graph for visual log overview ===
# Keep only the top-K variants by frequency, then build the DFG of that subset.
# This avoids the visualiser's KeyError on orphan activities and gives a clean
# overview of the log's dominant behaviour.

def variant_size(v):
    # PM4Py versions disagree: some return a list of traces per variant, some an int count.
    return v if isinstance(v, int) else len(v)

K = 20
sorted_variants = sorted(variants.items(), key=lambda x: -variant_size(x[1]))
top_variant_keys = [v[0] for v in sorted_variants[:K]]

log_top = pm4py.filter_variants(log, top_variant_keys)

dfg_f, sa_f, ea_f = pm4py.discover_dfg(log_top)
pm4py.save_vis_dfg(dfg_f, sa_f, ea_f, "sepsis_dfg.png")

covered_cases = sum(variant_size(v[1]) for v in sorted_variants[:K])
print(f"\nDirectly-follows graph saved to sepsis_dfg.png "
      f"(top {K} variants, covering {covered_cases} of "
      f"{log['case:concept:name'].nunique()} cases)")