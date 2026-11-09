# BANA 690A Federated Learning I: Lab Notes

**Name: Madison Metz**
**GitHub username: madisonmetz637**

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?
The coordinator holds a neutral, consented evaluation set.
The coordinator never holds a hospital's patients.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?
We can see Kestrel gains the most at 0.10 compared to Northgate at 0.01 and Three Rivers at -0.008. In order to offer Northgate to join, we would want to offer them to add to group rules and share the cost. 
## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
E (local epochs) cuts rounds the most with 27 rounds at E=1, 6 at E=5, and 2 at E=20 with all three hospitals. C barely matters (27, 28, 27 at E=1). The cost is more total computing with 27 → 30 → 40 local epochs. The savings also shrink when hospitals are different where with a  realistic skew and one hospital per round, E=20 needed 5 rounds instead of 2, because each round drifts toward one hospital’s patients.
## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
Label skew hurt the most. Kestrel paid since it dropped from 0.786 on its own to 0.730 in the federation, about 5.6 points. All three hospitals had the same kind of patients but different readmission rates (20%, 34%, 48%), and one shared model can’t fit all three, so the hospital with the unusual rate gets the bad fit. Fine-tuning fixed it. After 5 extra local epochs on its own data, Kestrel went up to 0.792, even better than going alone. Concept shift also hurt Kestrel (0.828 → 0.804) and fine-tuning brought it all the way back (0.828). Under quantity skew nobody paid: tiny Kestrel gained about 4 points (0.730 → 0.772), but with 60 patients it only gets about 2% of the vote.
## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
Only partial scores and residuals crossed the wire, 108,000 numbers in total, and zero actual patient features (age, labs, claims). The hospital alone got 0.806, and vertical FL got 0.834, the same as the forbidden pooled table. So it got the full benefit without sharing a single column. But it leaked anyway: the insurer recovered 100% of the readmission labels, because a negative residual means the patient was readmitted. I think the model should be jointly owned, since neither side could have built it alone. The agreement should bar the insurer from using it to set premiums or deny coverage, and the residuals should be encrypted so the labels can’t be read.
## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?
FL keeps raw data at home, but the updates that leave every round are made from patient data and can be reversed. In my run the coordinator rebuilt one Kestrel patient exactly from a single-patient update (error 1.11e-16), though mixing 8 patients made it garbage. It also trusts every member’s update blindly: one hospital boosting its update by 10 dropped the model to 0.506.
Looking only at update norms, I would have caught the boost (norm 10.37) and the backdoor (8.12), because honest hospitals were between 0.23 and 1.79. I would not have caught the label flips (1.04 and 1.79), because they look normal in size. Northgate’s flip still dropped accuracy to 0.727, because it has 35% of the vote.
## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.
I would make default aggregator the charter default, because it brought the boost attack back to 0.814 and cut backdoor success from 57% to 6% (clip only got it to 28%), while costing nothing with no attack (0.814).
Minimum participants per round was 5, because with only 2 the secure-aggregation sum gives away the other hospital’s update, and DP cost dropped from about 12 points at 3 hospitals to about 3 at 5.
A noise multiplier for five hospitals of 0.5, because accuracy was 0.806 vs 0.814 with no noise, less than 1 point, while still adding real protection.
## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?
I chose robust aggregation: secure_aggregation false, trimmed_mean, and reject updates with a norm above 6.0 (charter v1.1). With secure aggregation on, the boost attack from Three Rivers crashed the model to 0.525 and it was only caught at the final gate (BLOCKED), because the coordinator couldn't see the bad update. With my edits, the same attack PASSED at 0.793, with Three Rivers rejected every round. Trying both at once (secure aggregation true + trimmed_mean) was STOPPED at the pre-check, because the coordinator can't inspect updates it can't see.
I gave up privacy from the coordinator. It can now see every hospital's individual update, and Lab 5 showed a one-patient update can be reversed exactly (error 1e-16).
Compensating control of DP noise of 0.3 stays on, updates must be built from at least 8 patients so none can be reversed, and members can audit the round log.
I would add, "The coordinator must be a neutral party, not a member hospital, rotating annually, and every member has the right to audit the round log and the model card."
## Declaration
I ran these labs myself in my own Codespace. (type your name)
Madison Metz