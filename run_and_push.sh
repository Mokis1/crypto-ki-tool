#!/bin/bash

cd "$(dirname "$0")"  # Wechsle in den Ordner, in dem das Skript liegt

echo "🚀 Starte GPT-Newsanalyse..."
python gpt_news_live.py

echo "📤 Git-Push starten..."
git add news_result.json
git commit -m "auto: update GPT-News $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "✅ Alles erledigt!"
