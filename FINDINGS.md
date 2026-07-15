# Chat Sentiment & Issue Analysis

## Approach
Classified 49 trader chat messages using the Groq API (Llama 3.3) into a fixed set of issue
categories and a sentiment label (Positive/Neutral/Negative), then cross-tabulated results
against account tier and platform to identify priority issues and any tier-based differences.

## Finding 1: Technical/Execution Issues and Platform/App Bugs drive most negative sentiment
- Together account for 20 of 34 negative messages (59%)
- Technical/Execution Issue is the more consistently negative of the two — zero neutral or
  positive mentions, versus Platform/App Bugs which had some positive mentions too

## Finding 2: Premium and VIP customers report negative sentiment at a higher rate than Standard
- Premium: 81.2% negative | VIP: 77.8% negative | Standard: 56.5% negative
- Issue mix is similar across tiers, so this isn't about different problems — higher-tier
  customers appear to have higher expectations, making the same issues feel worse to them

## Recommendations
1. Prioritize Technical/Execution Issue fixes first — most consistently negative, no upside
2. Treat Premium/VIP sentiment as an urgent retention risk — these are the highest-value
   customers reporting the most dissatisfaction relative to their peers

## Caveats
- Sample size per tier is small (9-23 messages), so percentages should be treated as
  directional rather than statistically definitive
- AI-based classification is more flexible than keyword matching but not deterministic-
  re-running the same messages could occasionally produce slightly different category picks
