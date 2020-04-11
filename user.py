# Interacts with the database to follow conversations
from pymongo import MongoClient
from datetime import datetime
from operator import itemgetter
import os
from geo import get_country_name_and_flag

from vendors import chat_api
import thread

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
users = client.bot.users

print(os.getenv('ARBITRUR_MONGO_URL'))

def get(id_value, id_type = 'id'):
    try:
        user = list(users.find({id_type: id_value}))[0]
    except:
        user = None
    return user


def find(owner=None, thread_label = None, thread_solved = None):
    all_users = list(users.find({}))
    if owner:
        all_users = [ind_user for ind_user in all_users if owner in ind_user['owners']]
    if thread_label:
        all_users = [ind_user for ind_user in all_users for thread in ind_user['threads'] if thread_label == thread['label']]
    if thread_solved:
        all_users = [ind_user for ind_user in all_users for thread in ind_user['threads'] if thread_solved == thread['solved']]
    return all_users


def fetch_user_data(user_data):
    name = user_data.get('name')
    uuid = user_data.get('uuid')
    if uuid is None:
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        hour = str(datetime.now().hour)
        uuid = name[0:3].lower() + hour+ day+ month
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
    uuid = 'inbound_' + phone[-5:]
    return name, uuid, phone

def create(user_id, user_data = {}, user_source = 'inbound'):
    user_type = get_user_type(user_id)

    if len(user_data.keys())>0:
        name, uuid, phone = fetch_user_data(user_data)
    else:
        if user_type == 'agent':
            name, uuid, phone = fetch_agent(user_id)
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
        'owners': [],
        'threads': [],
    }

    if 'owner' in user_data:
        user['owners'].append(user_data.get('owner'))

    return users.insert_one(user)

def update(user_id, user_data):
    # user_data = {field:value, field2:value2 ...z

    if phone in user_data: user_data['country'] = phone_country(phone)

    users.find_one_and_update(
        {"id": user_id},
        {"$set": user_data},
        upsert=True
    )
    return True

def agents(): return {
    '8117649489': {'name': 'Ric'},
}

def get_agent(user_id):
    for agent in agents():
        if agent in user_id: return agents().get(agent)
    return None

def get_user_type(user_id):
    if get_agent(user_id): return 'agent'
    return 'user'

def phone_to_id(phone):
    phone = phone.replace(' ', '').replace('+', '')
    if len(phone) == 10: return '521' + phone + '@c.us'
    return phone + '@c.us'

def id_to_phone(user_id):
    return user_id.split('@')[0]
