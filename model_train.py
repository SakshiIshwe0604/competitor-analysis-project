import pandas as pd
import numpy as np
import os
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import joblib

# -------------------------------
# Paths
# -------------------------------
DATA_FILE = "data/processed/samsung_s24_engineered_price_data.csv"
BEST_PARAM_FILE = "models/best_sarima_params.txt"
MODEL_OUTPUT = "models/sarima_s24_model.pkl"
FORECAST_OUTPUT = "outputs/s24_forecast.csv"
PLOT_OUTPUT = "outputs/s24_forecast_plot.png"

os.makedirs("outputs", exist_ok=True)


# -------------------------------
# Read Best Parameters
# -------------------------------
def load_best_params():
    params = {}
    with open(BEST_PARAM_FILE, "r") as f:
        for line in f.readlines()[1:]:
            key, value = line.strip().split(": ")
            params[key] = int(value)
    return params


# -------------------------------
# Train the Model
# -------------------------------
def train_model():
    print("📥 Loading engineered dataset...")
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    # Only use price column for SARIMA
    prices = df["price"]

    # Train-test split (80/20)
    train_size = int(len(prices) * 0.8)
    train = prices[:train_size]
    test = prices[train_size:]

    print("⚙ Loading best parameters...")
    params = load_best_params()

    p, d, q = params["p"], params["d"], params["q"]
    P, D, Q, s = params["P"], params["D"], params["Q"], params["s"]

    print(f"🔧 Training SARIMA({p},{d},{q}) x ({P},{D},{Q},{s})")

    model = SARIMAX(
        train,
        order=(p, d, q),
        seasonal_order=(P, D, Q, s),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    model_fit = model.fit(disp=False)
    print("✅ Model training complete!")

    # Save model
    joblib.dump(model_fit, MODEL_OUTPUT)
    print(f"💾 Model saved to {MODEL_OUTPUT}")

    # Forecast on test set
    forecast = model_fit.forecast(steps=len(test))

    rmse = np.sqrt(np.mean((forecast - test) ** 2))
    print(f"📉 RMSE: {rmse:.2f}")

    # Forecast next 30 days
    future_forecast = model_fit.forecast(steps=30)

    forecast_df = pd.DataFrame({
        "date": pd.date_range(start=df["date"].iloc[-1], periods=30, freq="D"),
        "forecast_price": future_forecast
    })

    forecast_df.to_csv(FORECAST_OUTPUT, index=False)
    print(f"📄 Forecast saved to: {FORECAST_OUTPUT}")

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"][:train_size], train, label="Train")
    plt.plot(df["date"][train_size:], test, label="Test")
    plt.plot(forecast_df["date"], forecast_df["forecast_price"], label="Forecast (Next 30 Days)")
    plt.legend()
    plt.title("Samsung S24 Price Forecasting")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(PLOT_OUTPUT)
    print(f"📊 Plot saved to {PLOT_OUTPUT}")

    print("\n🎉 Forecasting Completed Successfully!")


if __name__ == "__main__":
    train_model()
