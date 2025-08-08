from textblob import TextBlob
import random
import json

def analyze_mood(text):
    blob = TextBlob(text);
    polarity = blob.sentiment.polarity;
    if polarity > 0.2:
        mood = "Positive";
    elif polarity < -0.2:
        mood= " Negative";
    else:
        mood = "Neutral"
    
    return mood, polarity;

def get_motivation(mood):
    try:
        with open("assets/mood_motivations.json", encoding="utf-8") as f:
            data = json.load(f)
        return random.choice(data.get(mood.lower(), ["Keep going!!"]))
    except Exception:
        return "You're doing your best. Keep it up!"
            