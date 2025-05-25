# gpt_coin_sentiment.py
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

coins = ["BTC", "ETH", "SOL", "XRP"]
prompts = {
    "BTC": "Gib eine kurze Marktanalyse zu Bitcoin (BTC) basierend auf aktuellen Entwicklungen. Ist die Stimmung bullish, neutral oder bearish?",
    "ETH": "Gib eine kurze Marktanalyse zu Ethereum (ETH) basierend auf aktuellen Entwicklungen. Ist die Stimmung bullish, neutral oder bearish?",
    "SOL": "Gib eine kurze Marktanalyse zu Solana (SOL) basierend auf aktuellen Entwicklungen. Ist die Stimmung bullish, neutral oder bearish?",
    "XRP": "Gib eine kurze Marktanalyse zu XRP basierend auf aktuellen Entwicklungen. Ist die Stimmung bullish, neutral oder bearish?"
}

results = {}
for coin in coins:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompts[coin]}
            ]
        )
        text = response["choices"][0]["message"]["content"].strip()
        results[coin] = {"gpt": text}
    except Exception as e:
        results[coin] = {"gpt": f"Fehler bei GPT: {str(e)}"}

with open("coin_sentiment.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("✅ coin_sentiment.json aktualisiert")

