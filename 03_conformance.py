import pm4py
import time

print("Reading log...")
log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")
print("Log loaded.\n")


print("Discovering models...")
alpha_net, alpha_im, alpha_fm = pm4py.discover_petri_net_alpha(log)
ind_net, ind_im, ind_fm = pm4py.discover_petri_net_inductive(log)
print("Models discovered.\n")


print("Computing token-based replay fitness (Alpha)...")
t0 = time.time()
alpha_fit_tbr = pm4py.fitness_token_based_replay(log, alpha_net, alpha_im, alpha_fm)
print(f"  Done in {time.time()-t0:.1f}s")
print("  Alpha — TBR fitness:", alpha_fit_tbr, "\n")

print("Computing token-based replay fitness (Inductive)...")
t0 = time.time()
ind_fit_tbr = pm4py.fitness_token_based_replay(log, ind_net, ind_im, ind_fm)
print(f"  Done in {time.time()-t0:.1f}s")
print("  Inductive — TBR fitness:", ind_fit_tbr, "\n")


print("Computing precision (Alpha)...")
t0 = time.time()
alpha_prec = pm4py.precision_token_based_replay(log, alpha_net, alpha_im, alpha_fm)
print(f"  Done in {time.time()-t0:.1f}s")
print("  Alpha — precision:", alpha_prec, "\n")

print("Computing precision (Inductive)...")
t0 = time.time()
ind_prec = pm4py.precision_token_based_replay(log, ind_net, ind_im, ind_fm)
print(f"  Done in {time.time()-t0:.1f}s")
print("  Inductive — precision:", ind_prec, "\n")

print("Computing alignment-based fitness (Alpha) — this may take a few minutes...")
t0 = time.time()
alpha_fit_ali = pm4py.fitness_alignments(log, alpha_net, alpha_im, alpha_fm)
print(f"  Done in {time.time()-t0:.1f}s")
print("  Alpha — alignment fitness:", alpha_fit_ali, "\n")

print("Computing alignment-based fitness (Inductive) — this may take a few minutes...")
t0 = time.time()
ind_fit_ali = pm4py.fitness_alignments(log, ind_net, ind_im, ind_fm)
print(f"  Done in {time.time()-t0:.1f}s")
print("  Inductive — alignment fitness:", ind_fit_ali, "\n")


print("="*60)
print("SUMMARY")
print("="*60)
print(f"{'Metric':<35} {'Alpha':>10} {'Inductive':>12}")
print("-"*60)
print(f"{'TBR fitness (avg trace fitness)':<35} "
      f"{alpha_fit_tbr['average_trace_fitness']:>10.4f} "
      f"{ind_fit_tbr['average_trace_fitness']:>12.4f}")
print(f"{'TBR fitness (log fitness)':<35} "
      f"{alpha_fit_tbr['log_fitness']:>10.4f} "
      f"{ind_fit_tbr['log_fitness']:>12.4f}")
print(f"{'Alignment fitness (log fitness)':<35} "
      f"{alpha_fit_ali['log_fitness']:>10.4f} "
      f"{ind_fit_ali['log_fitness']:>12.4f}")
print(f"{'Precision (TBR)':<35} "
      f"{alpha_prec:>10.4f} "
      f"{ind_prec:>12.4f}")
print("="*60)