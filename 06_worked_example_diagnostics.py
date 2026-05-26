import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.evaluation.precision import algorithm as precision_eval
from pm4py.algo.evaluation.precision.variants import etconformance_token
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.obj import EventLog


log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")
net_im, im_im, fm_im = pm4py.discover_petri_net_inductive(log)


print("=== Aggregate metrics for Inductive Miner ===")
tbr_fit = pm4py.fitness_token_based_replay(log, net_im, im_im, fm_im)
print("TBR fitness dict:", tbr_fit)

align_fit = pm4py.fitness_alignments(log, net_im, im_im, fm_im)
print("Alignment fitness dict:", align_fit)

prec = pm4py.precision_token_based_replay(log, net_im, im_im, fm_im)
print("Precision (escaping edges):", prec)


print("\n=== Trace 0 alignment ===")


event_log = log_converter.apply(log, variant=log_converter.Variants.TO_EVENT_LOG)

first_trace = event_log[0]
print("Trace length (events):", len(first_trace))
print("Activities in trace 0:", [e["concept:name"] for e in first_trace])


aligned_traces = alignments.apply_log(
    EventLog([first_trace]),
    net_im, im_im, fm_im
)
trace0_alignment = aligned_traces[0]

print("\n--- Equation 2 inputs for trace 0 ---")
print("Optimal alignment cost:", trace0_alignment.get("cost"))
print("Per-trace fitness:", trace0_alignment.get("fitness"))

cost = trace0_alignment.get("cost")
fit = trace0_alignment.get("fitness")
if fit is not None and fit < 1:
    print("Implied cost_worst:", cost / (1 - fit))
else:
    
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


print("\n=== Precision diagnostics for Inductive Miner ===")
prec_detailed = pm4py.precision_token_based_replay(log, net_im, im_im, fm_im)
print("Aggregate precision value:", prec_detailed)


try:
    from pm4py.algo.evaluation.precision.variants.etconformance_token import \
        get_log_prefixes, get_prefixes_from_log
    prefixes, prefix_count = get_log_prefixes(event_log)
    print(f"\nNumber of distinct prefixes (states) visited: {len(prefixes)}")
    
    sorted_prefixes = sorted(prefix_count.items(), key=lambda x: -x[1])[:5]
    for p, c in sorted_prefixes:
        print(f"  prefix={p}  count={c}")
except ImportError:
    print("(prefix extraction helpers not exposed in this PM4Py version)")


print("\n=== Soundness check ===")
from pm4py.algo.analysis.check_soundness import algorithm as check_soundness


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
    

print("\n=== Aggregate metrics for Alpha Miner ===")
tbr_fit_alpha = pm4py.fitness_token_based_replay(log, net_alpha, im_alpha, fm_alpha)
print("Alpha TBR fitness dict:", tbr_fit_alpha)

align_fit_alpha = pm4py.fitness_alignments(log, net_alpha, im_alpha, fm_alpha)
print("Alpha Alignment fitness dict:", align_fit_alpha)

prec_alpha = pm4py.precision_token_based_replay(log, net_alpha, im_alpha, fm_alpha)
print("Alpha Precision (escaping edges):", prec_alpha)