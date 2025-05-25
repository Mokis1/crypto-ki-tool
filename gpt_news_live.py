import requests
import json
from openai import OpenAI

# 🔑 Trage hier deine echten API-Keys ein
CRYPTO_PANIC_TOKEN = "8a9f804d7fabb5b6845f51a88ba2579d55b5ea78"
OPENAI_API_KEY = "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"
GPT_MODEL = "gpt-3.5-turbo"

# API-URL für CryptoPanic
CRYPTO_PANIC_API = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_TOKEN}&public=true"

# GPT-Client
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_crypto_news(limit=5):
    """Holt die neuesten Crypto-News-Titel von CryptoPanic"""
    try:
        response = requests.get(CRYPTO_PANIC_API)
        response.raise_for_status()
        data = response.json()
        titles = [item["title"] for item in data["results"][:limit]]
        return titles
    except Exception as e:
        print("❌ Fehler beim Abrufen der News:", e)
        return []

def ask_gpt_about_sentiment(titles):
    """Fragt GPT nach einer Gesamt-Stimmung basierend auf den News"""
    prompt = "Analysiere die folgende Liste von Krypto-News-Schlagzeilen. Gib ein Gesamt-Sentiment zurück: bullish, neutral oder bearish. Füge eine kurze Begründung hinzu.\n\n"
    prompt += "\n".join([f"- {title}" for title in titles])
    prompt += "\n\nAntwort im Format: 'Sentiment: ...' + Begründung."

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Fehler bei GPT-Abfrage:", e)
        return "Sentiment: unknown"

def save_result(titles, gpt_output):
    """Speichert die Analyse lokal als JSON-Datei"""
    result = {
        "sentiment_raw": gpt_output,
        "titles": titles
    }
    with open("news_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("✅ news_result.json wurde gespeichert.")

def main():
    titles = fetch_crypto_news()
    if not titles:
        print("⚠️ Keine Titel erhalten. Abbruch.")
        return
    sentiment = ask_gpt_about_sentiment(titles)
    save_result(titles, sentiment)

if __name__ == "__main__":
    main()
