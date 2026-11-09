"""
LAB 3: CLIENT HETEROGENEITY. When hospitals differ, who pays?

    python labs/lab3_skew.py --skew none
    python labs/lab3_skew.py --skew label
    python labs/lab3_skew.py --skew quantity
    python labs/lab3_skew.py --skew feature
    python labs/lab3_skew.py --skew concept
    python labs/lab3_skew.py --skew label --finetune     personalization: fine-tune the global model locally
    python labs/lab3_skew.py --skew concept --E 50       many local epochs (client drift)

For each hospital: local-only vs FedAvg vs centralized, on that hospital's
slice of the neutral test set. Then an optional personalized row.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import federation as F, model, ui
from fl.world import make_world

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--skew", default="label", choices=["none", "label", "quantity", "feature", "concept", "realistic"])
    ap.add_argument("--E", type=int, default=5)
    ap.add_argument("--prox", type=float, default=0.0, help="FedProx strength (0 = plain FedAvg)")
    ap.add_argument("--finetune", action="store_true", help="each hospital fine-tunes the global model on its own data")
    a = ap.parse_args()

    world = make_world(3, a.skew)
    ui.title(f"LAB 3  |  Heterogeneity, skew = {a.skew}")
    print(world.describe())

    central = F.centralized(world)
    local = F.local_only(world, epochs=100)
    ui.section(f"FedAvg, 20 rounds, E={a.E}" + (f", FedProx mu={a.prox}" if a.prox else ""))
    theta, hist = F.run(world, F.Config(rounds=20, E=a.E, prox_mu=a.prox, verbose=True))

    ui.section("Per hospital, on that hospital's slice of the neutral test set")
    rows = []
    for k, c in enumerate(world.clients):
        Xk, yk = world.test_for(k)
        row = [c.name, c.n, f"{c.y_train.mean():.2f}", ui.f3(model.accuracy(local[c.name], Xk, yk)),
               ui.f3(model.accuracy(theta, Xk, yk)), ui.f3(model.accuracy(central, Xk, yk))]
        if a.finetune:
            pers = model.local_train(theta, c.X_train, c.y_train, 5, 64, 0.1, rng=np.random.default_rng(1))
            row.append(ui.f3(model.accuracy(pers, Xk, yk)))
        rows.append(row)
    headers = ["hospital", "patients", "readmit rate", "local-only", "FedAvg", "centralized"] + (["FedAvg + local fine-tune"] if a.finetune else [])
    ui.table(headers, rows)

    tips = {
        "none": ["With identical hospitals, FedAvg equals centralized for everyone. This is the textbook case and it is rare."],
        "label": ["Same patients, different readmission rates. One global model, one threshold, three base rates: the hospital with the unusual rate pays.",
                  "Try --finetune: a few local epochs on top of the global model recover most of it. That is personalized FL in one line."],
        "quantity": ["The 60-patient hospital cannot learn 24 weights alone, so it gains the most from the federation.",
                     "But it also has the least say in the weighted average. Fair? Try the simple_mean aggregator in Lab 7's policy."],
        "feature": ["Older, sicker patients at one hospital shift the inputs, not the rule. FedAvg copes; the global model generalizes."],
        "concept": ["At Kestrel a facility discharge and living alone mean the OPPOSITE of what they mean elsewhere.",
                    "The average of two opposite rules is no rule. Kestrel does better ALONE. Federation is not always the answer.",
                    "Try --finetune: personalization repairs it. Try --E 50: with a convex model drift is mild; with deep nets it is not."],
        "realistic": ["A mix of everything. The small hospital gains; the medium one is roughly even; the large one gains nothing."],
    }
    ui.notice(tips[a.skew] + ["Write down WHICH hospital paid under this skew. Assignment 3 asks you to design these experiments."])
    ui.note_prompt(3, "Which skew hurt the most, which hospital paid, and what fixed it?")
##ANS: Label skew hurt most: Kestrel (readmission rate 0.48) fell from 0.786 alone to 0.730 with FedAvg, because one global threshold cannot fit three different base rates. Local fine-tuning fixed it (0.792); under concept skew Kestrel was also better alone (0.828 vs 0.804) and fine-tuning restored 0.828.

