# Interacts with the database to follow conversations
from pymongo import MongoClient
from datetime import datetime
from operator import itemgetter
import os

import user

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
conversations = client.bot.conversations

def create(message, user_type = 'user', message_type = 'user_utterance', interaction_name= 'initial_user_message'):
    user_id = message.get('user_id')
    text = message.get('text')
    created_at = message.get('created_at')
    # Canonical Conversation is updated only at text recieved and sent.
    # Messages are updated at bot interaction
    conversation = {
        'user_id': user_id,
        'messages': [
            {
                'sender': user_type,
                'message': message,
                'type': message_type,
                'created_at': created_at,
                'interaction_name': interaction_name,
            }
        ],
        'canonical_conversation': [],
        'context': {}
    }
    return conversations.insert_one(conversation)

def create_delegated(message):
    user_id = message['user_id']
    create(message, user_type= 'bot', message_type= 'bot_utterance', interaction_name = 'sent_message')
    set_finished(user_id)
    return True


def update(interaction, interaction_name, message, user_type = 'bot', message_type = 'bot_response'):
    user_id = message.get('user_id')
    text = message.get('text')
    # Dont use created_at from message for conversation, so that makes for harder last message search
    new_message = {
                'sender': user_type,
                'message': message,
                'type': message_type,
                'created_at':datetime.now(),
                'interaction_name': interaction_name,
    }

    conversations.update({'user_id': user_id}, {'$push': {'messages': new_message}})
    return True

def update_canonical_conversation(sender_id, reciever_id, text, sender_type):
    new_canonical_message = {
                'sender_type': sender_type,
                'sender_id': sender_id,
                'reciever_id': reciever_id,
                'text': text,
                'created_at': datetime.now(),
    }

    if sender_type == 'bot':
        user_id = reciever_id
    else:
        user_id = sender_id

    conversations.update({'user_id': user_id}, {'$push': {'canonical_conversation': new_canonical_message}})
    return True


def find(user_id):
    try:
        conversation = [conversation for conversation in list(conversations.find({'user_id': user_id}))][0]
    except:
        conversation = None
    return conversation

def delete(user_id):
    try:
        list(conversations.remove({'user_id': user_id}))
        conversation = True
    except:
        conversation = None
    return conversation

def context(user_id):
    try:
        context_data = [conversation['context'] for conversation in list(conversations.find({'user_id': user_id}))][0]
        context_data.update(user.get(user_id))
    except:
        context_data=user.get(user_id)
    return context_data

def update_context(user_id, field, text):
    user_data = user.get(user_id)
    if field in user_data:
        user.update(user_id, {field: text} )
    else:
        conversations.update({'user_id': user_id}, {'$set': {'context.'+field: text}})
    return True

def find_last_message(user_id):
    try:
        user_conversation = list(conversations.find({'user_id': user_id}))[0]
        last_message_date = max(map(itemgetter('created_at'), user_conversation['messages']))
        last_message = [message for message in user_conversation['messages'] if message['created_at'] == last_message_date][0]
    except:
        last_message = None
    return last_message


def is_finished(user_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    if 'finished' in user_conversation:
        if user_conversation['finished'] == 'true':
            return True
    return False

def set_finished(user_id):
    conversations.update({'user_id': user_id}, {'$set': {'finished': 'true'}})

def get_user_messages(user_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    messages = [message['text'] for message in user_conversation['canonical_conversation'] if message['sender_type'] =='user']
    return list(set(messages))

def get_canonical_messages(user_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    output = []
    for message in user_conversation['canonical_conversation']:
        if 'BEGIN:VCARD' in message['text']:
            card_name = message['text'].split('FN:')[1].split('\n')[0]
            card_phone = message['text'].split('\nEND:')[0].split(':')[-1]
            message['text'] = f'[Usuario mando tarjeta de {card_name}({card_phone})]'
        if 'video upload disabled' in message['text'].lower():
            message['text'] = f'[Usuario mando un video]'
        if message['sender_type'] == 'user':
            message['text'] = '👤: *' + message['text']  + '*'
        output.append(message)
    output = sorted(output, key=lambda x: x['created_at'], reverse=True)
    return output

def get_printable_conversation(user_id):
    user_messages = ["- " + message['text'] for message in get_canonical_messages(user_id)]
    return '\n'.join(user_messages)

def get_last_message(user_id):
    return get_user_messages(user_id)[-1]


def get_last_canonical_message_id(user_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    messages = user_conversation['canonical_conversation']
    return len(messages)-1

def get_canonical_message(user_id, message_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    messages = user_conversation['canonical_conversation']
    if message_id is None: return {'text': '*No se encontro mensaje*'}
    return messages[message_id]

def get_canonical_user_message(user_id, position=0):
    # The idea is to use -1 for last canonical last user message, an 0 for first
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    messages = user_conversation['canonical_conversation']
    counter = 0
    for i, message in enumerate(messages):
        if message['sender_type'] == 'user':
            user_message_pos = i
            if position == 0:
                return user_message_pos
    return user_message_pos


def get_current_redirect_user(agent_id):
    agent_context = context(agent_id)
    return agent_context['redirect_user']
