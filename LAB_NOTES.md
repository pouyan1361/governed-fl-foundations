# BANA 690A Federated Learning I: Lab Notes

**Name:*Aastha Malhotra*
**GitHub username:*am-malhotra*

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?
AM: The coordinator holds only a neutral evaluation set, not any hospital’s raw training data.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?
AM: Kestrel gains the most, about +0.102; Northgate gains only +0.010. I would offer Northgate a modest governance and fee-sharing deal because its data contribution is large, but its marginal model gain is small.

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
AM: Increasing local epochs E cuts rounds the most: E=1 takes 27 rounds, E=5 takes 6, and E=20 takes 2. The cost is more local compute, and under skew it can increase drift.

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
AM: The concept skew hurt the most; Kestrel paid because its FedAvg accuracy fell to 0.804 versus 0.828 local-only. A few rounds of local fine-tuning fixed it and brought Kestrel back to 0.828.

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
AM: Partial scores and residuals crossed the wire, but no raw feature columns. The residual leak exposed all labels, so the model should be jointly governed by both the hospital and the insurer.

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?
AM: FL keeps raw data at home, but the updates can still leak information or carry a poison signal. I would catch the boost attack from update norms alone, but not a simple label flip, because the flip attack stayed within the normal norm range.

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
AM: I would default to median because it cut backdoor success to 6% while keeping global accuracy at 0.817. I would require at least 3 hospitals per round because with only 2, the sum still leaks one hospital’s update. I would choose DP noise 0.3 for five hospitals because it kept accuracy at 0.814 while adding privacy.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
AM: I chose secure aggregation and added local clipping to 2.0 plus a minimum of 3 participants per round. One clause I would add is: no round may proceed with fewer than three hospitals, and all updates must be locally clipped before secure aggregation.

## Declaration
I ran these labs myself in my own Codespace. Aastha Malhotra
