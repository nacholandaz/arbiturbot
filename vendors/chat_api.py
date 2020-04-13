# Interacts with whatsapp api to send messages
import requests
import time
import os
import conversation
import user
import cli

CHAT_TOKEN = os.getenv('CHAT_TOKEN')


def natural_reply_time(reply_text):
    #http://www.iphonehacks.com/2010/03/iphone-user-types-incredible-83-wpm-attributes-speed-to-capacitive-touch-screen.html
    return time.sleep(int(float(len(reply_text.split(' ')))//10.0))

def mark_as_read_and_wait(reply_text, message):
    user_id = message['user_id']
    meta_chat = {
        'read': True,
        'chatId': user_id
    }
    requests.post(f'https://eu87.chat-api.com/instance99459/sendMessage?token={CHAT_TOKEN}', data=meta_chat).json()
    # Read, then wait proportionally to writing time
    natural_reply_time(reply_text)
    return True

def reply(reply_text, message):
    mark_as_read_and_wait(reply_text, message)
    user_id = message['user_id']
    meta_chat = {
        'body': reply_text,
        'chatId': user_id
    }
    if cli.is_on() == False:
        print(f'Sending text {reply_text} to chat api...')
        r = requests.post(f'https://eu87.chat-api.com/instance99459/sendMessage?token={CHAT_TOKEN}', data=meta_chat).json()
    else:
        cli.puts_reply(meta_chat)
    if user.get(user_id):
        if conversation.find(user_id) is None: conversation.create_delegated(message)
        SENDER_ID = user.phone_to_id(os.getenv('ARBITRUR_PHONE'))
        conversation.update_canonical_conversation(SENDER_ID, user_id, reply_text, 'bot')
    return True

def set_webhook(webhook_url):
    meta_chat = {
        "set": True,
        "webhookUrl": "http://d53eb69b.ngrok.io/messages"
    }
    return requests.post(f'https://eu87.chat-api.com/instance99459/webhook?token={CHAT_TOKEN}', data=meta_chat).json()

def get_chats():
    return requests.get(f'https://eu87.chat-api.com/instance99459/chats?token={CHAT_TOKEN}').json()

def get_messages():
    return requests.get(f'https://eu87.chat-api.com/instance99459/messages?token={CHAT_TOKEN}').json()

def get_chat_user_name(user_id):
    try:
        name =  [chat for chat in get_messages()['messages'] if chat['chatId'] == user_id][0].get('senderName')
    except:
        name = ''
    return name
