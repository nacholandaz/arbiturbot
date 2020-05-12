# Interacts with whatsapp api to send messages
import requests
import os

LUIS_AI_ID= os.getenv('LUIS_AI_ID')
LUIS_AI_KEY = os.getenv('LUIS_AI_KEY')


def query(text):
    params = f"verbose=true&timezoneOffset=0&subscription-key={LUIS_AI_KEY}&q={text}"
    url = f"https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/{LUIS_AI_ID}?{params}"
    print(url)
    r = requests.get(url).json()
    max_score = r['intents'][0]['score']
    max_intent = r['intents'][0]['intent'] if max_score > 0.7 else None
    response = {'intent': max_intent, 'sentiment': r['sentimentAnalysis']['label']}
    print(response)
    return response

def get_label(text):
    intent = query(text)['intent']
    if intent in ['sale', 'support']: return intent
    return None
