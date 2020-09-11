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

def clean_pending_index():
    current_p = list(pending_conversations.find({}))
    current_pids = []
    current_pending_users = []
    for p in current_p:

        # There can only be one open pending conversation
        removed_p = False
        if p['user_id'] in current_pending_users:
          if p['closed'] == False:
            removed_p = True
            pending_conversations.remove(
              {'id': p['id']}
            )
        else:
          if p['closed'] == False:
            current_pending_users.append(p['user_id'])

        if removed_p == True:
          continue

        if p['id'] in current_pids:
          past_pid = p['id']
          p['id'] = 'p' + get_next_index()
          del p['_id']
          pending_conversations.find_one_and_update(
              {"id": past_pid},
              {"$set": p}
          )

        current_pids.append(p['id'])

    return True

def create(user_id, owners = []):
  index = 'p' + get_next_index()
  creation_time = datetime.now()
  pending_conversation = {
      'user_id': user_id,
      'owners': owners,
      'id': index,
      'created_at': creation_time,
      'new_messages': True,
      'updated_at': creation_time,
      'closed': False
  }

  pending_conversations.insert_one(pending_conversation)
  clean_pending_index()
  return pending_conversation

def get(pending_conversation_id):
  try:
    output = list(pending_conversations.find({'id':pending_conversation_id}))[0]
  except:
    output = None
  return output

def find(user_id = None, owner = None, closed = None, new_messages = None):
  if user_id:
    response = list(pending_conversations.find({'user_id':user_id}))
  else:
    response = list(pending_conversations.find({}))
  if len(response) == 0:
    return []
  if owner:
    response = [ item for item in response if owner in item['owners'] or len(item['owners']) == 0]
  if closed is not None:
    response = [ item for item in response if item['closed'] == closed]
  if new_messages is not None:
    response = [ item for item in response if item['new_messages'] == new_messages]
  return response

def pending_conversations_agent_indicator(agent_id):
  n_pending_conv = len(find(owner=agent_id, closed = False, new_messages = True))
  output_string = ''
  for n in range(n_pending_conv):
    output_string += "*"
  return output_string

def close(pending_conv_id):

  pending_conversations.find_one_and_update(
    {'id': pending_conv_id},
    {"$set": {'closed': True, 'new_messages': False}}
  )
  return True

def open(pending_conv_id):
  pending_conversations.find_one_and_update(
    {'id': pending_conv_id},
    {"$set": {'closed': False, 'new_messages': True}}
  )
  return True

def received_new_messages(user_id):
  pending_conversations.find_one_and_update(
    {'user_id': user_id, 'closed': False},
    {"$set": {'new_messages': True}}
  )
  return True

def remove_new_messages(user_id):
  pending_conversations.find_one_and_update(
    {'user_id': user_id, 'closed': False},
    {"$set": {'new_messages': False}}
  )
  return True

def add_owner(pending_conv_id, owner):
  pen_conv = get(pending_conv_id)
  if owner in pen_conv['owners']:
    return True
  push_obj = {'$push': {'owners': owner}}
  pending_conversations.find_one_and_update(
    {'id': pending_conv_id}, push_obj
  )
  return True

def remove_owner(pending_conv_id, owner_remove):
  pen_conv = get(pending_conv_id)
  owners = [owner for owner in pen_conv['owners'] if owner != owner_remove]
  pending_conversations.find_one_and_update(
    {'id'  : pending_conv_id}, {'$set': {'owners': owners }}
  )
  return True

def switch_owner(pending_conv_id, owner_remove, owner_add):
  remove_owner(pending_conv_id, owner_remove)
  add_owner(pending_conv_id, owner_add)
  return True

def alert_admins_pending(pending_conversation):
  print('Alerting Admins of new message')
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


def delete_user(user_id):
  response = list(pending_conversations.remove({'user_id':user_id}))
  return True

def delete_agent(agent_id):
  pending_convos_agent = find(owner = agent_id)
  for pending_convo in pending_convos_agent:
    remove_owner(pending_convo['id'], agent_id)
  return True
