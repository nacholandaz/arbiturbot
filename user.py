# Interacts with the database to follow conversations
from pymongo import MongoClient
from datetime import datetime
from operator import itemgetter
import os
from geo import get_country_name_and_flag

from vendors import chat_api, sheets

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
users = client.bot.users
print(os.getenv('ARBITRUR_MONGO_URL'))

def get(id_value, id_type = 'id'):
    try:
        user = list(users.find({id_type: id_value}))[0]
    except:
        user = None
    return user


def find(owner=None, thread_label = None, thread_solved = None, name = None, phone = None, uuid = None, user_type = None):
    all_users = list(users.find({}))
    if owner:
        all_users = [ind_user for ind_user in all_users if owner == ind_user['owner']]
    if thread_label:
        all_users = [ind_user for ind_user in all_users for thread in ind_user['threads'] if thread_label == thread['label']]
    if thread_solved:
        all_users = [ind_user for ind_user in all_users for thread in ind_user['threads'] if thread_solved == thread['solved']]
    if name:
        all_users = [ind_user for ind_user in all_users if name == ind_user['name']]
    if phone:
        all_users = [ind_user for ind_user in all_users if clean_phone(phone) == ind_user['phone']]
    if uuid:
        all_users = [ind_user for ind_user in all_users if uuid == ind_user['uuid']]
    if user_type:
        all_users = [ind_user for ind_user in all_users if user_type == ind_user['type']]
    return all_users

def fetch_user_data(user_data):
    name = user_data.get('name')
    uuid = user_data.get('uuid')
    if uuid is None:
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        hour = str(datetime.now().hour)
        uuid = 'u' + current_user_index()
    phone = user_data.get('phone')
    return name, uuid, phone

def fetch_agent(user_id):
    name = get_agent(user_id).get('name')
    uuid = 'agent_' + name[0:3].lower()
    phone = user_id.split('@')[0]
    return name, uuid, phone

def fetch_user(user_id):
    name = chat_api.get_chat_user_name(user_id)
    phone = user_id.split('@')[0]
    uuid = 'u' + current_user_index()
    return name, uuid, phone

def current_user_index():
    return str(len(list(users.find({'type': 'user'})))+1)

def index_exists(uuid): len(list(users.find({'uuid': uuid}))) > 0

def create(user_id, user_data = {}, user_source = 'inbound'):
    user_type = get_user_type(user_id)

    if user_type == 'agent':
        name, uuid, phone = fetch_agent(user_id)
    else:
        if len(user_data.keys())>0:
            name, uuid, phone = fetch_user_data(user_data)
        else:
            name, uuid, phone = fetch_user(user_id)

    if phone: country = get_country_name_and_flag(phone)
    user = {
        'id': user_id,
        'source': user_source,
        'type': user_type,
        'name': name,
        'uuid': uuid,
        'phone': phone,
        'country': country,
        'created_at': datetime.now(),
        'owner': None,
        'threads': [],
        'answering': False,
        'current_thread': None,
    }

    if 'owner' in user_data: user['owner'] = user_data.get('owner')

    return users.insert_one(user)

def update(user_id, user_data):
    # user_data = {field:value, field2:value2 ...z

    if 'phone' in user_data:
        user_data['country'] = country = get_country_name_and_flag(user_data['phone'])

    users.find_one_and_update(
        {"id": user_id},
        {"$set": user_data}
    )
    return True

def set_user_answering(user_id):
    update(user_id, {'answering':True})
    return True

def remove_user_answering(user_id):
    update(user_id, {'answering':False})
    return True

def is_bot_answering(user_id):
    user = get(user_id)
    answering = user.get('answering')
    if answering: return answering
    return False

@ring.dict(expire=24*60*60)
def agents():
    return sheets.get_agents_data()

def get_agent(user_id):
    for agent in agents():
        if agent in user_id: return agents().get(agent)
    return None

def get_user_type(user_id):
    if get_agent(user_id): return 'agent'
    return 'user'

def clean_phone(phone):
    replace_chars = [' ', '+', "-", ")", '(', '[', ']']
    for char in replace_chars:
      phone = phone.replace(char, '')
    if len(phone) == 10:
        prefix = '521'
    elif len(phone) == 11:
        prefix = '52'
    elif len(phone) == 12:
        phone = phone[2:]
        prefix = '521'
    else:
        prefix = ''
    return prefix + phone


def phone_to_id(phone): return clean_phone(phone) + '@c.us'

def id_to_phone(user_id):
    return user_id.split('@')[0]
