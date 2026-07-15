# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 00:12:16 2026

@author: JR
"""

import pandas as pd

df = pd.read_csv("chat_messages_classified.csv")

print("=== 1. What's driving negative sentiment? ===")
negative_df = df[df["sentiment"] == "Negative"]
print(negative_df["issue_category"].value_counts())

print("\n=== 2. Overall sentiment breakdown per issue category ===")
print(pd.crosstab(df["issue_category"], df["sentiment"]))

print("\n=== 3. Issue category by account tier ===")
print(pd.crosstab(df["account_tier"], df["issue_category"]))

print("\n=== 4. Sentiment by account tier (are VIPs happier or angrier?) ===")
print(pd.crosstab(df["account_tier"], df["sentiment"]))

import pandas as pd
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: Negative sentiment count by issue category
negative_df = df[df["sentiment"] == "Negative"]
category_counts = negative_df["issue_category"].value_counts()

axes[0].barh(category_counts.index, category_counts.values, color="#c0392b")
axes[0].set_xlabel("Number of Negative Messages")
axes[0].set_title("What's Driving Negative Sentiment")
axes[0].invert_yaxis()  # highest at top

# Chart 2: Negative sentiment RATE by account tier (not just raw count)
tier_sentiment = pd.crosstab(df["account_tier"], df["sentiment"])
tier_sentiment["total"] = tier_sentiment.sum(axis=1)
tier_sentiment["negative_rate"] = (tier_sentiment["Negative"] / tier_sentiment["total"] * 100).round(1)

# Drop "Unknown" tier if it only has 1 row, not meaningful to compare
tier_sentiment_clean = tier_sentiment[tier_sentiment.index != "Unknown"]

axes[1].bar(tier_sentiment_clean.index, tier_sentiment_clean["negative_rate"], color="#e67e22")
axes[1].set_ylabel("% of Messages That Are Negative")
axes[1].set_title("Negative Sentiment Rate by Account Tier")
axes[1].set_ylim(0, 100)

# Add percentage labels on top of bars
for i, val in enumerate(tier_sentiment_clean["negative_rate"]):
    axes[1].text(i, val + 2, f"{val}%", ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("chat_analysis_charts.png", dpi=150)
plt.show()

print(tier_sentiment_clean)