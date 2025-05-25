import requests
import openai
import json

# 🔑 Deine API-Keys einfügen:
CRYPTO_PANIC_TOKEN = "8a9f804d7fabb5b6845f51a88ba2579d55b5ea78"
OPENAI_API_KEY = "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"

# API-URLs
CRYPTO_PANIC_API = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_TOKEN}&public=true"

# GPT-Modell
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-3.5-turbo"

def fetch_crypto_news(limit=5):
    """Holt die letzten Crypto-News von CryptoPanic"""
    try:
        res = requests.get(CRYPTO_PANIC_API)
        res.raise_for_status()
        data = res.json()
        headlines = [item["title"] for item in data["results"][:limit]]
        return headlines
    except Exception as e:
        print("Fehler beim Abrufen der News:", e)
        return []

def ask_gpt_about_sentiment(headlines):
    """Sendet News-Titel an GPT und erhält eine Marktstimmungsanalyse"""
    prompt = "Gib eine Marktstimmung (bullish, neutral oder bearish) basierend auf folgenden Krypto-News:\n\n"
    prompt += "\n".join([f"- {title}" for title in headlines])
    prompt += "\n\nAntwort bitte im Format: 'Sentiment: bullish' und eine kurze Begründung."

    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Fehler bei GPT-Abfrage:", e)
        return "Sentiment: unknown"

def save_result(headlines, gpt_output):
    """Speichert das Ergebnis als JSON-Datei"""
    result = {
        "sentiment_raw": gpt_output,
        "titles": headlines
    }
    with open("news_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Ergebnis gespeichert in 'news_result.json'.")

def main():
    headlines = fetch_crypto_news()
    if not headlines:
        print("Keine Headlines erhalten.")
        return
    gpt_output = ask_gpt_about_sentiment(headlines)
    save_result(headlines, gpt_output)

if __name__ == "__main__":
    main()
