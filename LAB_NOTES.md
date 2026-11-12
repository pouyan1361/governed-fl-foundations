# BANA 690A Federated Learning I: Lab Notes

**Name:** Farha Nadine
**GitHub username:** nadifn01

One to three sentences per prompt, in your own words, with a number from your
own run where the prompt asks for one. Commit this file to your fork by the
end of class (see README, "Turning in your notes").

## Lab 0: The world
What does the coordinator hold, and what does it never hold?

The coordinator holds just the shared global model and a de-identified evaluation set (1,500 rows: 500 per hospital), never raw patient data, protecting privacy.

## Lab 1: FedAvg from scratch
Which hospital gains most from federating, by how much (your numbers), and what would you offer Northgate to join?

Kestrel benefits most from federating, with a 10.2 percentage point increase (0.696 to 0.798), while Northgate gains just 0.010 (0.810 to 0.820). I’d offer Northgate a steering committee seat, a rotating coordinator role, access to broader rural data, cost-sharing, and regulatory goodwill.

## Lab 2: McMahan's knobs
From the grid: which knob cuts communication rounds the most, and what do you pay for it?
Increasing local epochs (E) reduces communication rounds—from 27 (E=1) to just 2 (E=20) with full hospital participation—but increases total local computation (27 to 40 epochs, or up to 100 under skewed, partial participation) and raises the risk of client drift when hospitals differ.

## Lab 3: Heterogeneity
Which skew hurt the most, which hospital paid, and what fixed it?

Label skew hurt Kestrel the most, lowering its accuracy by 5.6 points because one global threshold doesn’t fit different hospital rates. Concept shift also dropped Kestrel’s score by 2.4 points. Local fine-tuning fixed both issues, restoring Kestrel’s performance.

## Lab 4: Vertical federation
What crossed the wire, what leaked anyway, and who should own the resulting model?

108,000 partial scores and residuals were shared, revealing all hospital readmission labels to the insurer and summarizing claims data back to the hospital, even though no raw data was sent. Both organizations should jointly govern the model, require encryption, and restrict its use solely to patient care—not insurance pricing.

## Lab 5: Threats
Finish the sentence: "FL keeps raw data at home, but ..." Then: which attack would you have caught from update norms alone, and which not?

Federated learning (FL) keeps raw data local, but model updates can still leak patient info and let dishonest hospitals attack the shared model. Checking update norms easily catches large attacks like boost (10.37) and backdoor (8.123), but misses label flipping, which looks normal (1.037 and 1.789).

## Lab 6: Defenses
Which aggregator would you make the charter default, what minimum number of participants per round, and what noise multiplier for a five-hospital consortium? One sentence of justification each.

Trimmed mean or median is the best default because they stop attacks and keep results accurate. Each round should include at least 3–5 hospitals to protect privacy and remove outliers. With 5 hospitals, a noise multiplier of 0.3 offers strong privacy without hurting accuracy. These steps make the system safer and fair for everyone involved.

## Lab 7: FL as a governance control
The charter had to choose between secure aggregation and robust aggregation. Which did you choose, what compensating control did you add, and what one clause would you add to the consortium agreement?

By allowing the coordinator to check updates using trimmed mean and rejecting anything above 6.0, Three Rivers’ bad update was blocked and accuracy jumped from 0.5248 to 0.7932. Privacy was protected by adding noise (0.3) and switching the coordinator every year. Each hospital can fine-tune locally, and routine audits make sure everything is fair and accurate.

## Declaration
I ran these labs myself in my own Codespace. (type your name)
Farha Nadine
