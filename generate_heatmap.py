import requests
import json

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False
}

resp = requests.get(url, params=params)
data = resp.json()

heatmap = {coin["symbol"].upper(): round(coin["price_change_percentage_24h"] or 0, 2) for coin in data}

with open("heatmap_data.json", "w") as f:
    json.dump(heatmap, f, indent=2)
