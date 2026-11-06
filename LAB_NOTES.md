# BANA 690A Federated Learning I: Lab Notes

**Name:** Lori Balian
**GitHub username:** LoriBalian

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?
The coordinator holds the shared model, but never the raw data.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?
Kestrel benefits the most, with its accuracy increasing from 69.6% to 79.8%. Northgate only improves by 1 percent, so I would offer them a say in important decisions and help with costs to encourage them to join.

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
Increasing E reduces the number of rounds the most, from 27 to 2, but requires more training work.

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
Label skew hurt the most. Kestrel's accuracy dropped from 78.6% to 73.0%, but fine-tuning improved it to 79.2%.

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
The hospital and insurer shared scores and results, but not patient records. The insurer was still able to figure out 100% of the readmission labels. I think both organizations should share ownership of the model.

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?
FL keeps raw data at home, but patient information can still leak through model updates.
The boost and backdoor attacks could be caught because their updates were much larger than normal.

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
I would choose median because it reduced backdoor success from 57% to 6%. I would require at least 3 hospitals per round to help protect their individual updates. For 5 hospitals, I would choose noise 0.3 because accuracy stayed at 81.4% while adding privacy protection.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
I turned off secure aggregation and used trimmed mean to stop the attack. Accuracy improved from 52.48% to 79.32%. The downside is that the coordinator can now see individual updates, but keeping noise at 0.3 helps protect privacy. I would also require regular audits for extra protection.

## Declaration
I ran these labs myself in my own Codespace. Lori Balian
