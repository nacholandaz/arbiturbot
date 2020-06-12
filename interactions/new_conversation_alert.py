import os
import user

from vendors import chat_api
from conversation import context, get_printable_conversation, get_last_message, update_context

def logic(interaction, message):
    user_id = message['user_id']
    user_context = context(message['user_id'])
    # TODO(ricalanis): Change to broadcast
    agent_phones = [key for key in user.agents().keys()]
    last_message = get_last_message(user_id)
    user_new_message = user.get(user_context['id'])

    if user_new_message.get('owner') is not None:
        message_redirect = f"Mensaje de {user_context['name']}({user_context['phone']}):{last_message}"
        message = {'user_id': user.get('owner')}
        chat_api.reply(message_redirect, message)
        return True

    for phone in agent_phones:
        agent_user_id = user.phone_to_id(phone)
        if user.get(agent_user_id) is None: continue
        message = { 'user_id': user.phone_to_id(phone)}
        agent_name = user.agents()[phone]['name']

        text_alert = f"Acaba de llegar un mensaje de: {user_context['name']}({user_context['phone']})"
        chat_api.reply(text_alert, message)

        text_alert = f"*Ultimo mensaje: {last_message}*"
        chat_api.reply(text_alert, message)

        update_context(agent_user_id, 'last_message_user', user_context['id'])
        update_context(agent_user_id, 'last_message_name', user_context['name'])
        update_context(agent_user_id, 'last_message_phone', user_context['phone'])

        text_alert = f"Escribe 'p' para poner un timer de 5 min a esta conversación y entrar en la conversación con {user_context['name']}({user_context['phone']}). Por lo contrario sigue escribiendo."
        chat_api.reply(text_alert, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
