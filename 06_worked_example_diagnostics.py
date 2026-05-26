import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.evaluation.precision import algorithm as precision_eval
from pm4py.algo.evaluation.precision.variants import etconformance_token
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.obj import EventLog

# === 1. Re-discover the Inductive Miner net (or load yours) ===
# Replace this if you already have `log`, `net_im`, `im_im`, `fm_im` in memory
log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")
net_im, im_im, fm_im = pm4py.discover_petri_net_inductive(log)

# === 2. Aggregate fitness and precision (re-verify Table 4) ===
print("=== Aggregate metrics for Inductive Miner ===")
tbr_fit = pm4py.fitness_token_based_replay(log, net_im, im_im, fm_im)
print("TBR fitness dict:", tbr_fit)

align_fit = pm4py.fitness_alignments(log, net_im, im_im, fm_im)
print("Alignment fitness dict:", align_fit)

prec = pm4py.precision_token_based_replay(log, net_im, im_im, fm_im)
print("Precision (escaping edges):", prec)

# === 3. Per-trace alignment details for trace 0 (worked example) ===
print("\n=== Trace 0 alignment ===")

# Convert the DataFrame to an EventLog so we can index by trace
event_log = log_converter.apply(log, variant=log_converter.Variants.TO_EVENT_LOG)

first_trace = event_log[0]
print("Trace length (events):", len(first_trace))
print("Activities in trace 0:", [e["concept:name"] for e in first_trace])

# Compute the full alignment object (not just the fitness scalar)
aligned_traces = alignments.apply_log(
    EventLog([first_trace]),
    net_im, im_im, fm_im
)
trace0_alignment = aligned_traces[0]

print("\n--- Equation 2 inputs for trace 0 ---")
print("Optimal alignment cost:", trace0_alignment.get("cost"))
print("Per-trace fitness:", trace0_alignment.get("fitness"))
# cost_worst can be derived: fitness = 1 - cost/cost_worst  =>  cost_worst = cost / (1 - fitness)
cost = trace0_alignment.get("cost")
fit = trace0_alignment.get("fitness")
if fit is not None and fit < 1:
    print("Implied cost_worst:", cost / (1 - fit))
else:
    # If fitness is exactly 1, the trace has no deviations and the formula divides by zero.
    # In that case cost_worst can be approximated as (trace_length + num_visible_transitions).
    visible_transitions = [t for t in net_im.transitions if t.label is not None]
    print("Implied cost_worst (formula approx):",
          len(first_trace) + len(visible_transitions))

print("\nFull alignment dict for trace 0:")
for k, v in trace0_alignment.items():
    if k != "alignment":
        print(f"  {k}: {v}")

print("\nAlignment moves (event, model_transition):")
for move in trace0_alignment["alignment"]:
    print(" ", move)

# === 4. Precision diagnostics: per-state observed vs enabled activities ===
print("\n=== Precision diagnostics for Inductive Miner ===")
prec_detailed = pm4py.precision_token_based_replay(log, net_im, im_im, fm_im)
print("Aggregate precision value:", prec_detailed)

# If you have access to the lower-level diagnostics, also run:
try:
    from pm4py.algo.evaluation.precision.variants.etconformance_token import \
        get_log_prefixes, get_prefixes_from_log
    prefixes, prefix_count = get_log_prefixes(event_log)
    print(f"\nNumber of distinct prefixes (states) visited: {len(prefixes)}")
    # Print the 5 most frequent prefixes and their counts
    sorted_prefixes = sorted(prefix_count.items(), key=lambda x: -x[1])[:5]
    for p, c in sorted_prefixes:
        print(f"  prefix={p}  count={c}")
except ImportError:
    print("(prefix extraction helpers not exposed in this PM4Py version)")

# === 5. Soundness check (Step 1) ===
print("\n=== Soundness check ===")
from pm4py.algo.analysis.check_soundness import algorithm as check_soundness

# Re-discover the Alpha net so we can check it (also needed for Step 6)
net_alpha, im_alpha, fm_alpha = pm4py.discover_petri_net_alpha(log)

try:
    alpha_sound = check_soundness.check_easy_soundness_net_in_fin_marking(
        net_alpha, im_alpha, fm_alpha
    )
    print(f"Alpha Miner net is easy-sound: {alpha_sound}")
except Exception as e:
    print(f"Alpha soundness check raised: {type(e).__name__}: {e}")

try:
    inductive_sound = check_soundness.check_easy_soundness_net_in_fin_marking(
        net_im, im_im, fm_im
    )
    print(f"Inductive Miner net is easy-sound: {inductive_sound}")
except Exception as e:
    print(f"Inductive soundness check raised: {type(e).__name__}: {e}")
    
# === 6. Alpha Miner aggregate verification (Step 6) ===
print("\n=== Aggregate metrics for Alpha Miner ===")
tbr_fit_alpha = pm4py.fitness_token_based_replay(log, net_alpha, im_alpha, fm_alpha)
print("Alpha TBR fitness dict:", tbr_fit_alpha)

align_fit_alpha = pm4py.fitness_alignments(log, net_alpha, im_alpha, fm_alpha)
print("Alpha Alignment fitness dict:", align_fit_alpha)

prec_alpha = pm4py.precision_token_based_replay(log, net_alpha, im_alpha, fm_alpha)
print("Alpha Precision (escaping edges):", prec_alpha)