# 📊 Competitor Analysis & Pricing Intelligence System

A complete end-to-end **Competitor Monitoring, Price Forecasting, Sentiment Analysis, and Slack Alerting System** built for the Infosys 6.0 Internship Milestone Project.

This project aggregates competitor pricing data, performs feature engineering, forecasts future prices using SARIMA, analyzes customer sentiment using LLaMA-based transformer models, and sends real-time Slack alerts for price and sentiment trends. A Streamlit dashboard provides visual insights.

---

# 🚀 **Project Overview**

This system performs the following automated tasks:

### ✔ **Web Scraping / Data Collection**

Collects product pricing and metadata from ecommerce sites (Flipkart, Amazon, etc.) using Selenium.

### ✔ **Data Processing & Feature Engineering**

Feature engineering on historical price data:

* Date features
* Lag features
* Rolling means
* Differencing features

### ✔ **Time Series Forecasting (SARIMA Model)**

Uses SARIMA to predict competitor future pricing.
Hyperparameters are optimized using Optuna.

### ✔ **Sentiment Analysis (LLaMA Transformer)**

Analyzes Amazon customer reviews using a free LLaMA-style model:

* positive
* negative

### ✔ **Slack Alert System**

Sends:

* 📈 Price Increase Alerts
* 📉 Price Drop Alerts
* 🧠 Sentiment Alerts

### ✔ **Streamlit Dashboard**

Interactive dashboard includes:

* Forecast charts
* Sentiment distribution
* Engineered feature table

---

# 📁 **Project Structure**

```
competitor_analysis_project/
│
├── competitor_engine/                 # Scrapers, utilities, fetchers
│
├── data/
│   ├── raw/                           # Raw scraped price data
│   └── processed/                     # Engineered datasets
│
├── models/
│   ├── sarima_s24_model.pkl          # Saved SARIMA model
│   └── best_sarima_params.txt        # Best parameters from Optuna
│
├── outputs/
│   ├── s24_forecast.csv              # Forecast results
│   ├── s24_forecast_plot.png         # Forecast chart
│   └── sentiment_llama_output.csv    # LLaMA sentiment results
│
├── feature_engineering.py
├── hyper_tune.py
├── model_train.py
├── gpt_llama_sentiment.py
├── sentiment_llama_alerts.py
├── price_alerts.py
├── send_slack_alert.py
├── competitor_dashboard.py
├── main.py                            # Full pipeline automation
└── README.md (this file)
```

---

# 🔧 **Setup Instructions**

## 1️⃣ Clone the project & enter folder

```
cd competitor_analysis_project
```

## 2️⃣ Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

(If no requirements.txt, install manually: Streamlit, pandas, numpy, statsmodels, transformers, torch, seaborn, matplotlib, optuna, requests, selenium.)

---

# ⚙️ **How to Run the Automated Pipeline**

The entire system runs with one command:

```
python3 main.py
```

This runs:

1. Feature Engineering
2. SARIMA Hyperparameter Tuning
3. SARIMA Model Training
4. Price Forecast Generation
5. Price Alert → Slack
6. LLaMA Sentiment Analysis
7. Sentiment Alert → Slack

---

# 📈 **Price Forecasting (SARIMA)**

SARIMA was used instead of Linear Regression or LightGBM because:

* It models seasonality
* Works with time dependency
* Detects trends
* Ideal for pricing applications

Output stored in:

```
outputs/s24_forecast.csv
```

---

# 🧠 **Sentiment Analysis (LLaMA Model)**

Uses a free LLaMA-style transformer model (DistilBERT SST-2) to classify reviews.
Outputs stored in:

```
outputs/sentiment_llama_output.csv
```

Example results:

```
positive: 6
negative: 4
```

---

# 🔔 **Slack Integration**

System sends:

* Price increase alerts
* Price drop alerts
* Mixed/negative sentiment alerts

Webhook URL stored inside:

```
send_slack_alert.py
```

Example alert:

```
📈 Price Increase Alert! Competitor forecast price increased from 43782 → 43973
```

---

# 🖥 **Dashboard (Streamlit)**

Launch using:

```
streamlit run competitor_dashboard.py
```

Dashboard sections:

* 📈 Price Forecast Chart
* 🧠 LLaMA Sentiment Distribution
* 📂 Engineered Features Table

---

# 📊 **Results Summary**

* SARIMA RMSE: ~2500
* LLaMA Sentiment: 60% positive, 40% negative
* Slack alerts triggered correctly
* Dashboard live and working
* Pipeline fully automated

# 🙌 **Author**

Sakshi Ishwe — Infosys Springboard Internship Project

If you need enhancements, improvements, or deployment steps, feel free to ask!
