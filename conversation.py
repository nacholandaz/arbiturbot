# Interacts with the database to follow conversations
from pymongo import MongoClient
from datetime import datetime
from operator import itemgetter
import os

client = MongoClient(os.environ['MONGO_URL'])
conversations = client.bot.conversations

def create(message):
    user_id = message.get('user_id')
    text = message.get('text')
    created_at = message.get('created_at')
    conversation = {
        'user_id': user_id,
        'messages': [
            {
                'sender': 'user',
                'message': message,
                'type': 'user_utterance',
                'created_at': created_at,
                'interaction_name': 'initial_user_message',
            }
        ],
        'context': {}
    }
    return conversations.insert_one(conversation)

def update(interaction, interaction_name, message):
    user_id = message.get('user_id')
    text = message.get('text')
    new_message = {
                'sender': 'bot',
                'message': message,
                'type': 'bot_response',
                'created_at': datetime.now(),
                'interaction_name': interaction_name,
    }
    conversations.update({'user_id': user_id}, {'$push': {'messages': new_message}})

def find_user(user_id):
    try:
        users = [conversation['user_id'] for conversation in list(conversations.find({'user_id': user_id}))][0]
    except:
        users = None
    return users

def context(user_id):
    try:
        context = [conversation['context'] for conversation in list(conversations.find({'user_id': user_id}))][0]
    except:
        context = None
    return context

def update_context(user_id, field, text):
    conversations.update({'user_id': user_id}, {'$set': {'context.'+field: text}})
    return True

def find_last_message(user_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    last_message_date = max(map(itemgetter('created_at'), user_conversation['messages']))
    last_message = [message for message in user_conversation['messages'] if message['created_at'] == last_message_date][0]
    return last_message


def is_finished(user_id):
    user_conversation = list(conversations.find({'user_id': user_id}))[0]
    if 'finished' in user_conversation:
        if user_conversation['finished'] == 'true':
            return True
    return False

def set_finished(user_id):
    conversations.update({'user_id': user_id}, {'$set': {'finished': 'true'}})
