import pandas as pd
from send_slack_alert import send_alert

FORECAST_FILE = "outputs/s24_forecast.csv"

def send_price_alert():
    df = pd.read_csv(FORECAST_FILE)

    # Extract last 2 predictions (most recent change)
    last_two = df.tail(2)

    prev_price = last_two.iloc[0]["forecast_price"]
    new_price = last_two.iloc[1]["forecast_price"]


    # Determine direction
    if new_price > prev_price:
        msg = (
            f"📈 *Price Increase Alert!*\n"
            f"Competitor forecast price increased from {prev_price:.2f} → {new_price:.2f}"
        )
    elif new_price < prev_price:
        msg = (
            f"📉 *Price Drop Alert!*\n"
            f"Competitor forecast price dropped from {prev_price:.2f} → {new_price:.2f}"
        )
    else:
        msg = (
            f"➖ *Price Stable*\n"
            f"Competitor forecast price remains unchanged at {new_price:.2f}"
        )

    send_alert(msg)
    print("📨 Price alert sent to Slack.")

if __name__ == "__main__":
    send_price_alert()
