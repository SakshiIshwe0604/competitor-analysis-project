import pandas as pd
from send_slack_alert import send_alert

SENTIMENT_FILE = "outputs/sentiment_llama_output.csv"

def send_llama_sentiment_alert():
    print("📥 Loading LLaMA sentiment results...")
    df = pd.read_csv(SENTIMENT_FILE)

    # Count sentiment distribution
    positive = len(df[df["llama_sentiment"] == "positive"])
    negative = len(df[df["llama_sentiment"] == "negative"])
    total = positive + negative

    # Calculate percentages
    positive_pct = round((positive / total) * 100, 2)
    negative_pct = round((negative / total) * 100, 2)

    # Create message
    message = (
        "🧠 *LLaMA Sentiment Update*\n"
        f"👍 Positive: {positive} reviews ({positive_pct}%)\n"
        f"👎 Negative: {negative} reviews ({negative_pct}%)\n"
    )

    # Trigger alerts if sentiment is concerning
    if negative_pct > 60:
       message += "\n🔥 *Strong Alert:* High customer negativity detected! Competitor product may be failing."
    elif negative_pct > 40:
       message += "\n⚠️ *Warning:* Negativity is rising. Monitor competitor sentiment closely."
    elif negative_pct > 25:
       message += "\nℹ️ *Notice:* Mixed sentiment. Keep an eye on future trends."
    else:
       message += "\n✅ Sentiment looks stable. No major concerns."


    # Send to Slack
    send_alert(message)
    print("📨 Sentiment alert sent to Slack successfully!")

if __name__ == "__main__":
    send_llama_sentiment_alert()
