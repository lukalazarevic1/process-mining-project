import pm4py

print("Reading log...")
log = pm4py.read_xes("Sepsis Cases - Event Log.xes.gz")
print("Log loaded.\n")


print("Running Alpha Miner...")
alpha_net, alpha_im, alpha_fm = pm4py.discover_petri_net_alpha(log)
pm4py.save_vis_petri_net(alpha_net, alpha_im, alpha_fm, "alpha_petri.png")
print("Saved: alpha_petri.png\n")


print("Running Inductive Miner...")
ind_net, ind_im, ind_fm = pm4py.discover_petri_net_inductive(log)
pm4py.save_vis_petri_net(ind_net, ind_im, ind_fm, "inductive_petri.png")
print("Saved: inductive_petri.png\n")

print("Done.")