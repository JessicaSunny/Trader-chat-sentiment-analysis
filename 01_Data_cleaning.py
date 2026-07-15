# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 00:00:13 2026

@author: JR
"""

import pandas as pd

df = pd.read_csv("chat_messages.csv")

print("Before cleaning:")
print(df.isnull().sum())

# message_text: can't impute what a trader actually said — drop rows with no text
df = df.dropna(subset=["message_text"])

# account_tier: categorical, fill with explicit "Unknown" rather than guessing a tier
df["account_tier"] = df["account_tier"].fillna("Unknown")

# platform: same logic — categorical, fill with explicit "Unknown"
df["platform"] = df["platform"].fillna("Unknown")

print("\nAfter cleaning:")
print(df.isnull().sum())
print("\nFinal shape:", df.shape)

df.to_csv("chat_messages_cleaned.csv", index=False)