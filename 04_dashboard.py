import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trader Chat Sentiment Analysis", layout="wide")

st.title("Trader Chat Sentiment & Issue Analysis")
st.markdown("Analyzing support chat messages classified via the Groq API (Llama 3.3) "
            "into issue categories and sentiment.")

# Load data
df = pd.read_csv("chat_messages_classified.csv")

# --- Sidebar filters ---
st.sidebar.header("Filters")
tier_options = ["All"] + sorted(df["account_tier"].dropna().unique().tolist())
selected_tier = st.sidebar.selectbox("Account Tier", tier_options)

platform_options = ["All"] + sorted(df["platform"].dropna().unique().tolist())
selected_platform = st.sidebar.selectbox("Platform", platform_options)

filtered_df = df.copy()
if selected_tier != "All":
    filtered_df = filtered_df[filtered_df["account_tier"] == selected_tier]
if selected_platform != "All":
    filtered_df = filtered_df[filtered_df["platform"] == selected_platform]

# --- Top-level metrics ---
col1, col2, col3 = st.columns(3)
total_msgs = len(filtered_df)
negative_pct = (filtered_df["sentiment"] == "Negative").mean() * 100 if total_msgs > 0 else 0
top_issue = filtered_df["issue_category"].value_counts().idxmax() if total_msgs > 0 else "N/A"

col1.metric("Total Messages", total_msgs)
col2.metric("% Negative", f"{negative_pct:.1f}%")
col3.metric("Top Issue Category", top_issue)

st.divider()

# --- Charts ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Negative Messages by Issue Category")
    neg_df = filtered_df[filtered_df["sentiment"] == "Negative"]
    if len(neg_df) > 0:
        counts = neg_df["issue_category"].value_counts().reset_index()
        counts.columns = ["issue_category", "count"]
        fig1 = px.bar(counts, x="count", y="issue_category", orientation="h",
                      color_discrete_sequence=["#c0392b"])
        fig1.update_layout(yaxis_title="", xaxis_title="Number of Negative Messages")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No negative messages in this selection.")

with c2:
    st.subheader("Negative Sentiment Rate by Account Tier")
    tier_sent = pd.crosstab(df["account_tier"], df["sentiment"])
    if "Negative" in tier_sent.columns:
        tier_sent["total"] = tier_sent.sum(axis=1)
        tier_sent["negative_rate"] = (tier_sent["Negative"] / tier_sent["total"] * 100).round(1)
        tier_sent = tier_sent[tier_sent.index != "Unknown"].reset_index()
        fig2 = px.bar(tier_sent, x="account_tier", y="negative_rate",
                      text="negative_rate", color_discrete_sequence=["#e67e22"])
        fig2.update_traces(texttemplate="%{text}%", textposition="outside")
        fig2.update_layout(yaxis_title="% Negative", xaxis_title="", yaxis_range=[0, 100])
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Sentiment breakdown table ---
st.subheader("Full Breakdown: Issue Category x Sentiment")
breakdown = pd.crosstab(filtered_df["issue_category"], filtered_df["sentiment"])
st.dataframe(breakdown, use_container_width=True)

# --- Raw data explorer ---
with st.expander("View raw filtered messages"):
    st.dataframe(filtered_df[["message_text", "account_tier", "platform",
                                "issue_category", "sentiment"]], use_container_width=True)
