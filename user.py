# Interacts with the database to follow conversations
from pymongo import MongoClient
from datetime import datetime, timedelta
from operator import itemgetter
import os
from geo import get_country_name_and_flag
import conversation
import pending_conversations
import notification


from vendors import chat_api, sheets

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
users = client.bot.users
agents_source = client.bot.agent_source
print(os.getenv('ARBITRUR_MONGO_URL'))

def get(id_value, id_type = 'id'):
    try:
        user = list(users.find({id_type: id_value}))[0]
    except:
        user = None
    return user


def find(user_id = None, owner=None, thread_label = None, thread_solved = None, name = None, phone = None, uuid = None, user_type = None):
    all_users = list(users.find({}))
    if user_id:
        all_users = [ind_user for ind_user in all_users if user_id == ind_user['id']]
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
    uuid = 'a' + current_agent_index()
    phone = user_id.split('@')[0]
    return name, uuid, phone

def fetch_user(user_id):
    name = chat_api.get_chat_user_name(user_id)
    phone = user_id.split('@')[0]
    uuid = 'u' + current_user_index()
    return name, uuid, phone

def current_user_index():
    return str(len(list(users.find({'type': 'user'})))+1)

def current_agent_index():
    return str(len(list(users.find({'type': 'agent'})))+1)

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
    users.insert_one(user)

    message = {'user_id': user_id}
    if user_source == 'inbound':
        message['text'] = 'Start message'
        conversation.create(message)
    else:
        message['text'] = 'Start message'
        conversation.create(message,
                            user_type= 'bot',
                            message_type= 'bot_utterance',
                            interaction_name = 'finish_conversation')

    # Add pending conversation if the given user model is a client
    if user_type == 'user':
        if user_data.get('owner'):
            owners_pending_convo = [user_data.get('owner')]
        else:
            owners_pending_convo = []
        pending_conversations.create(user_id, owners = owners_pending_convo)

    if user_type == 'agent':
        for hour in [9, 17]:
            notification.create(
                user_id,
                notification_type = 'set_time',
                notification_nature = 'timed',
                settings = { 'hour': hour, 'minute': 0 }
            )
    return True

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

def insert_agent_data():
    output = {}
    agent_info = sheets.get_agents_data()
    agent_info['created_at'] = datetime.now()
    agents_source.remove({})
    agents_source.insert([agent_info])
    response = agent_info
    del response['created_at']
    print('**** Updated agent list ******')
    return response

def agents():
    all_agents = list(agents_source.find({}))
    if len(all_agents) == 0: return insert_agent_data()
    if datetime.now() > all_agents[0]['created_at'] + timedelta(minutes=5):
        return insert_agent_data()
    response = all_agents[0]
    del response['created_at']
    return response

def get_agent(user_id):
    for agent in agents():
        if agent in user_id: return agents().get(agent)
    return None

def get_user_type(user_id):
    if is_user_server(user_id): return 'server'
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

def server_user_id():
    arbi_phone = str(os.getenv('ARBITRUR_PHONE'))
    return f'521{arbi_phone}@c.us'

def is_user_server(user_id):
    arbi_user = server_user_id()
    return user_id == arbi_user

def remove_user(user_id):
    user = list(users.remove({'id': user_id}))
    return True

def delete(user_id):
    user_type = get_user_type(user_id)
    if user_type == 'user':
        print(f"deleting user: {user_id}")
        delete_user(user_id)
    if user_type == 'agent':
        print(f"deleting agent: {user_id}")
        delete_agent(user_id)
    return True

def delete_user(user_id):
    conversation.delete(user_id)
    pending_conversations.delete_user(user_id)
    remove_user_from_all_agents_redirect(user_id)
    remove_user(user_id)
    return True

def delete_agent(agent_id):
    conversation.delete(agent_id)
    pending_conversations.delete_agent(agent_id)
    remove_user(agent_id)
    return True

def remove_user_from_agent_redirect(user_id, agent_id):
    user_context = conversation.context(agent_id)
    redirect_user = user_context.get('redirect_user')
    if redirect_user == user_id:
        conversation.update_context(agent_id, 'redirect_user', None)
        conversation.update_context(agent_id, 'redirect_name', None)
        conversation.update_context(agent_id, 'redirect_phone', None)
        conversation.update_context(agent_id, 'conversational_level', 'user')
        conversation.update_context(agent_id, 'current_pending_conversation', None)

def remove_user_from_all_agents_redirect(user_id):
    agents_data = find(user_type = 'agent')
    for agent in agents_data:
        remove_user_from_agent_redirect(user_id, agent['id'])
    return True


def demote_to_user_if_needed(user_id, user_data):
    agents_results = len(find(user_id = user_id, user_type = 'agent'))
    if agents_results > 0 and get_agent(user_id) == 'user':
        delete_agent(user_id)
        create(user_id, user_data)
    return True


def promote_to_agent_if_needed(user_id, user_data):
    user_results = len(find(user_id = user_id, user_type = 'user'))
    if user_results > 0 and get_agent(user_id) == 'agent':
        delete_user(user_id)
        create(user_id, user_data)
    return True

