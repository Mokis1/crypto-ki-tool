import json
from datetime import datetime

whales = [
    { "coin": "BTC", "amount": 1500, "to": "Binance" },
    { "coin": "ETH", "amount": 23000, "to": "Unknown wallet" },
    { "coin": "USDT", "amount": 50000000, "to": "Kraken" }
]

with open("whale_data.json", "w") as f:
    json.dump(whales, f, indent=2)
