import pandas as pd
import numpy as np
import os

RAW_FILE = "data/raw/samsung_galaxy_s24_price_history.csv"
OUTPUT_DIR = "data/processed/"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "samsung_s24_engineered_price_data.csv")

def load_data():
    df = pd.read_csv(RAW_FILE)

    # Ensure proper column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Check required columns
    if "date" not in df.columns or "price" not in df.columns:
        raise ValueError("CSV must contain 'date' and 'price' columns.")

    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)
    return df

def add_date_features(df):
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["day_of_week"] = df["date"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    return df

def add_lag_features(df):
    for lag in [1, 2, 3, 7, 14, 30]:
        df[f"lag_{lag}"] = df["price"].shift(lag)
    return df

def add_rolling_features(df):
    df["rolling_7_mean"]  = df["price"].rolling(window=7).mean()
    df["rolling_14_mean"] = df["price"].rolling(window=14).mean()
    df["rolling_30_mean"] = df["price"].rolling(window=30).mean()

    df["rolling_7_std"]  = df["price"].rolling(window=7).std()
    df["rolling_14_std"] = df["price"].rolling(window=14).std()

    return df

def add_difference_features(df):
    df["diff_1"] = df["price"].diff(1)
    df["diff_7"] = df["price"].diff(7)
    return df

def clean_data(df):
    # Fill NaN using forward fill for early dates
    df = df.fillna(method="ffill")
    df = df.fillna(method="bfill")
    return df

def save_output(df):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n🎉 Feature engineering complete!")
    print(f"📁 Saved engineered file to: {OUTPUT_FILE}")

def run_feature_engineering():
    print("🔄 Loading raw price data...")
    df = load_data()

    print("📅 Adding date-based features...")
    df = add_date_features(df)

    print("📈 Adding lag features...")
    df = add_lag_features(df)

    print("📊 Adding rolling statistics...")
    df = add_rolling_features(df)

    print("🔁 Adding difference features...")
    df = add_difference_features(df)

    print("🧼 Cleaning final dataset...")
    df = clean_data(df)

    print("💾 Saving final engineered dataset...")
    save_output(df)

if __name__ == "__main__":
    run_feature_engineering()
