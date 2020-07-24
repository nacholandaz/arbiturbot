from pymongo import MongoClient
from datetime import datetime, timedelta
from operator import itemgetter
import os
from geo import get_country_name_and_flag
import user

from vendors import chat_api

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
pending_conversations = client.bot.pending_conversations

def get_next_index():
  return str(len(list(pending_conversations.find()))+1)

def create(user_id, owners = []):
  index = 'p' + get_next_index()
  creation_time = datetime.now()
  uuid = user.get(user_id)['uuid']
  pending_conversation = {
      'user_id': user_id,
      'user_uuid': uuid,
      'owners': owners,
      'id': index,
      'created_at': creation_time,
      'new_messages': True,
      'updated_at': creation_time,
      'closed': False
  }

  pending_conversations.insert_one(pending_conversation)

  return pending_conversation

def get(pending_conversation_id):
  try:
    output = list(pending_conversations.find({'id':pending_conversation_id}))[0]
  except:
    output = None
  return None


def find(user_id = None, owner = None, closed = None, new_messages = None):
  if user_id:
    response = list(pending_conversations.find({'user_id':user_id}))
  else:
    response = list(pending_conversations.find({}))
  if len(response) == 0:
    return []
  if owner:
    response = [ item for item in response if owner in item['owners'] or item['owners'] == []]
  if closed:
    response = [ item for item in response if item['closed'] == closed]
  if new_messages:
    response = [ item for item in response if item['new_messages'] == new_message]
  return response

def pending_conversations_agent_indicator(agent_id):
  number_pending_conversations = len(find(owner=agent_id))
  output_string = ''
  for n in range(number_pending_conversations):
    output_string += "*"
  return output_string

def close(pending_conv_id):
  pending_conversations.update({'id': pending_conv_id}, {'closed': True})
  return True

def received_new_messages(user_id):
  pending_conversations.find_one_and_update(
    {'user_id': user_id, 'closed': False},
    {"$set": {'new_messages': True}}
  )
  return True

def add_owner(pending_conv_id, owner):
  push_obj = {'$push': {'owners': owner}}
  pending_conversations.find_one_and_update(
    {'id': pending_conv_id}, push_obj
  )
  return True

def remove_owner(pending_conv_id, owner_remove):
  pen_conv = get(pending_conv_id)
  owners = [owner for owner in open_conv['owners'] if owner != owner_remove]
  pending_conversations.find_one_and_update(
    {'id'  : pending_conv_id}, {'set': {'owners': owners }}
  )
  return True

def alert_admins_pending(pending_conversation):
  if len(pending_conversation['owners']) == 0:
    agents = [u['id'] for u in user.find(user_type = 'agent')]
  else:
    agents = pending_conversation['owners']
  for agent in agents:
    text = pending_conversations_agent_indicator(agent)
    message = {
      'text': text,
      'user_id': agent
    }
    chat_api.reply(text, message)
  return None
