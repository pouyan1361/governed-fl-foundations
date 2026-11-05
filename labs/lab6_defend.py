"""
LAB 6a: ROBUST AGGREGATION. Blunting the poisoners.

    python labs/lab6_defend.py                       attack x defense table (about 15 seconds)
    python labs/lab6_defend.py --attack backdoor --defense median --verbose

Defenses the coordinator can apply without seeing any patient data:
  clip      scale every update down to a maximum norm
  median    per coordinate, take the median across hospitals
  trimmed   per coordinate, drop the largest and smallest, average the rest
  krum      keep only the update closest to its neighbours
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fl import federation as F, ui
from fl.world import make_world

DEFENSES = {
    "none": {},
    "clip": {"clip_norm": 2.0},
    "median": {"aggregator": "median"},
    "trimmed": {"aggregator": "trimmed_mean"},
    "krum": {"aggregator": "krum"},
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--attack", default="all", choices=["all", "none", "boost", "backdoor"])
    ap.add_argument("--defense", default="all", choices=["all"] + list(DEFENSES))
    ap.add_argument("--scale", type=float, default=10.0)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    world = make_world(5, "realistic")
    ui.title("LAB 6a  |  Robust aggregation against the Lab 5 attackers (five hospitals, Three Rivers is dishonest)")
    attacks = ["none", "boost", "backdoor"] if a.attack == "all" else [a.attack]
    defenses = list(DEFENSES) if a.defense == "all" else [a.defense]

    rows = []
    for atk in attacks:
        for dfn in defenses:
            cfg = F.Config(rounds=15, attack=None if atk == "none" else atk, attacker="Three Rivers",
                           attack_scale=a.scale, verbose=a.verbose, **DEFENSES[dfn])
            if a.verbose:
                ui.section(f"attack={atk} defense={dfn}")
            theta, hist = F.run(world, cfg)
            last = hist[-1]
            rows.append([atk, dfn, ui.f3(last["global_acc"]), ui.f3(min(last["per_client"].values())),
                         f"{last['attack_success_rate']:.0%}" if "attack_success_rate" in last else "-",
                         ", ".join(last["clipped"]) or "-"])
    ui.section("Results after 15 rounds")
    ui.table(["attack", "defense", "global acc", "worst hospital", "backdoor success", "clipped in last round"], rows)

    ui.notice([
        "Against boost, everything works: the attack lives in the size of the update, and every defense limits size.",
        "Against the backdoor, clipping is not enough; median, trimmed mean and Krum are.",
        "With no attack, the robust aggregators cost almost nothing here. Their real cost: they can silence an honest outlier, often the small hospital.",
        "None of these needed a single patient record. They are coordinator-side controls.",
    ])
    ui.note_prompt(6, "Which defense would you write into the federation policy as the default aggregator, and why?")
##ANS: Aggregator: trimmed mean, because it restored the boost attack to about 0.81 and cut backdoor success from 57% to 8% at almost no cost without an attack. Minimum participants: 5 per round, because with very few members the sum reveals individual updates and DP becomes expensive (0.678 at noise 1.0 with 3 hospitals vs 0.785 with 5). Noise multiplier: 0.3, which cost nothing for five hospitals in my run (0.814, same as no noise).
