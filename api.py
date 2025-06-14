import requests
import time
from config import CRYPTO_URLS, COINCAP_SYMBOLS
from secrets import API_KEY

def fetch_crypto_data(index):
    url = CRYPTO_URLS[index]
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()["data"]
        price = float(data["priceUsd"])
        change = float(data["changePercent24Hr"])
        price_str = f"${price:.2f}"
        while len(price_str) < 10:
            price_str = f"${price:.{2 + (10 - len(price_str))}f}"
        change_str = f"{change:.2f}"
        return price_str, change_str
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "N/A", "N/A"

def get_historical_prices(index, interval):
    symbol = COINCAP_SYMBOLS[index]
    now_ms = int(time.time() * 1000)
    if interval == "1d":
        start_ms = now_ms - 24 * 60 * 60 * 1000
        points = 24
        interval_param = "h1"
    elif interval == "7d":
        start_ms = now_ms - 7 * 24 * 60 * 60 * 1000
        points = 7
        interval_param = "d1"
    elif interval == "30d":
        start_ms = now_ms - 30 * 24 * 60 * 60 * 1000
        points = 30
        interval_param = "d1"
    else:
        start_ms = now_ms - 7 * 24 * 60 * 60 * 1000
        points = 7
        interval_param = "d1"

    url = f"https://rest.coincap.io/v3/assets/{symbol}/history?interval={interval_param}&start={start_ms}&end={now_ms}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()
        prices = [float(point["priceUsd"]) for point in data["data"]]
        if len(prices) > points:
            step = len(prices) / points
            sampled = []
            for i in range(points):
                idx = int(i * step)
                sampled.append(prices[idx])
            return sampled
        elif len(prices) > 0:
            while len(prices) < points:
                prices.append(prices[-1])
            return prices
        else:
            return [1] * points
    except Exception as e:
        print(f"Error fetching historical data from CoinCap: {e}")
        return [1] * points