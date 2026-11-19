"""
Figure generation script — Restaurant Chain X CLV Analysis
Exports all requested figures to: ./figures/

Figures produced:
  Figure 1  — Frequency distribution histogram
  Figure 2  — Historical revenue per customer distribution
  Figure 3  — Historical customer lifetime distribution
  Figure 4  — Predicted 6-month CLV distribution
  Figure 5  — Mean CLV by channel (barplot)
  Figure 6A — Mean CLV: top 10 stores (barplot)
  Figure 6B — Mean CLV: bottom 10 stores (barplot)
  Figure R1 — Revenue per order distribution: Stars vs Casuals (owned channels)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Output folder ─────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "figures")
os.makedirs(OUTDIR, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size":      11,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "figure.dpi":     150,
})

BLUE   = "#2C7BB6"
RED    = "#D7191C"
ORANGE = "#FDAE61"
GREY   = "#AAAAAA"

def save(name):
    path = os.path.join(OUTDIR, name)
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"  Saved: {name}")

# ══════════════════════════════════════════════════════════════════════════════
# Load data
# ══════════════════════════════════════════════════════════════════════════════
print("Loading data...")

clv_df = pd.read_csv(os.path.join(BASE, "lifetimes_summary_with_CLV.csv"))

# Historical CLV table (recomputed from raw data)
raw = pd.read_csv(os.path.join(BASE, "group_assignment_2026.csv"))
raw["DeliveryTimestamp"] = pd.to_datetime(raw["DeliveryTimestamp"], utc=True, errors="coerce")
raw = raw[raw["PriceExcVat"] > 0]

hist = (
    raw.groupby("CustomerID")
    .agg(
        first_purchase=("DeliveryTimestamp", "min"),
        last_purchase =("DeliveryTimestamp", "max"),
        total_orders  =("OrderID", "nunique"),
        revenue       =("PriceExcVat", "sum"),
        avg_order_val =("PriceExcVat", "mean"),
    )
    .reset_index()
)
hist["lifetime_days"] = (hist["last_purchase"] - hist["first_purchase"]).dt.days

# Segment assignment (mirrors Retention.ipynb)
repeaters  = clv_df[clv_df["frequency"] > 0]
clv_75th   = repeaters["CLV_6m"].quantile(0.75)

def assign_segment(row):
    if row["frequency"] == 0:
        return "One-timer"
    elif row["CLV_6m"] >= clv_75th:
        return "Star"
    else:
        return "Casual"

clv_df["segment"] = clv_df.apply(assign_segment, axis=1)

print(f"  Raw rows: {len(raw):,} | Customers: {len(hist):,}")
print(f"  CLV rows: {len(clv_df):,} | CLV 75th pct (repeaters): €{clv_75th:.2f}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Frequency distribution histogram
# Capped at 10+ to keep readable; % labels on bars
# ══════════════════════════════════════════════════════════════════════════════
print("Figure 1: Frequency distribution...")

CAP = 10
freq = clv_df["frequency"].copy()
freq_capped = freq.clip(upper=CAP)

counts = freq_capped.value_counts().sort_index()
total  = len(freq)

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(
    [str(int(x)) if x < CAP else f"{CAP}+" for x in counts.index],
    counts.values,
    color=BLUE, edgecolor="white", linewidth=0.5, width=0.7
)

# Percentage labels on each bar
for bar, cnt in zip(bars, counts.values):
    pct = cnt / total * 100
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + total * 0.003,
        f"{pct:.1f}%",
        ha="center", va="bottom", fontsize=8.5, color="#333333"
    )

ax.set_xlabel("Number of repeat purchases (frequency)")
ax.set_ylabel("Number of customers")
ax.set_title("Figure 1: Distribution of Customer Purchase Frequency")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_ylim(0, counts.max() * 1.12)

fig.tight_layout()
save("figure_1_frequency_distribution.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Historical revenue per customer distribution
# ══════════════════════════════════════════════════════════════════════════════
print("Figure 2: Historical revenue distribution...")

rev = hist["revenue"]
cap = rev.quantile(0.99)   # trim extreme tail for readability
mean_rev = rev.mean()

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(rev[rev <= cap], bins=60, color=BLUE, edgecolor="white", linewidth=0.3)
ax.axvline(mean_rev, color=RED, linewidth=1.8, linestyle="--",
           label=f"Mean: €{mean_rev:.0f}")
ax.set_xlabel("Historical revenue per customer (€ excl. VAT)")
ax.set_ylabel("Number of customers")
ax.set_title("Figure 2: Distribution of Historical Revenue per Customer\n(top 1% trimmed for readability)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x):,}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(frameon=False)
fig.tight_layout()
save("figure_2_historical_revenue.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Historical customer lifetime distribution
# ══════════════════════════════════════════════════════════════════════════════
print("Figure 3: Historical lifetime distribution...")

lt = hist["lifetime_days"]
mean_lt = lt.mean()

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(lt, bins=60, color=BLUE, edgecolor="white", linewidth=0.3)
ax.axvline(mean_lt, color=RED, linewidth=1.8, linestyle="--",
           label=f"Mean: {mean_lt:.0f} days")
ax.set_xlabel("Customer lifetime (days from first to last purchase)")
ax.set_ylabel("Number of customers")
ax.set_title("Figure 3: Distribution of Historical Customer Lifetime")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(frameon=False)
fig.tight_layout()
save("figure_3_historical_lifetime.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Predicted 6-month CLV distribution
# ══════════════════════════════════════════════════════════════════════════════
print("Figure 4: Predicted CLV distribution...")

clv = clv_df["CLV_6m"]
cap = clv.quantile(0.99)
mean_clv = clv.mean()

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(clv[clv <= cap], bins=60, color=BLUE, edgecolor="white", linewidth=0.3)
ax.axvline(mean_clv, color=RED, linewidth=1.8, linestyle="--",
           label=f"Mean: €{mean_clv:.0f}")
ax.set_xlabel("Predicted 6-month CLV per customer (€)")
ax.set_ylabel("Number of customers")
ax.set_title("Figure 4: Distribution of Predicted 6-Month CLV\n(top 1% trimmed for readability)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x):,}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(frameon=False)
fig.tight_layout()
save("figure_4_predicted_clv.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Mean CLV by channel (horizontal barplot)
# ══════════════════════════════════════════════════════════════════════════════
print("Figure 5: Mean CLV by channel...")

ch = (
    clv_df.groupby("Channel")["CLV_6m"]
    .mean()
    .sort_values()
    .reset_index()
)
ch.columns = ["Channel", "Mean_CLV"]

colors = [BLUE if c not in ("S4D - Cash register",) else GREY for c in ch["Channel"]]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(ch["Channel"], ch["Mean_CLV"], color=colors, edgecolor="white", height=0.6)

for bar, val in zip(bars, ch["Mean_CLV"]):
    ax.text(val + 2, bar.get_y() + bar.get_height() / 2,
            f"€{val:.0f}", va="center", fontsize=10)

ax.set_xlabel("Mean predicted 6-month CLV (€)")
ax.set_title("Figure 5: Mean Predicted CLV by Ordering Channel")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x)}"))
ax.set_xlim(0, ch["Mean_CLV"].max() * 1.18)
fig.tight_layout()
save("figure_5_clv_by_channel.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6A & 6B — Mean CLV: top 10 and bottom 10 stores
# ══════════════════════════════════════════════════════════════════════════════
print("Figure 6: Top/bottom 10 stores by mean CLV...")

store_clv = (
    clv_df.groupby("StoreName")["CLV_6m"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
store_clv["StoreName_short"] = store_clv["StoreName"].str.replace(
    "Spare Rib Express ", "", regex=False
)

top10    = store_clv.head(10).sort_values("CLV_6m")
bottom10 = store_clv.tail(10).sort_values("CLV_6m", ascending=False).sort_values("CLV_6m")

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

for ax, data, title, color in [
    (axes[0], top10,    "Figure 6A: Top 10 Stores by Mean CLV",    BLUE),
    (axes[1], bottom10, "Figure 6B: Bottom 10 Stores by Mean CLV", ORANGE),
]:
    bars = ax.barh(data["StoreName_short"], data["CLV_6m"],
                   color=color, edgecolor="white", height=0.65)
    for bar, val in zip(bars, data["CLV_6m"]):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
                f"€{val:.0f}", va="center", fontsize=9)
    ax.set_xlabel("Mean predicted 6-month CLV (€)")
    ax.set_title(title, pad=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x)}"))
    ax.set_xlim(0, data["CLV_6m"].max() * 1.22)

fig.suptitle("Mean Predicted CLV: Top 10 vs Bottom 10 Stores", fontsize=13, fontweight="bold", y=1.01)
fig.tight_layout()
save("figure_6_clv_top_bottom_stores.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE R1 — Revenue per order distribution: Stars vs Casuals (owned channels)
# Two overlaid/side-by-side histograms
# ══════════════════════════════════════════════════════════════════════════════
print("Figure R1: Star vs Casual revenue per order (owned channels)...")

owned   = ["Website", "ConsumerApp"]
stars   = clv_df[(clv_df["segment"] == "Star")   & (clv_df["Channel"].isin(owned)) & (clv_df["monetary_value"] > 0)]
casuals = clv_df[(clv_df["segment"] == "Casual") & (clv_df["Channel"].isin(owned)) & (clv_df["monetary_value"] > 0)]

cap = max(stars["monetary_value"].quantile(0.99), casuals["monetary_value"].quantile(0.99))
bins = np.linspace(0, cap, 55)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)

for ax, data, label, color in [
    (axes[0], stars,   f"Stars (n={len(stars):,})",   BLUE),
    (axes[1], casuals, f"Casuals (n={len(casuals):,})", ORANGE),
]:
    mv = data["monetary_value"].clip(upper=cap)
    mean_mv = data["monetary_value"].mean()

    ax.hist(mv, bins=bins, color=color, edgecolor="white", linewidth=0.3, alpha=0.85)
    ax.axvline(mean_mv, color=RED, linewidth=1.8, linestyle="--",
               label=f"Mean: €{mean_mv:.0f}")
    ax.set_xlabel("Avg revenue per order (€)")
    ax.set_ylabel("Number of customers")
    ax.set_title(label)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x)}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(frameon=False)

fig.suptitle("Figure R1: Revenue per Order — Stars vs Casuals (Owned Channels)",
             fontsize=13, fontweight="bold")
fig.tight_layout()
save("figure_R1_star_casual_order_value.png")

print()
print(f"All figures saved to: {OUTDIR}")
print(f"  {len(os.listdir(OUTDIR))} files total")
