"""
LAB 5b: INFERENCE ATTACKS. The model update is not harmless.

    python labs/lab5_leak.py                 reconstruct a patient from one gradient
    python labs/lab5_leak.py --batch 8       the same attack on an 8-patient update
    python labs/lab5_leak.py --secagg        the same attack when updates are masked (Lab 6)

Then a membership inference attack: can an outsider tell whether a given
patient was in Kestrel's training data, just from the model's loss on them?
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import federation as F, model, privacy, ui
from fl.world import make_world, to_human

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=1, help="patients in the update the coordinator receives")
    ap.add_argument("--secagg", action="store_true", help="updates are masked before the coordinator sees them")
    ap.add_argument("--patient", type=int, default=0)
    a = ap.parse_args()

    world = make_world(3, "realistic")
    kestrel = world.clients[2]
    theta = F.centralized(world)                 # any current global model will do

    ui.title("LAB 5b  |  Gradient leakage: reading a patient out of an update")
    print("  The coordinator receives from Kestrel the gradient of the loss on a batch of patients.")
    print("  For logistic regression that gradient is (p - y) * [x, 1] averaged over the batch.")
    print("  With ONE patient, divide the weight part by the bias part and x comes back exactly.\n")

    idx = slice(a.patient, a.patient + a.batch)
    X, y = kestrel.X_train[idx], kestrel.y_train[idx]
    true_x = kestrel.X_train[a.patient]
    grads = [model.gradient(theta, X, y)]
    if a.secagg:
        others = [model.gradient(theta, c.X_train[:a.batch], c.y_train[:a.batch]) for c in world.clients[:2]]
        _, masked = privacy.secure_aggregate(others + grads, return_masked=True)
        grads = [masked[-1]]
        print("  Secure aggregation is ON: the coordinator sees Kestrel's MASKED update.\n")

    recon = privacy.reconstruct_from_gradient(grads[0])
    err = float(np.max(np.abs(recon - true_x))) if recon is not None else float("inf")
    print(f"  update built from {a.batch} patient(s)   max reconstruction error: {err:.2e}")
    ui.section("Original vs reconstructed (human units)")
    orig, rec = to_human(true_x), to_human(recon) if recon is not None else {}
    rows = [[k, orig[k], rec.get(k, "?"), "match" if orig[k] == rec.get(k) else "no"] for k in list(orig)[:12]]
    ui.table(["feature", "actual patient", "reconstructed", ""], rows)
    print(f"  ... {len(orig) - 12} more features, same story.   Readmitted: {'yes' if y[0] == 1 else 'no'}")

    ui.section("Membership inference: was this patient in Kestrel's training set?")
    Xo, yo = world.test_for(2)
    local = F.local_only(world, epochs=100)["Kestrel"]
    fed, _ = F.run(world, F.Config(rounds=15, verbose=False))
    rows = []
    for name, th in [("Kestrel's local-only model", local), ("the federated global model", fed)]:
        acc, _ = privacy.membership_inference_loss(th, kestrel.X_train, kestrel.y_train, Xo[:kestrel.n], yo[:kestrel.n])
        rows.append([name, f"{acc:.0%}", "coin flip is 50%"])
    ui.table(["model the attacker queries", "attack accuracy", ""], rows)

    ui.notice([
        "One patient per update: exact reconstruction, no optimization needed. The update IS the record.",
        "Eight patients per update: the arithmetic no longer separates them (deep nets are less lucky: optimization attacks still work).",
        "With secure aggregation the coordinator sees noise; only the sum across hospitals is meaningful.",
        "A small hospital's own model memorizes its patients; the federated model memorizes them less. Federation helped here.",
    ])
    ui.note_prompt(5, "After this lab, finish the sentence: 'FL keeps raw data at home, but ...'")
##ANS: FL keeps raw data at home, but a single-patient update reveals that patient exactly (reconstruction error 1.1e-16), and one member can poison everyone (boost drops global accuracy to 0.506). Update norms alone would catch boost (norm 10.37) and the backdoor (8.12) against a normal range of 0.23 to 1.79, but not label flipping (norm 1.04, inside the normal range).
