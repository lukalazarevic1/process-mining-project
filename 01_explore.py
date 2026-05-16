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