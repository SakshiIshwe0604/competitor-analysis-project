import pandas as pd
import numpy as np
import optuna
import warnings
import os
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")

DATA_FILE = "data/processed/samsung_s24_engineered_price_data.csv"
OUTPUT_DIR = "models/"
BEST_PARAM_FILE = os.path.join(OUTPUT_DIR, "best_sarima_params.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

def sarima_objective(trial, data):
    p = trial.suggest_int("p", 0, 3)
    d = trial.suggest_int("d", 0, 1)
    q = trial.suggest_int("q", 0, 3)

    P = trial.suggest_int("P", 0, 2)
    D = trial.suggest_int("D", 0, 1)
    Q = trial.suggest_int("Q", 0, 2)
    s = trial.suggest_categorical("s", [7, 12, 30])

    train_size = int(len(data) * 0.8)
    train = data["price"][:train_size]
    test = data["price"][train_size:]

    try:
        model = SARIMAX(
            train,
            order=(p, d, q),
            seasonal_order=(P, D, Q, s),
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        model_fit = model.fit(disp=False)
        forecast = model_fit.forecast(steps=len(test))
        rmse = np.sqrt(np.mean((forecast - test) ** 2))
        return rmse
    except:
        return np.inf

def run_tuning():
    print("Loading data...")
    df = load_data()

    print("Running SARIMA Hyperparameter Tuning...")
    study = optuna.create_study(direction="minimize")
    study.optimize(lambda trial: sarima_objective(trial, df), n_trials=20)

    print("\nBest Parameters Found:")
    print(study.best_params)

    with open(BEST_PARAM_FILE, "w") as f:
        f.write("Best SARIMA Parameters:\n")
        for key, value in study.best_params.items():
            f.write(f"{key}: {value}\n")

    print(f"\nSaved best parameters to: {BEST_PARAM_FILE}")

if __name__ == "__main__":
    run_tuning()
