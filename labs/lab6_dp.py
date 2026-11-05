"""
LAB 6c: DIFFERENTIAL PRIVACY. Buying plausible deniability with accuracy.

    python labs/lab6_dp.py                        noise multiplier x consortium size table
    python labs/lab6_dp.py --noise 0.5 --hospitals 3 --verbose

Client-level DP, central version: clip each hospital's update to norm 1.0,
add Gaussian noise with standard deviation (noise multiplier x 1.0) to the
sum, then average. The noise hides any ONE hospital's contribution. The
price is accuracy, and the price falls as the consortium grows.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import federation as F, ui
from fl.world import make_world

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--noise", type=float, default=None)
    ap.add_argument("--hospitals", type=int, default=None)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    ui.title("LAB 6c  |  Differential privacy: accuracy vs noise multiplier vs consortium size")
    noises = [a.noise] if a.noise is not None else [0.0, 0.1, 0.3, 0.5, 1.0]
    sizes = [a.hospitals] if a.hospitals is not None else [3, 5, 10]
    rows = []
    for n in sizes:
        world = make_world(n, "realistic")
        row = [f"{n} hospitals"]
        for s in noises:
            theta, hist = F.run(world, F.Config(rounds=15, clip_norm=1.0, dp_noise=s, verbose=a.verbose))
            row.append(ui.f3(hist[-1]["global_acc"]))
        rows.append(row)
    ui.table([""] + [f"noise {s}" for s in noises], rows)

    ui.notice([
        "Noise 0 is plain FedAvg with clipping. Each step to the right hides any one hospital better.",
        "With 3 hospitals the price is steep; with 10 it almost disappears. More members, cheaper privacy. Membership is a privacy lever.",
        "The noise multiplier becomes an epsilon through a privacy accountant over all rounds; the primer on Canvas gives the intuition.",
        "Which cell would you defend to the AI Risk Committee? That number goes into the policy in Lab 7.",
    ])
    ui.note_prompt(6, "Pick a noise multiplier for a 5-hospital consortium and give one sentence of justification.")
##ANS: Default aggregator: trimmed mean, because it restored boost to about 0.81 and cut backdoor success from 57% to 8% at almost no clean cost. Minimum participants: 5 per round, because with two or three members the sum reveals individual updates and the DP cost is steep (0.678 at noise 1.0 with 3 hospitals). Noise multiplier: 0.3 for five hospitals, which cost nothing in my run (0.814)