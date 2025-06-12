import requests
from config import API_KEY, CRYPTO_URLS

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