# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 00:05:40 2026

@author: JR
"""

import pandas as pd
import os
import json
import time
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

df = pd.read_csv("chat_messages_cleaned.csv")

ISSUE_CATEGORIES = [
    "Technical/Execution Issue",
    "Withdrawal/KYC Issue",
    "Customer Support Quality",
    "Fees/Pricing",
    "Platform/App Bugs",
    "Positive Experience",
    "Other"
]

def classify_message(message_text):
    prompt = f"""Analyze this trader's message and return TWO things:
1. An issue category — pick exactly ONE from this list: {', '.join(ISSUE_CATEGORIES)}
2. A sentiment — exactly one of: Positive, Neutral, Negative

Message: "{message_text}"

Respond with ONLY valid JSON in this exact format, nothing else, no explanation:
{{"issue_category": "the category", "sentiment": "the sentiment"}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    reply_text = response.choices[0].message.content

    try:
        parsed = json.loads(reply_text)
        return parsed["issue_category"], parsed["sentiment"]
    except (json.JSONDecodeError, KeyError):
        return "Other", "Neutral"

categories = []
sentiments = []

for i, row in df.iterrows():
    category, sentiment = classify_message(row["message_text"])
    categories.append(category)
    sentiments.append(sentiment)
    print(f"Row {i}: {category} | {sentiment}")
    time.sleep(0.3)  # small pause to stay well within free-tier rate limits

df["issue_category"] = categories
df["sentiment"] = sentiments

df.to_csv("chat_messages_classified.csv", index=False)
print("\nDone. Saved to chat_messages_classified.csv")