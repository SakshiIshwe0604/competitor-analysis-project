# scrapers.py
# Flipkart scraper with undetected-chromedriver (bypasses bot detection)

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime

RAW_CSV = "data/raw/competitor_prices.csv"

def init_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=options)
    return driver

def fetch_page_source(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(5)  # allow JS + anti-bot bypass
    html = driver.page_source
    driver.quit()
    return html

def scrape_single_product(url, platform="Flipkart"):
    print(f"Scraping using stealth mode: {url}")

    driver = init_driver()
    driver.get(url)
    time.sleep(5)

    # Product Name selectors
    name_selectors = [
        ".B_NuCI",
        "span.VU-ZEz",
        "span.DcDWDd",
        "h1"
    ]

    product_name = "Unknown Product"
    for sel in name_selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, sel)
            product_name = element.text.strip()
            break
        except:
            continue

    # Price selectors
    price_selectors = [
        "._30jeq3",
        ".Nx9bqj",
        "div.CxhGGd"
    ]

    price = None
    for sel in price_selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, sel)
            price = ''.join(ch for ch in element.text if ch.isdigit())
            break
        except:
            continue

    promo = 1 if "offer" in driver.page_source.lower() else 0

    driver.quit()

    # Save row
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "platform": platform,
        "product_name": product_name,
        "price": price,
        "currency": "INR",
        "promo_tag": promo,
        "url": url
    }

    with open(RAW_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(row)

    print("Scraped & Saved:", row)
