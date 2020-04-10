from datetime import datetime

import conversation
import user


def find_all(user_id=None, label = None, solved = None):
  if user_id:
    response = list(users.find({'id':user_id}))[0]['threads']
  else:
    all_users = list(users.find({}))
    response = [item for user_convo in all_users for item in user_combo['threads']]
  if label:
    response = [ item for item in response in item['label'] == label]
  if solved:
    response = [ item for item in response in item['solved'] == solved]
  return solved


def create(user_id, last_message_id, label = None, first_message_id = None):
  new_thread = {
    'label': None,
    'first_canonical_message_id':None,
    'last_canonical_message_id':last_message_id,
    'solved': False,
    'created_at': datetime.now(),
    'updated_at': datetime.now(),
  }
  users.update({'id': user_id}, {'$push': {'threads': new_thread}})

def get(user_id, thread_id):
  try:
    return list(users.find({'id':user_id}))[0]['threads'][thread_id]
  except:
    None
  return None

def update(user_id, thread_id, field, value):
    users.find_one_and_update(
        {"id": user_id},
        {"$set":
          {f"threads.{thread_id}.{field}": value}
        },
        upsert=True
    )
    return True
