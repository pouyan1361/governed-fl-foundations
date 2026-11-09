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

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
Label skew hurt most. Kestrel (48% readmission rate) paid, losing 5.6 points vs training alone. Local fine-tuning fixed it, recovering 6.2 points

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
**Aggregator:** Trimmed mean, because plain FedAvg gives every update full weight so one poisoned hospital can pull the global model, while trimmed mean drops the extreme updates and holds up to f attackers at little cost on clean data.

**Minimum participants per round:** 5, because in lab6_dp.py the accuracy cost of noise 1.0 fell from 12.3 points with 3 hospitals to 2.9 with 5, so privacy is only affordable once at least 5 members contribute each round.

**Noise multiplier (5 hospitals):** 0.5, because it cost only 0.8 points (0.814 to 0.806 in lab6_dp.py) while 1.0 cost 2.9, which is meaningful privacy for almost no accuracy loss.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?

## Declaration
I ran these labs myself in my own Codespace. (type your name)
