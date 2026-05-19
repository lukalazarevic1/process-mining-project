import pm4py
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments

log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")
ind_net, ind_im, ind_fm = pm4py.discover_petri_net_inductive(log)
alpha_net, alpha_im, alpha_fm = pm4py.discover_petri_net_alpha(log)


print("=== Token-based replay (Alpha) — detailed per-trace output ===")
replay = token_replay.apply(log, alpha_net, alpha_im, alpha_fm)

for i, r in enumerate(replay[:20]):
    print(f"\nTrace {i}: trace_fitness={r['trace_fitness']:.4f}, "
          f"is_fit={r['trace_is_fit']}, "
          f"produced_tokens={r['produced_tokens']}, "
          f"consumed_tokens={r['consumed_tokens']}, "
          f"missing_tokens={r['missing_tokens']}, "
          f"remaining_tokens={r['remaining_tokens']}")
    if not r['trace_is_fit']:
        print(f"  Activated transitions: {[str(t) for t in r['activated_transitions']]}")
        break


print("\n\n=== Alignment-based replay (Inductive) — first trace ===")
ali = alignments.apply(log, ind_net, ind_im, ind_fm,
                       variant=alignments.Variants.VERSION_DIJKSTRA_NO_HEURISTICS)
first = ali[0]
print(f"Cost: {first['cost']}, Fitness: {first['fitness']:.4f}")
print("Alignment pairs (event, transition):")
for pair in first['alignment'][:15]:
    print(f"  {pair}")