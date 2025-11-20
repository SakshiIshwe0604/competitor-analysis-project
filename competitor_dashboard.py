import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Competitor Analysis Dashboard", layout="wide")

st.title("📊 Competitor Analysis Dashboard")
st.write("Real-time insights for price trends, sentiment, and alerts.")

# ---- Load Data ----
forecast_file = "outputs/s24_forecast.csv"
sentiment_file = "outputs/sentiment_llama_output.csv"
engineered_file = "data/processed/samsung_s24_engineered_price_data.csv"

# Load datasets safely
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return None

forecast_df = load_data(forecast_file)
sentiment_df = load_data(sentiment_file)
engineered_df = load_data(engineered_file)

# ---- Tabs ----
tab1, tab2, tab3 = st.tabs(["📈 Price Forecast", "🧠 Sentiment Analysis", "📂 Engineered Data"])

# ---- Price Forecast Tab ----
with tab1:
    st.header("📈 Price Forecast Trend")

    if forecast_df is not None:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(forecast_df["date"], forecast_df["forecast_price"], marker='o')
        ax.set_title("Forecasted Competitor Prices")
        ax.set_xlabel("Date")
        ax.set_ylabel("Forecast Price (INR)")
        st.pyplot(fig)

        st.subheader("Latest Forecast Values")
        st.write(forecast_df.tail())
    else:
        st.warning("Forecast file not found.")

# ---- Sentiment Analysis Tab ----
with tab2:
    st.header("🧠 LLaMA Sentiment Analysis Results")

    if sentiment_df is not None:
        sentiment_count = sentiment_df["llama_sentiment"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=sentiment_count.index, y=sentiment_count.values, ax=ax)
        ax.set_title("Sentiment Distribution")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.write("### Detailed Sentiment Data")
        st.dataframe(sentiment_df)
    else:
        st.warning("Sentiment file not found.")

# ---- Engineered Data Tab ----
with tab3:
    st.header("📂 Engineered Price Dataset (Features)")

    if engineered_df is not None:
        st.dataframe(engineered_df)
    else:
        st.warning("Engineered file not found.")
