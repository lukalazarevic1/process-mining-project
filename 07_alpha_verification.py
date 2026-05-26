import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.obj import EventLog

# Load the log
log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")

# Discover BOTH nets (we need both for the four quality dimensions)
net_alpha, im_alpha, fm_alpha = pm4py.discover_petri_net_alpha(log)
net_im, im_im, fm_im = pm4py.discover_petri_net_inductive(log)

# === Alpha Miner aggregate verification (Step 6) ===
print("=== Aggregate metrics for Alpha Miner ===")

tbr_fit_alpha = pm4py.fitness_token_based_replay(log, net_alpha, im_alpha, fm_alpha)
print("Alpha TBR fitness dict:", tbr_fit_alpha)

align_fit_alpha = pm4py.fitness_alignments(log, net_alpha, im_alpha, fm_alpha)
print("Alpha Alignment fitness dict:", align_fit_alpha)

prec_alpha = pm4py.precision_token_based_replay(log, net_alpha, im_alpha, fm_alpha)
print("Alpha Precision (escaping edges):", prec_alpha)

# === Generalisation and Simplicity for Alpha Miner (Step 2) ===
print("\n=== Generalisation and Simplicity for Alpha Miner ===")
try:
    gen_alpha = pm4py.generalization_tbr(log, net_alpha, im_alpha, fm_alpha)
    print("Alpha Generalisation (TBR):", gen_alpha)
except Exception as e:
    print(f"Alpha generalisation raised: {type(e).__name__}: {e}")

try:
    simp_alpha = pm4py.simplicity_petri_net(net_alpha, im_alpha, fm_alpha)
    print("Alpha Simplicity:", simp_alpha)
except Exception as e:
    print(f"Alpha simplicity raised: {type(e).__name__}: {e}")

# === Generalisation and Simplicity for Inductive Miner (Step 2) ===
print("\n=== Generalisation and Simplicity for Inductive Miner ===")
try:
    gen_im = pm4py.generalization_tbr(log, net_im, im_im, fm_im)
    print("Inductive Generalisation (TBR):", gen_im)
except Exception as e:
    print(f"Inductive generalisation raised: {type(e).__name__}: {e}")

try:
    simp_im = pm4py.simplicity_petri_net(net_im, im_im, fm_im)
    print("Inductive Simplicity:", simp_im)
except Exception as e:
    print(f"Inductive simplicity raised: {type(e).__name__}: {e}")