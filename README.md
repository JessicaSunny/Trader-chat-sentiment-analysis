# Trader Chat Sentiment & Issue Analysis

Analyzes customer support chat messages from traders to identify what's driving negative
sentiment, quantify issue frequency and severity, and compare experience across account tiers.

Live Dashboard: https://trader-chat-sentiment-analysis-mrkdqrzon55jztq3nekjep.streamlit.app/

## Approach
1. **Data cleaning** — handled missing values per column type (dropped rows with missing
   message text, filled missing categorical fields with "Unknown")
2. **AI classification** — used the Groq API (Llama 3.3) to classify each message into a
   fixed issue category and sentiment label, using structured JSON prompting
3. **Analysis** — cross-tabulated issue category against sentiment and account tier to
   identify priority issues and tier-based differences in reported experience

## Key Findings
- **Technical/Execution Issues** and **Platform/App Bugs** together drive 59% of all
  negative feedback
- **Premium (81.2%) and VIP (77.8%) customers report negative sentiment at a notably
  higher rate than Standard customers (56.5%)**, despite reporting a similar mix of issues —
  suggesting higher expectations amplify the same problems for higher-value customers

Full write-up in [FINDINGS.md](FINDINGS.md).

## Files
| File | Description |
|---|---|
| `01_Data_cleaning.py` | Loads raw data, handles missing values per column type |
| `02_AI_classification.py` | Calls the Groq API to classify each message (issue category + sentiment) |
| `03_Analysis_and_charts.py` | Quantifies findings and generates charts |
| `chat_messages.csv` | Raw input data |
| `chat_messages_cleaned.csv` | After missing-value treatment |
| `chat_messages_classified.csv` | Final output with AI-assigned category and sentiment |
| `chat_analysis_charts.png` | Summary visualizations |
| `FINDINGS.md` | Full findings and recommendations |

## Tech stack
Python, pandas, Groq API (Llama 3.3), matplotlib

## Note
`chat_messages.csv` is synthetic data generated for practice purposes.
