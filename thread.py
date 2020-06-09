from datetime import datetime
import conversation
import user

def find_all(user_id=None, label = None, solved = None):
  if user_id:
    response = list(user.users.find({'id':user_id}))[0]['threads']
  else:
    all_users = list(user.users.find({}))
    response = [item for user_convo in all_users for item in user_combo['threads']]
  if label:
    response = [ item for item in response if item['label'] == label]
  if solved:
    response = [ item for item in response if item['solved'] == solved]
  return response


def create(user_id, first_message_id = None, label = None, last_message_id = None, label_set_by = 'arbi'):
  if first_message_id == None:
      first_message_id = conversation.get_canonical_user_message(user_id, position=0)

  current_threads = user.get(user_id).get('threads')
  current_thread_pos =len(current_threads)-1

  new_thread = {
    'label': label,
    'label_set_by': label_set_by,
    'label_set_at': datetime.now(),
    'first_canonical_message_id':first_message_id,
    'last_canonical_message_id':last_message_id,
    'solved': False,
    'closed_at': None,
    'created_at': datetime.now(),
    'updated_at': datetime.now(),
    'current_thread':current_thread_pos,
  }

  push_obj = {'$push': {'threads': new_thread}}

  user.users.update({'id': user_id}, push_obj)
  return True

def find(user_id):
  try:
    threads = list(user.users.find({'id':user_id}))[0]['threads']
  except:
    threads = None
  return threads

def get(user_id, thread_id):
  try:
    thread = list(user.users.find({'id':user_id}))[0]['threads'][thread_id]
  except:
    thread = None
  return threads

def current_open_thread(user_id, label=None, solved = False):
  user_threads = find(user_id)
  threads_reverse = user_threads[::-1]
  for i, thread in enumerate(threads_reverse):
      if label is not None:
        if thread['solved'] == False and thread['label'] == label and thread['solved'] == solved:
            return len(user_threads) - i - 1
      else:
        if thread['solved'] == False and thread['solved'] == solved:
            return len(user_threads) - i - 1
  return None

def close(user_id, thread_id = None, label = None):
  if thread_id is None: thread_id = current_open_thread(user_id, label=label, solved = False)
  if thread_id is None: return False
  last_message_id = conversation.get_canonical_user_message(user_id, -1)
  user.users.update(
    {'id': user_id},
    {'$set':
      {
        f'threads.{str(thread_id)}.solved': True,
        f'threads.{str(thread_id)}.last_canonical_message_id': last_message_id,
        f'threads.{str(thread_id)}.closed_at': datetime.now(),
        f'threads.{str(thread_id)}.updated_at': datetime.now(),
      }
    }
  )
  return True

def update(user_id, thread_id, field, value):
    user.users.find_one_and_update(
        {"id": user_id},
        {"$set":
          {f"threads.{thread_id}.{field}": value}
        },
        upsert=True
    )
    return True

def printable_label(label):
    label_dict = {None: 'indefinido', 'sale': 'venta', 'report': 'reporte'}
    return label_dict.get(label)

def printable_status(solved):
    if solved == True: return 'resuelto'
    return 'sin resolver'

def get_user_threads(user_id):
  return user.get(user_id).get('threads')

def set_thread_as_current(user_id, thread_id):
  user_threads = get_user_threads(user_id)
  if thread_id <= len(user_threads) - 1:
    user.users.update({'id': user_id}, push_obj)
    push_obj = {'$push': {'current_thread': current_thread_pos}}
    user.users.update({'id': user_id}, push_obj)
    return True
  return None
