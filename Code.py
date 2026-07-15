# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:32:49 2026

@author: JR
"""

import pandas as pd

df = pd.read_csv("feedback.csv")

print("Before cleaning:")
print(df.isnull().sum())

# comment_text: can't impute or guess what someone said —
# a missing comment has no analytical value, so we drop those rows
df = df.dropna(subset=["comment_text"])

# channel: categorical, so fill with an explicit "unknown" label
# rather than guessing a specific channel — keeps it visible as its own category
df["channel"] = df["channel"].fillna("unknown")

# rating: ordinal (1-5), so median is safer than mean if any are missing
# (only applies if rating actually has missing values — check first)
if df["rating"].isnull().sum() > 0:
    median_rating = df["rating"].median()
    df["rating"] = df["rating"].fillna(median_rating)

print("\nAfter cleaning:")
print(df.isnull().sum())
print("\nFinal shape:", df.shape)

df.to_csv("feedback_cleaned.csv", index=False)


import pandas as pd

df = pd.read_csv("feedback_cleaned.csv")

# Define themes as keyword groups - based on skimming the comments first
# This is a judgment call: choose keywords that actually reflect language in YOUR data
theme_keywords = {
    "App Performance/Bugs": ["crash", "slow", "lag", "freeze", "buggy", "bug"],
    "Withdrawal/Deposit Issues": ["withdrawal", "deposit", "fee", "fees"],
    "Customer Support": ["support", "response", "wait", "reply", "service"],
    "Verification/Onboarding": ["verification", "verify", "onboarding"],
    "Positive Experience": ["great", "excellent", "love", "easy", "smooth", "impressed", "happy"],
}

def assign_theme(comment):
    comment_lower = str(comment).lower()
    matched_themes = []
    for theme, keywords in theme_keywords.items():
        if any(kw in comment_lower for kw in keywords):
            matched_themes.append(theme)
    return matched_themes if matched_themes else ["Other/Unclassified"]

df["themes"] = df["comment_text"].apply(assign_theme)

# Explode so each theme gets its own row for counting
# (a comment can belong to more than one theme)
exploded = df.explode("themes")

print("=== Theme frequency ===")
print(exploded["themes"].value_counts())

print("\n=== Average rating per theme ===")
print(exploded.groupby("themes")["rating"].mean().round(2).sort_values())

print("\n=== Theme by channel ===")
print(pd.crosstab(exploded["themes"], exploded["channel"]))

exploded.to_csv("feedback_with_themes.csv", index=False)