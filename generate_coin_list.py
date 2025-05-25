import requests, json

coins = []
page = 1

while page <= 3:  # 3 Seiten x 100 = bis zu 300 Coins
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&page={page}&per_page=100"
    resp = requests.get(url).json()
    coins += resp
    page += 1

result = [
    {
        "name": c["name"],
        "symbol": c["symbol"].upper(),
        "price": round(c["current_price"], 4),
        "market_cap": c["market_cap"]
    }
    for c in coins
]

with open("all_coins.json", "w") as f:
    json.dump(result, f, indent=2)
