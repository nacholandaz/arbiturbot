import requests
import json
from textblob import TextBlob
from googletrans import Translator
import os
translator = Translator()

def get(input_text):
    url_gpt = os.environ['URL_GPT']
    content = {"context":input_text,"model_size":"gpt","top_p":0.9,"temperature":1,"max_time":1}
    return requests.post(url_gpt, data=json.dumps(content)).json()['sentences'][0]['value']

def answer(text_input):
    if text_input[-1] != '?': text_input + '?\n'
    original_language = TextBlob(text_input).detect_language()
    if  original_language != 'en':
        text_input = translator.translate(text_input, dest='en').text
    gpt_response = get(text_input).strip()
    if original_language == 'en': return gpt_response
    return translator.translate(gpt_response, dest=original_language).text
