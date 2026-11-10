# BANA 690A Federated Learning I: Lab Notes

**Name: Joseph Galvez**
**GitHub username: josephg753**

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?

Coordinator holds a neutral, consented evaluation set of 500 de-identified rows from each hospital's population. It never holds training records.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?

Kestrel gains the most from federating by +0.102 - Northgate can be offered Governance/a board seat to overview what happens with the data and how it gets used in future models.
This could extend to Northgate also being given monetary value if they are not seeking governance.

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?

E cuts communication rounds the most but the computations for it take more time due to how long it takes to train
It creates a risk because if the hospitals are taking longer to train, the shared model will tilt towards the hospitals that reported back before training started

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?

The label skew hurt the most as it had very different readmission rates, Kestrel had the most unusually high readmission rate which dropped its accuracy (FedAvg)
Fine-tuning the shared model on each hospital's own data fixed it which brought Kestrel's accuracy back up

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?

What crossed the wire was 108,000 partial scores/residuals and what leaked is the residuals showed each patients readmission label to the insurer. The scores gave the hospital a weighted summary,
the owner of the model should be both parties involved. 

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?

FL keeps raw data at home, but the updates can still leak information about patietns and can be poisoned by a dishonest hospital. It's important to note that each hospital needs to be honest.
Boost and backdoor would have been caught right away since the numbers are so much higher but flip might have passed through the cracks. 

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.

1. Median would be the agreggator as it has the lowest backdoor success at 6%
2. Minimum number of participants should be 3 to outvote a dishonest hospital (like Three Rivers)
3. For 5 hospitals, 0.5 noise multipler shows the best results because it keeps accuracy high and is the most noise we can add before it drops significantly


## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?

Secure aggregation is the better way to go based on the output from the run_federation.py file. The charter is meant to protect members from a coordinator who has access to too much information and instead will deny their request. The compensating control is max_norm at 2.0, dp_noise at 0.3, and the gate which will block deployment after training. The clause I would add is to make each hospital run their own official software without changes and allow for access to the committee/coordinator to review to prevent dishonest participants.


## Declaration
I ran these labs myself in my own Codespace. (Joseph Galvez)
