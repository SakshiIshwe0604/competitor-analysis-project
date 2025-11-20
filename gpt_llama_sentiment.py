from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

# FREE LLaMA-style sentiment model
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

print("📥 Loading LLaMA-style sentiment model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

labels = ["negative", "positive"]

def llama_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    return labels[torch.argmax(probs)]

def run_llama_sentiment_analysis():
    print("📥 Loading review dataset...")
    df = pd.read_csv("amazon_s24_full_reviews.csv")

    # FIX: Use the correct column name
    if "Review" not in df.columns:
        raise ValueError("CSV must have a 'Review' column.")

    print("🤖 Running LLaMA-style sentiment classification...")
    df["llama_sentiment"] = df["Review"].apply(llama_sentiment)

    output_path = "outputs/sentiment_llama_output.csv"
    df.to_csv(output_path, index=False)

    print("✅ Sentiment analysis completed!")
    print(f"💾 Saved to {output_path}")
    print("\n📊 Sentiment summary:\n")
    print(df["llama_sentiment"].value_counts())

if __name__ == "__main__":
    run_llama_sentiment_analysis()
