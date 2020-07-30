from geo import get_country_name_and_flag
import conversation
import user
from vendors import chat_api
from interactions import list_users, list_agents

def logic(interaction, message):
    user_id = message['user_id']
    text = message['text']

    agent_uuid = text.split(' ')[0].lower()
    agent_data_uuid = user.find(uuid = agent_uuid)

    if len(agent_data_uuid) == 0:
        r_text = 'No se encontro ningún agente con dicho identificador'
        chat_api.reply(r_text, message)
        return True

    agent_data = agent_data_uuid[0]
    user_context = conversation.context(user_id)
    redirect_user_id = user_context.get('redirect_user')
    user_data = user.get(redirect_user_id)
    current_p_results = pending_conversations.find(user_id = redirect_user_id, closed = False)
    current_p = current_p_results[0].get('id') if len(current_p_results)>0 else None

    if current_p is None:
        pending_conversations.create(redirect_user_id, [agent_uuid])
        current_p_results = pending_conversations.find(user_id = redirect_user_id, closed = False)
        current_p = current_p_results[0].get('id') if len(current_p_results)>0 else None
    else:
        pending_conversations.switch_owner(current_p, user_id, agent_uuid)

    conversation.update_context(user_id, 'redirect_user', None)
    conversation.update_context(user_id, 'redirect_name', None)
    conversation.update_context(user_id, 'redirect_phone', None)
    conversation.update_context(user_id, 'conversational_level', 'user')
    conversation.update_context(user_id, 'current_pending_conversation', None)

    r_text = f'{agent_uuid} ha recibido al usuario {user_data['uuid']}'
    chat_api.reply(r_text, message)

    a_text = f'Has recibido al usuario {user_data['uuid']} de {user_id}'
    chat_api.reply(a_text, {'user_id': agent_uuid, 'text': a_text})
    return True


def get_next_interaction(interaction, message):
    return interaction['next_interaction']

