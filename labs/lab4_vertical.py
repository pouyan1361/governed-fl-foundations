"""
LAB 4: VERTICAL FEDERATION. Same patients, different features, two owners.

    python labs/lab4_vertical.py

Horizontal FL (Labs 1 to 3): every hospital has the same 24 features for
DIFFERENT patients. Vertical FL: Northgate (24 clinical features + the label)
and Sierra Health Plan, an insurer (6 claims features) hold different
features for the SAME patients. Neither may send its columns to the other.

The split model: score = X_hospital @ w_h + X_insurer @ w_i + b
  1. the insurer computes its partial score for a batch and sends it over
  2. the hospital adds its own partial score, applies the sigmoid, compares with
     the label, and sends the residual (p - y) back
  3. each party updates ONLY its own weights with its own features
Only partial scores and residuals cross the wire. Never a feature value.

Assumed solved before training: entity alignment (which rows are the same
patient). Real systems use private set intersection for that. We assume the
rows are already aligned, which is what the simulator gives us.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import model, ui
from fl.world import make_world

EPOCHS, B, LR = 30, 64, 0.1

if __name__ == "__main__":
    world = make_world(3, "realistic")
    hosp = world.clients[0]                              # Northgate: clinical features and labels
    Xh, y = hosp.X_train, hosp.y_train
    Xi = world.X_claims_train[hosp.name]                  # the insurer's view of the SAME patients
    Xh_test, y_test = world.test_for(0)
    Xi_test = world.X_claims_test[world.test_source == 0]
    n, dh, di = len(y), Xh.shape[1], Xi.shape[1]
    rng = np.random.default_rng(690)

    ui.title("LAB 4  |  Vertical FL: Northgate (24 clinical features + label) and Sierra Health Plan (6 claims features)")
    print(f"  aligned patients: {n}   hospital features: {dh}   insurer features: {di}")

    # Baseline 1: hospital alone on its 24 features
    theta_h_only = model.local_train(model.init(dh), Xh, y, EPOCHS, B, LR, rng=np.random.default_rng(690))
    acc_h_only = model.accuracy(theta_h_only, Xh_test, y_test)

    # Baseline 2: the forbidden ideal, all 30 features in one table
    X_all, X_all_test = np.hstack([Xh, Xi]), np.hstack([Xh_test, Xi_test])
    theta_all = model.local_train(model.init(dh + di), X_all, y, EPOCHS, B, LR, rng=np.random.default_rng(690))
    acc_all = model.accuracy(theta_all, X_all_test, y_test)

    # Vertical FL: split training
    ui.section("Vertical FL training (what crosses the wire each batch: partial scores one way, residuals the other)")
    w_h, b = np.zeros(dh), 0.0        # hospital's parameters
    w_i = np.zeros(di)                # insurer's parameters
    crossed = 0
    for ep in range(1, EPOCHS + 1):
        order = rng.permutation(n)
        for s in range(0, n, B):
            idx = order[s:s + B]
            z_i = Xi[idx] @ w_i                        # insurer -> hospital: partial scores
            z_h = Xh[idx] @ w_h + b
            p = model.sigmoid(z_h + z_i)
            r = p - y[idx]                             # hospital -> insurer: residuals
            crossed += 2 * len(idx)
            w_h -= LR * Xh[idx].T @ r / len(idx)       # hospital updates its own weights
            b -= LR * float(np.mean(r))
            w_i -= LR * Xi[idx].T @ r / len(idx)       # insurer updates its own weights
        if ep in (1, 5, 10, 20, 30):
            p_test = model.sigmoid(Xh_test @ w_h + b + Xi_test @ w_i)
            print(f"  epoch {ep:>2}: accuracy {np.mean((p_test >= 0.5) == y_test):.3f}   numbers crossed so far: {crossed:,}   feature values crossed: 0")
    p_test = model.sigmoid(Xh_test @ w_h + b + Xi_test @ w_i)
    acc_vfl = float(np.mean((p_test >= 0.5) == y_test))

    ui.section("Result on Northgate's slice of the neutral test set")
    ui.table(["model", "features", "accuracy"], [
        ["hospital alone", dh, ui.f3(acc_h_only)],
        ["vertical FL (hospital + insurer, no columns shared)", dh + di, ui.f3(acc_vfl)],
        ["forbidden: all columns in one table", dh + di, ui.f3(acc_all)],
    ])

    ui.section("What leaked anyway (the naive version is NOT private)")
    # The insurer receives residual r = p - y. If r < 0 the label was 1.
    z_i = Xi @ w_i; z_h = Xh @ w_h + b
    r_all = model.sigmoid(z_h + z_i) - y
    label_guess = (r_all < 0).astype(int)
    print(f"  The insurer sees residuals r = p - y. Rule: r < 0 means readmitted. Labels recovered: {np.mean(label_guess == y):.1%}")
    print("  The hospital sees the insurer's partial scores: a weighted sum of claims features, which still says something about them.")

    ui.notice([
        "Vertical FL reaches the forbidden model's accuracy without either party sending a column.",
        "But the residual gives the insurer every label, and the partial score leaks a projection of the claims data.",
        "Real vertical FL encrypts or masks these intermediate values (homomorphic encryption, secure computation) and uses PSI for alignment.",
        "Governance question: who is the controller of a model trained on two organizations' columns?",
    ])
    ui.note_prompt(4, "What crossed the wire in vertical FL, what leaked anyway, and who should own the resulting model?")
##ANS: Only partial scores and residuals crossed the wire (zero feature values), and vertical FL matched the pooled model (0.834 vs 0.806 for the hospital alone). But the residuals let the insurer recover 100% of the readmission labels, so the model should be jointly controlled under a written agreement, with the hospital as controller of its clinical use.
