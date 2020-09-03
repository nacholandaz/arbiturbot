# Interacts with whatsapp api to send messages
import requests
import time
import os
import conversation
import user
import cli
import log_handler

CHAT_TOKEN = os.getenv('CHAT_TOKEN')
CHAT_URL = os.getenv('CHAT_URL')


def try_send(url, meta_chat):
    total_tries = 5
    tries = 0
    sent = 0
    r = None
    for i in range(0, total_tries):
        try:
            r = requests.post(url, data=meta_chat).json()
            return r
        except:
            time.sleep(0.5)
    if sent == 0: print('We could not send the message to server...')
    return r

def natural_reply_time(reply_text):
    #http://www.iphonehacks.com/2010/03/iphone-user-types-incredible-83-wpm-attributes-speed-to-capacitive-touch-screen.html
    return time.sleep(int(float(len(reply_text.split(' ')))//10.0))

def mark_as_read_and_wait(reply_text, message):
    user_id = message['user_id']
    meta_chat = {
        'read': True,
        'chatId': user_id
    }
    url = f'{CHAT_URL}sendMessage?token={CHAT_TOKEN}'
    r = try_send(url, meta_chat)
    # Read, then wait proportionally to writing time
    natural_reply_time(reply_text)
    return True

def reply(reply_text, message, canonical = True):
    mark_as_read_and_wait(reply_text, message)
    user_id = message['user_id']
    meta_chat = {
        'body': reply_text,
        'chatId': user_id
    }
    log_handler.insert_message(meta_chat)
    if cli.is_on() == False:
        print(f'Sending text {reply_text} to chat api...')
        url = f'{CHAT_URL}sendMessage?token={CHAT_TOKEN}'
        try_send(url, meta_chat)
    else:
        cli.puts_reply(meta_chat)
    if user.get(user_id):
        if conversation.find(user_id) is None: conversation.create_delegated(message)
        if canonical == True:
            SENDER_ID = user.phone_to_id(os.getenv('ARBITRUR_PHONE'))
            conversation.update_canonical_conversation(SENDER_ID, user_id, reply_text, 'bot')
    return True

def set_webhook(webhook_url):
    meta_chat = {
        "set": True,
        "webhookUrl": webhook_url
    }
    return requests.post(f'{CHAT_URL}webhook?token={CHAT_TOKEN}', data=meta_chat).json()

def get_chats():
    return requests.get(f'{CHAT_URL}chats?token={CHAT_TOKEN}').json()

def get_messages():
    return requests.get(f'{CHAT_URL}messages?token={CHAT_TOKEN}').json()

def get_chat_user_name(user_id):
    try:
        name =  [chat for chat in get_messages()['messages'] if chat['chatId'] == user_id][0].get('senderName')
    except:
        name = ''
    return name
