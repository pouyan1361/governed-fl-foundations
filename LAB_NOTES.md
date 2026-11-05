# BANA 690A Federated Learning I: Lab Notes

**Name:Riley Phipps**
**GitHub username:rileyphipps23**

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?
The coordinator holds a neutral test set that is consented for using 500 rows of both hospitals population. It never holds the training records of the hospital.  

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?
Kestrel gains the most from federating by 0.102. Because it only gains this much, I would offer Northgate to join the improved shared model, reduced costs, and a part in deciding how to manage the model.

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
The knob that cuts communication rounds the most is E. What we pay for it is more local computation as well as a greater risk of client drift when hospital data is different, which can happen when one hospital decides not to participate.

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
What hurt the most was label skew. Kestrel hospital paid the most which caused it's accuracy to fall from , 0.786 to 0.730. What fixed it was local fine-tuning which raised it's accuracy to 0.792.

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
What crossed the wire was partial scores and residuals between the hospital and the insurer. The patient labels were recovered by the insurer while the hospital learned information regarding the claims data. The resulting model should be managed by both organization. 

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?
FL keeps raw data at home, but harmful updates that poison the model can still be sent by a untrustworthy hospital. The attack that i would have caught from update norms alone is backdoor attacks and boost attacks due to the large updates while the small Three rivers flip attack would be missed. 


## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
The aggregator that I would make the charter default is the trimmed mean because it keeps a strong accuracy while combating boost and backdoor attacks.
The minimum number of participants per round is 3 because any less could mix with another hospital's aggregate. 
The noise multiplier for a five-hospital consortium is 0.3 because this will keep the same accuracy as no noise while adding more privacy.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
Between the two, I chose robust aggregation, specifically trimmed mean, because it kept accuracy high while protecting the model from backdoor attacks and boost attacks. The compensating control that I added was clipping as well as a 0.3 difference privacy noise multiplier. One clause I would add to the consortium agreement would be that atleast three hostpitals much participate in order for training rounds to begin.

## Declaration
I ran these labs myself in my own Codespace. Riley Phipps
