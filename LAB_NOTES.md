# BANA 690A Federated Learning I: Lab Notes

**Name: Manchi Hsu
**GitHub username: ManchiHsu

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?
The coordeinator holds a neutral, consented, de-identified evaluation set of 1500 records, but never holds any hospital's training records

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?
Kestrel gains the most from federating, with accuracy increasing from 0.696 to 0.798, a gain of 0.102 (10.2 percentage points). Northgate only gains 0.010, so I would offer it a role in consortium decision-making, shared costs, and access to a model trained on more diverse patient populations.
## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
Increasing local epochs (E) reduces communication rounds the most. With realistic skew and C=1.0, increasing E from 1 to 20 reduces rounds from 16 to 1, but more local computation may be required. When C=0.34, increasing E from 5 to 20 does not reduce rounds and increases total local epochs from 25 to 100.
## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
Label skew caused the most harm, especially to Kestrel, where accuracy dropped from 0.786 (local-only) to 0.730 (FedAvg), a loss of 0.056. Local fine-tuning improved Kestrel's accuracy to 0.792, showing that personalization can help hospitals with different patient populations.
## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
In vertical FL, 108,000 intermediate numbers (partial scores and residuals) crossed the wire, but no raw feature values were shared. However, the insurer could recover 100% of the patient labels from the residuals. I would recommend joint governance and shared control of the resulting model between the hospital and insurer, with clear privacy and usage restrictions.
## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?
FL keeps raw data at home, but model updates can still leak patient information and be manipulated by malicious hospitals. Update norms could detect the boost (10.37) and backdoor (8.123) attacks, but not the label-flipping attacks because their norms remained within the normal range. A single-patient gradient allowed nearly exact reconstruction, while batching and secure aggregation prevented that simple reconstruction attack.
## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
I would choose median aggregation as the default because it reduced backdoor success from 57% to 6% while maintaining good accuracy. I would require at least three hospitals per round to reduce the risk of revealing individual updates. For a five-hospital consortium, I would choose a noise multiplier of 0.3 because it maintained an accuracy of 0.814 while adding privacy protection.
## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
 I chose robust aggregation using trimmed mean instead of secure aggregation, which improved accuracy from 0.5248 to 0.7932 under the boost attack. I kept differential privacy with a noise multiplier of 0.3 as a compensating control. I would add a clause requiring hospitals to follow update validation rules, with regular audits and coordinator rotation to protect privacy.
## Declaration
I ran these labs myself in my own Codespace. (Manchi Hsu)
