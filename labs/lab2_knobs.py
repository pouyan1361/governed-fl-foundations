"""
LAB 2: McMAHAN'S KNOBS. Communication rounds are the cost that matters.

    python labs/lab2_knobs.py                 one run with the defaults
    python labs/lab2_knobs.py --E 20 --C 0.34 one run with your knobs
    python labs/lab2_knobs.py --grid          the whole table (E x C), about 10 seconds
    python labs/lab2_knobs.py --grid --skew label   the same table on skewed hospitals

The knobs (McMahan et al. 2017):
  C  fraction of hospitals that participate in a round
  E  local epochs each participant runs before reporting back
  B  local batch size
"Converged" here means the test log loss is within 2 percent of the
centralized model's. Log loss, not accuracy: for logistic regression the
accuracy is nearly right after one tiny step (only the direction matters),
so accuracy hides how far the model still has to travel.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import federation as F, model, ui
from fl.world import make_world

LR, B, MAX_ROUNDS = 0.05, 64, 100


def rounds_to_converge(world, E, C, target):
    rng = np.random.default_rng(690)
    theta = model.init(world.X_test.shape[1])
    n_sel = max(1, int(round(C * len(world.clients))))
    for r in range(1, MAX_ROUNDS + 1):
        chosen = sorted(rng.choice(len(world.clients), n_sel, replace=False).tolist()) if n_sel < len(world.clients) else range(len(world.clients))
        thetas, sizes = [], []
        for k in chosen:
            c = world.clients[k]
            thetas.append(model.local_train(theta, c.X_train, c.y_train, E, B, LR, rng=rng)); sizes.append(c.n)
        total = sum(sizes)
        theta = sum(t * (n / total) for t, n in zip(thetas, sizes))
        if model.loss(theta, world.X_test, world.y_test) <= target:
            return r, model.accuracy(theta, world.X_test, world.y_test)
    return None, model.accuracy(theta, world.X_test, world.y_test)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--E", type=int, default=5)
    ap.add_argument("--C", type=float, default=1.0)
    ap.add_argument("--skew", default="none")
    ap.add_argument("--grid", action="store_true")
    a = ap.parse_args()

    world = make_world(3, a.skew)
    central = F.centralized(world, epochs=100, lr=LR)
    target = model.loss(central, world.X_test, world.y_test) * 1.02
    ui.title(f"LAB 2  |  Rounds to converge, skew = {a.skew}   (target: test loss within 2% of centralized, {target:.4f})")

    if a.grid:
        rows = []
        for E in [1, 5, 20]:
            row = [f"E={E}"]
            for C in [0.34, 0.67, 1.0]:
                r, acc = rounds_to_converge(world, E, C, target)
                row.append(f"{r if r else '>'+str(MAX_ROUNDS)} rounds ({E * (r or MAX_ROUNDS)} local epochs)")
            rows.append(row)
        ui.table(["", "C=0.34 (1 of 3)", "C=0.67 (2 of 3)", "C=1.0 (all 3)"], rows)
        ui.notice([
            "Down a column: more local epochs per round, far fewer rounds. That is the paper's headline.",
            "Across a row: more hospitals per round helps a little; the big lever is E.",
            "Read the local-epoch totals: fewer rounds cost MORE total computation. Communication is what you save.",
            "Rerun with --skew realistic: with one hospital per round (C=0.34), many local epochs help less, because each round now drifts toward one hospital.",
        ])
    else:
        r, acc = rounds_to_converge(world, a.E, a.C, target)
        print(f"  E={a.E}  C={a.C}  ->  {'converged in ' + str(r) + ' rounds' if r else 'did not converge in ' + str(MAX_ROUNDS)}   (accuracy {acc:.3f})")
        print("  Each round moves 25 numbers per participating hospital. Try --grid for the full table.")
    ui.note_prompt(2, "From the grid: which knob cuts rounds the most, and what do you pay for it?")
##ANS: Local epochs (E) cut rounds the most: 27 rounds at E=1 down to 2 rounds at E=20 with all hospitals participating. The price is more total computation (40 local epochs instead of 27) and more drift toward individual hospitals when data are skewed.
