# BANA 690A Federated Learning I: Lab Notes

**Name:Kelly A.**
**GitHub username:kellyaltamira892**

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold? The coordinator holds the consented evalutaion set, the coordinator never sees a hosipitals patients.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join? Kestrel gains the most at 10 points. 

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
Increasing local epochs reduced communication rounds the most. Increasing E from 1 to 20 reduced communication rounds from approximately 27 to 2, but increased total local computation from 27 to 40 epochs.

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?
Label skew caused the largest accuracy decrease for Kestrel Hospital, from 0.786 with local training to 0.730 with FedAvg. Personalization through five additional local training epochs improved its accuracy to 0.792.

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?
Although no raw feature values were shared, the insurer could recover 100% of patient readmission labels from the residual signs. The resulting model should have joint governance between the hospital and insurer.

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not? FL keeps raw data at home, can still expose patient information and may allow participants to manipulate the model. Monitoring update norms can detect the boosted model poisoning attack because its norm was approximately 10.37, compared with 0.2–1.8. Update norms alone would not detect membership inference attacks because these involve extracting information.

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each. I would choose coordinate-wise median as the default aggregator. I would require at least three hospitals per round to limit individual influence and support proper aggregation. For five-hospital, I would choose a differential privacy noise multiplier of 0.5 because it provides additional privacy protection.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement? After modifying the federation policy to prioritize robust aggregation, the model passed all governance checks with a global accuracy of 0.7932, Kestrel accuracy of 0.75, and a hospital accuracy gap of 0.082. However, when I changed secure aggregation back to true, the charter pre-check stopped the run because secure aggregation hides individual hospital updates. This demonstrates that privacy and robustness controls can conflict, requiring the consortium to choose compatible controls before deployment.

## Declaration
I ran these labs myself in my own Codespace. (Kelly A.)
