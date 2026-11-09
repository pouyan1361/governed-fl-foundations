"""
Assignment 3 charts. Put this file in your fork's labs/ folder and run:

    python labs/make_charts.py

It reads results/a3_results.csv and writes two PNGs into results/:
    chart_a_fedavg_vs_hospitals.png   (FedAvg accuracy vs number of hospitals, one line per skew)
    chart_b_worst_vs_skew.png         (worst-hospital accuracy vs skew, one bar per E, one panel per size)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "results" / "a3_results.csv")
skews = list(dict.fromkeys(df["skew"]))      # keep harness order
sizes = sorted(df["n_clients"].unique())
Es = sorted(df["E"].unique())

# ---- Chart (a): FedAvg accuracy vs number of hospitals, one line per skew ----
E_A = 5 if 5 in Es else Es[0]   # E barely changes final accuracy; say which E you used in the caption
a = df[df["E"] == E_A]
fig, ax = plt.subplots(figsize=(7, 4.5))
for s in skews:
    sub = a[a["skew"] == s].sort_values("n_clients")
    ax.plot(sub["n_clients"], sub["fedavg_acc"] * 100, marker="o", label=s)
cent = a.groupby("n_clients")["centralized_acc"].mean() * 100
ax.plot(cent.index, cent.values, "k--", linewidth=1, label="centralized (avg over skews)")
ax.set_xticks(sizes)
ax.set_xlabel("Number of hospitals in the consortium")
ax.set_ylabel("FedAvg global accuracy on neutral test set (%)")
ax.set_title(f"(a) FedAvg accuracy vs consortium size, E = {E_A}, {df['rounds'].iloc[0]} rounds")
ax.grid(alpha=0.3)
ax.legend(title="skew", fontsize=8, ncol=2)
fig.tight_layout()
fig.savefig(ROOT / "results" / "chart_a_fedavg_vs_hospitals.png", dpi=200)

# ---- Chart (b): worst-hospital accuracy vs skew, one bar per E (one panel per size) ----
fig, axes = plt.subplots(1, len(sizes), figsize=(5 * len(sizes), 4.5), sharey=True)
axes = np.atleast_1d(axes)
x = np.arange(len(skews))
w = 0.8 / len(Es)
for ax, n in zip(axes, sizes):
    sub = df[df["n_clients"] == n]
    for i, E in enumerate(Es):
        vals = [sub[(sub["skew"] == s) & (sub["E"] == E)]["worst_hospital_acc"].iloc[0] * 100 for s in skews]
        ax.bar(x + (i - (len(Es) - 1) / 2) * w, vals, w, label=f"E = {E}")
    # worst hospital on its own (local-only), for comparison
    loc = [sub[sub["skew"] == s]["worst_local_only_acc"].iloc[0] * 100 for s in skews]
    ax.scatter(x, loc, color="black", marker="_", s=300, zorder=3, label="worst local-only")
    ax.set_xticks(x)
    ax.set_xticklabels(skews, rotation=30)
    ax.set_title(f"{n} hospitals")
    ax.set_xlabel("Type of skew")
    ax.set_ylim(65, 85)
    ax.grid(axis="y", alpha=0.3)
axes[0].set_ylabel("Worst hospital's accuracy (%)")
axes[0].legend(fontsize=8)
fig.suptitle("(b) Worst-hospital accuracy under FedAvg, by skew and local epochs E")
fig.tight_layout()
fig.savefig(ROOT / "results" / "chart_b_worst_vs_skew.png", dpi=200)

print("wrote results/chart_a_fedavg_vs_hospitals.png and results/chart_b_worst_vs_skew.png")
