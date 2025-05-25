import requests, openai, json, os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# News holen
res = requests.get("https://cryptopanic.com/api/v1/posts/?auth_token=DEIN_TOKEN&public=true")
headlines = [p["title"] for p in res.json()["results"][:5]]

# GPT bewerten lassen
results = []
for title in headlines:
    prompt = f"Wie ist die Marktstimmung bei dieser Krypto-News? Gib 'bullish', 'bearish' oder 'neutral'.\n\n\"{title}\""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )
    sentiment = response.choices[0].message.content.strip()
    results.append({ "title": title, "sentiment": sentiment })

with open("gpt_news_feed.json", "w") as f:
    json.dump(results, f, indent=2)
