import pandas as pd
from textblob import TextBlob
import os

REVIEWS_FILE = "amazon_s24_full_reviews.csv"
OUTPUT_FILE = "outputs/sentiment_analysis_output.csv"

os.makedirs("outputs", exist_ok=True)

def perform_sentiment_analysis():
    print("📥 Loading review data...")
    df = pd.read_csv(REVIEWS_FILE)

    # Clean column names
    df.columns = [c.strip().lower() for c in df.columns]

    if "review" not in df.columns:
        raise ValueError("CSV must contain a 'review' column.")

    print("🔍 Running sentiment analysis...")
    df["polarity"] = df["review"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df["sentiment"] = df["polarity"].apply(
        lambda p: "positive" if p > 0 else ("negative" if p < 0 else "neutral")
    )

    summary = df["sentiment"].value_counts(normalize=True) * 100

    print("\n📊 Sentiment Distribution:")
    print(summary)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n💾 Sentiment results saved to: {OUTPUT_FILE}")

    return summary


if __name__ == "__main__":
    perform_sentiment_analysis()
