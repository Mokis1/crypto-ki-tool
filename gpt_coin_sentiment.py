import requests
import json
from openai import OpenAI

OPENAI_API_KEY = "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"
GPT_MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key=OPENAI_API_KEY)

COINS = ["bitcoin", "ethereum", "solana", "xrp", "dogecoin"]
VS_CURRENCY = "usd"

def get_news_for_coin(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/status_updates"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        titles = [entry["description"] for entry in data.get("status_updates", [])[:3]]
        return titles
    except Exception as e:
        return [f"No news found for {coin}"]

def analyze_coin_with_gpt(coin, titles):
    prompt = (
        f"Analyze the following news headlines about {coin.upper()} and provide a sentiment "
        f"(bullish, neutral, or bearish) with a short explanation:\n\n"
        + "\n".join([f"- {t}" for t in titles])
    )

    try:
        res = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return "Sentiment: unknown – GPT error."

def main():
    result = {}
    for coin in COINS:
        titles = get_news_for_coin(coin)
        sentiment = analyze_coin_with_gpt(coin, titles)
        result[coin.upper()] = {
            "news": titles,
            "gpt": sentiment
        }

    with open("coin_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ Datei coin_sentiment.json wurde erstellt.")

if __name__ == "__main__":
    main()
