# BANA 690A Federated Learning I: Lab Notes

**Name:** Denise Anciola
**GitHub username:** @denisecanciola99

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?

What the coordinator holds
  A neutral, consented evaluation set: 500 de-identified rows from each hospital's population.
  Zero training records. The coordinator never sees a hospital's patients.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?
Kestrel gained the most: 69.6% alone vs 79.8% with FedAvg, +10.2 points, because it only has 60 patients. Northgate (1,800 patients) gained just +1.0 (81.0% to 82.0%) while supplying most of the signal, so I'd offer it a permanent Steering Committee seat, a reduced cost share weighted by data contributed, and the right to deploy the global model first.

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
Local epochs (E) cut communication the most: in my A3 grid, average rounds to converge fell from 21.4 at E=1 to 4.7 at E=5 and 1.7 at E=20, while FedAvg accuracy moved less than half a point. The price is more local drift under skew, and E did not help the worst hospital under label skew (73.6% vs 73.4% at E=1 vs 20 with 5 hospitals).

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
Label skew hurt most. Kestrel (48% readmission rate) paid, losing 5.6 points vs training alone. Local fine-tuning fixed it, recovering 6.2 points

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
Only partial scores and residuals crossed the wire (108,000 numbers over 30 epochs, 0 feature values), and the joint model reached 83.4% vs 80.6% for Northgate alone, the same as pooling all columns. But the residual signs gave Sierra Health Plan 100% of the readmission labels, and the partial scores leak a projection of the claims data. The model should be jointly controlled under a written agreement, with Northgate as controller for patient labels and neither party allowed to deploy or reuse it without the other's consent.

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?
FL keeps raw data at home, but the update can be the record: from a one-patient update the coordinator rebuilt every feature exactly (max error 1.1e-16). Update norms would have caught boost (10.37) and backdoor (8.12), since normal updates ranged 0.23 to 1.79, but not label flipping (1.04 and 1.79, inside the normal range), and Northgate's flip still dropped global accuracy from 81.4% to 72.7%.

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
**Aggregator:** Trimmed mean, because plain FedAvg gives every update full weight so one poisoned hospital can pull the global model, while trimmed mean drops the extreme updates and holds up to f attackers at little cost on clean data.

**Minimum participants per round:** 5, because in lab6_dp.py the accuracy cost of noise 1.0 fell from 12.3 points with 3 hospitals to 2.9 with 5, so privacy is only affordable once at least 5 members contribute each round.

**Noise multiplier (5 hospitals):** 0.5, because it cost only 0.8 points (0.814 to 0.806 in lab6_dp.py) while 1.0 cost 2.9, which is meaningful privacy for almost no accuracy loss.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
I chose robust aggregation (trimmed mean), so secure_aggregation is false, because poisoning can't be stopped if the coordinator can't see individual updates. The compensating control is DP noise 0.5 plus a neutral third-party coordinator instead of Northgate Health IT, since the coordinator can now read each hospital's update. Clause: the coordinator may not be a member hospital and must keep an audit log of every round that the Steering Committee reviews.

## Declaration
I ran these labs myself in my own Codespace. Denise Anciola
