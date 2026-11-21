# BANA 690A Federated Learning I: Lab Notes

**Name: Dougem Yamral**
**GitHub username: dougemyamral909-svg**

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
The coordinator holds 500 de-identified rows from each hospital's population. The coordinator never holds any hospital training records and the coordinator never sees a hospital's patients.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?

Kestrel gains the most from federating, with its accuracy increasing from 69.6% to 79.8%, which is a gain of 10.2 percentage points. To encourage Northgate to join, I would offer it a say in the consortium’s rules and shared costs, since its accuracy only improved by 1 percentage point

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?

From the grid, the E knob cuts communication rounds and costs more computation. For example increasing E from 1 to 20 reduced communication rounds from 27 to 2, but increased total local training from 27 to 40 epochs

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?

Label skew hurt the most because the hospitals had different readmission rates. Kestrel’s accuracy dropped from 78.6% alone to 73.0% with FedAvg, but local fine-tuning fixed the loss since it was raised to 79.2%

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?

Partial scores and residuals crossed the wire. The readmission labels were leaked to the insurer. I think Northgate and Sierra should both share ownership since they both contributed to the model

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?

FL keeps raw data at home, but model updates can still reveal patient information since the single-patient update allowed almost exact reconstruction. I would have caught the boost and backdoor attacks because their update norms were 10.37 and 8.123 which isabove the no-attack range of 0.228–1.789. I would have not caught label flipping because its update norms stayed within that range.

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.

I would choose median as a defualt aggregator because it restored accuracy to 81.4% under the boost attack and reduced backdoor sucess from 57% to 6%. I would require at least 3 participants per round because only having 2, could lead to where one can subtract its own update from the sum and recover the other’s update. I would choose a noise multiplier of 0.3 for five hospitals because it adds privacy noise while keeping accuracy at 81.4% which is the same as the no-noise result.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?

I chose robust aggregation using trimmed mean because accuracy under attack improved from 52.48% to 79.32%. My compensating control was DP noise at 0.3, which remained on after turning off secure aggregation. I would add a clause giving consortium members the right to audit the coordinator and review the round log.




## Declaration
I ran these labs myself in my own Codespace. (Dougem Yamral)
