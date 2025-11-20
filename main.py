import os
import subprocess
from datetime import datetime

def run_step(title, command):
    print(f"\n🚀 {title}...")
    result = subprocess.run(["python3"] + command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Errors/Warnings:\n", result.stderr)
    print(f"✅ {title} completed.\n")

def main():
    print("\n==============================")
    print("🧠 COMPETITOR ANALYSIS PIPELINE")
    print("==============================\n")
    print(f"⏰ Run Time: {datetime.now()}\n")

    # 1️⃣ Feature Engineering
    run_step("Running Feature Engineering",
             ["feature_engineering.py"])

    # 2️⃣ Hyperparameter Tuning
    run_step("Running Hyperparameter Tuning (SARIMA)",
             ["hyper_tune.py"])

    # 3️⃣ Model Training & Forecasting
    run_step("Training Forecast Model & Generating Forecast",
             ["model_train.py"])

    # 4️⃣ Send Price Alert
    run_step("Sending Price Alert to Slack",
             ["price_alerts.py"])

    # 5️⃣ Sentiment Analysis using LLaMA
    run_step("Running LLaMA Sentiment Analysis",
             ["gpt_llama_sentiment.py"])

    # 6️⃣ Send Sentiment Alert
    run_step("Sending Sentiment Alert to Slack",
             ["sentiment_llama_alerts.py"])

    print("\n🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
    print("Your competitor analysis system is fully updated.\n")

if __name__ == "__main__":
    main()
