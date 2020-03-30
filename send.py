# Interacts with whatsapp api to send messages
import requests
import time
import os

CHAT_TOKEN = os.environ['CHAT_TOKEN']

def natural_reply_time(reply_text):
    #http://www.iphonehacks.com/2010/03/iphone-user-types-incredible-83-wpm-attributes-speed-to-capacitive-touch-screen.html
    #return time.sleep(len(reply_text.split(' ')))
    return 1

def mark_as_read_and_wait(reply_text, message):
    user_id = message['user_id']
    meta_chat = {
        'read': True,
        'chatId': user_id
    }
    requests.post(f'https://api.chat-api.com/instance99459/sendMessage?token={CHAT_TOKEN}', data=meta_chat).json()
    # Read, then wait proportionally to writing time
    natural_reply_time(reply_text)
    return True

def reply(reply_text, message):
    mark_as_read_and_wait(reply_text, message)
    print('Sending message:' + reply_text)
    user_id = message['user_id']
    meta_chat = {
        'body': reply_text,
        'chatId': user_id
    }
    requests.post(f'https://api.chat-api.com/instance99459/sendMessage?token={CHAT_TOKEN}', data=meta_chat).json()
    return True

def set_webhook(webhook_url):
    meta_chat = {
        "set": True,
        "webhookUrl": "http://d53eb69b.ngrok.io/messages"
    }
    return requests.post(f'https://api.chat-api.com/instance99459/webhook?token={CHAT_TOKEN}', data=meta_chat).json()
