# competitor_engine/fetch_price_history.py

import requests
import pandas as pd
from datetime import datetime

API_URL = "https://django.prixhistory.com/api/product/history/updateFromSlug"
HEADERS = {
    "auth": "rlPC4RU1BE2DJoIhAQVR56gtHzPMbcIaw42TuoC+1N4qMApS9+qlP8WOA/6oN/ou",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Origin": "https://pricehistoryapp.com",
    "Referer": "https://pricehistoryapp.com/",
}

def fetch_price_history(slug, output_csv):
    """Fetch and save price history for a competitor product."""
    
    payload = {"slug": slug}
    
    res = requests.post(API_URL, headers=HEADERS, data=payload)

    if res.status_code != 200:
        print("Error:", res.status_code)
        return None
    
    data = res.json()
    
    if "history" not in data:
        print("No history found.")
        return None
    
    hist = data["history"]

    if isinstance(hist, dict):
        hist = [{"date": k, "price": v} for k, v in hist.items()]

    df = pd.DataFrame(hist)
    
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df = df.sort_values("date")
    
    df.to_csv(output_csv, index=False)
    
    print(f"Saved: {output_csv}")
    return df
