# Customer Analytics: Customer Lifetime Value for a Food-Delivery Chain

Team project for the **Customer Analytics** elective (MSc Business Analytics, RSM, 2026). The client is a Dutch franchise chain of delivery restaurants, referred to here as **Restaurant Chain X**. The chain is moving from a product-centric to a customer-centric business and wants to run targeted marketing campaigns as experiments.

**My role:** main code executor. I wrote and ran the Python pipeline (CLV models, segmentation, acquisition and retention analysis, figures). After each round of strategy feedback from the team, I adjusted the code and re-ran it.

## The question

Using a sample of the chain's order history, the team had to:

1. Segment customers by Customer Lifetime Value (CLV): who generates the most revenue, and who is most loyal?
2. Propose a customer **acquisition** strategy.
3. Propose a customer **retention** strategy.
4. Project the future health of the customer base.
5. Recommend how to build a culture of experimentation: which experiments, which hypotheses, which data.

## Data

Order-level records, September 2023 to February 2026:

| | |
|---|---|
| Orders | about 1.94M |
| Customers | 875,558 (after dropping zero-revenue orders) |
| Stores | 82 |
| Fields | order ID, timestamp, price incl. and excl. VAT, zip code, city, customer ID, store, ordering channel |

Channels: TakeAway (68% of orders), Website (28%), ConsumerApp, UberEats, and a small in-store intake module.

The data belongs to the client and is **not included** in this repository. Data quality issues I handled:
- City names are inconsistent (about 4,200 variants), so city is not used for segmentation.
- About 2.6% of zip codes are invalid.
- The VAT ratio varies around the expected 9%, so all revenue is based on the **ex-VAT price**.

## Method

1. **Historical CLV** (benchmark): total ex-VAT spend per customer. The mean is €90 and the median €52, so the distribution is heavily right-skewed.
2. **Predictive CLV (6-month horizon)** with the `lifetimes` package:
   - **BG/NBD** model for how many purchases a customer will still make, allowing for churn.
   - **Gamma-Gamma** model for expected order value (repeat buyers only).
   - Combined into a 6-month CLV per customer (mean €129, median €52).
3. **Segmentation:**
   - **One-timer:** exactly one order.
   - **Casual:** repeat buyer, below the top quartile of predicted CLV among repeaters.
   - **Star:** repeat buyer in the top quartile of predicted CLV among repeaters.
4. **Acquisition analysis:** Star rate and average predicted CLV by channel and by store.
5. **Retention analysis:** order cadence per segment, reachability through owned channels, and a Mann-Whitney U test between channels.

## Key findings

**Segments**

| Segment | Customers | Share | Avg 6-month CLV |
|---|---|---|---|
| One-timer | 549,274 | 62.7% | €52.94 |
| Casual | 244,713 | 27.9% | €113.91 |
| Star | 81,571 | 9.3% | €686.83 |

- Stars place about 6.7 repeat orders, against 2.1 for Casuals. Their order value is only slightly higher (€47 vs €40), so the difference is **how often they order**, not how much they spend.
- Stars reorder roughly every 98 days. Casuals take around 340 days. If Casuals ordered at the Star cadence, their repeat frequency would more than double.

**Acquisition**

- Website (10.7%) and TakeAway (9.4%) produce Stars at similar rates. TakeAway is the biggest source in absolute numbers.
- UberEats (0.5%) and the intake module (0.2%) produce almost no Stars. These are mostly one-off, platform-driven buyers.
- ConsumerApp customers have the highest *historical* CLV (€126), but their *predicted* CLV is lower than Website and TakeAway. The app works better as a retention tool for existing regulars than as an acquisition channel.
- The best stores by Star rate and predicted CLV are in **smaller regional towns** (for example Middelburg, Den Helder, Heerlen), not in the big cities.
- Website Stars are worth more than TakeAway Stars (about €710 vs €678 predicted CLV, p < 0.0001).

**Retention**

- 146,185 one-timers are reachable through owned channels (Website, app). The recommendation is a win-back message about 30 days after the first order, while the brand is still fresh.
- Because the chain cannot contact TakeAway and UberEats customers directly, the plan focuses on moving them onto owned channels.

## Repository contents

| File | Purpose |
|---|---|
| `RFM_model_v4.ipynb` | Data preparation, BG/NBD + Gamma-Gamma CLV model, segment assignment, figures |
| `Acquisition_v4.ipynb` | Segment mix by channel and store, channel quality, store-level acquisition efficiency |
| `Retention_v4.ipynb` | Segment profiles, inter-purchase gaps, owned-channel reachability, significance test |
| `generate_figures.py` | Regenerates all report figures into `figures/` |
| `figures/` | Output figures used in the report |
| `city_distribution.csv` | Orders per city |

## How to run

```bash
pip install -r requirements.txt
```

The notebooks expect two CSV files in this folder, which are not in the repository:
`group_assignment_2026.csv` (raw orders) and `lifetimes_summary_with_CLV.csv` (the output of `RFM_model_v4.ipynb`).

Run the notebooks in this order: `RFM_model_v4` → `Acquisition_v4` → `Retention_v4`. To rebuild only the figures:

```bash
python generate_figures.py
```

## Tools

Python, pandas, NumPy, `lifetimes` (BG/NBD, Gamma-Gamma), SciPy, matplotlib, Jupyter.
