"""
LAB 1: FEDERATED AVERAGING FROM SCRATCH. About 60 lines, nothing hidden.

    python labs/lab1_fedavg.py              (fails until you implement weighted_average)
    python -m pytest -q tests/test_lab1.py  (checks your line)

One round of FedAvg:
  1. the coordinator broadcasts the global model theta
  2. every hospital trains E epochs on its own patients, starting from theta
  3. every hospital sends back its new model theta_k (never its patients)
  4. the coordinator averages the models, weighted by how many patients each
     hospital trained on, and that average becomes the next global model

YOUR JOB: implement weighted_average(). It is one line of arithmetic.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import model, ui
from fl.world import make_world, pooled

ROUNDS, E, B, LR = 15, 5, 64, 0.1


def weighted_average(thetas, sizes):
    """thetas: list of model vectors, one per hospital.
    sizes:  list of patient counts, same order.
    Return ONE vector: the average of the thetas, where hospital k counts with
    weight n_k / n_total. Hint: sum(theta_k * (n_k / total) for ...)."""
    total = sum(sizes)
    return sum(theta * (n / total) for theta, n in zip(thetas, sizes))


def run_fedavg(world, verbose=True):
    theta = model.init(world.X_test.shape[1])                      # the global model: all zeros
    rng = np.random.default_rng(690)
    if verbose:
        print(f"{'round':>5} | {'global acc':>10} | " + " ".join(f"{c.name[:12]:>12}" for c in world.clients))
    for r in range(1, ROUNDS + 1):
        thetas, sizes = [], []
        for c in world.clients:                                     # step 2: local work, in parallel in real life
            theta_k = model.local_train(theta, c.X_train, c.y_train, E, B, LR, rng=rng)
            thetas.append(theta_k); sizes.append(c.n)                # step 3: only the model comes back
        theta = weighted_average(thetas, sizes)                     # step 4: YOUR LINE
        if verbose:
            per = " ".join(f"{model.accuracy(theta, *world.test_for(k)):>12.3f}" for k in range(len(world.clients)))
            print(f"{r:>5} | {model.accuracy(theta, world.X_test, world.y_test):>10.3f} | {per}")
    return theta


if __name__ == "__main__":
    world = make_world(3, "realistic")
    ui.title("LAB 1  |  FedAvg from scratch: three hospitals, one model, zero shared records")
    print(world.describe())

    ui.section("The two baselines every federation must be compared against")
    X, y = pooled(world)
    central = model.local_train(model.init(X.shape[1]), X, y, 30, B, LR, rng=np.random.default_rng(690))
    local = {c.name: model.local_train(model.init(X.shape[1]), c.X_train, c.y_train, 100, B, LR, rng=np.random.default_rng(690))
             for c in world.clients}
    print(f"  centralized (the forbidden ideal): accuracy {model.accuracy(central, world.X_test, world.y_test):.3f} on the neutral test set")
    print("  local-only (each hospital alone): see the table below")

    ui.section(f"FedAvg: {ROUNDS} rounds, E={E} local epochs, B={B}, lr={LR}")
    try:
        theta = run_fedavg(world)
    except NotImplementedError as e:
        print(f"\n  {e}\n  Open labs/lab1_fedavg.py, find weighted_average(), and write the line.")
        sys.exit(1)

    ui.section("Who gains from federating?")
    rows = []
    for k, c in enumerate(world.clients):
        Xk, yk = world.test_for(k)
        lo, fe, ce = model.accuracy(local[c.name], Xk, yk), model.accuracy(theta, Xk, yk), model.accuracy(central, Xk, yk)
        rows.append([c.name, c.n, ui.f3(lo), ui.f3(fe), ui.f3(ce), f"{fe - lo:+.3f}"])
    ui.table(["hospital", "patients", "local-only", "FedAvg", "centralized", "gain from FedAvg"], rows)
    print(f"\n  overall on the neutral test set: FedAvg {model.accuracy(theta, world.X_test, world.y_test):.3f}   centralized {model.accuracy(central, world.X_test, world.y_test):.3f}")

    ui.notice([
        "FedAvg matches the centralized model without any record leaving a hospital.",
        "The smallest hospital gains the most. The largest gains almost nothing.",
        "So the question for the consortium agreement is: what does Northgate get for joining?",
        "Every round, each hospital sent 25 numbers (24 weights and a bias). Never a patient.",
    ])
    ui.note_prompt(1, "Which hospital gains most from federating, by how much, and what would you offer Northgate to join?")
