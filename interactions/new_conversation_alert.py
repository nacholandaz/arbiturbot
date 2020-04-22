import os
import user

from vendors import chat_api
from conversation import context, get_printable_conversation, get_last_message

def logic(interaction, message):
    user_id = message['user_id']
    user_context = context(message['user_id'])
    # TODO(ricalanis): Change to broadcast
    agent_phones = [key for key in user.agents().keys()]
    last_message = get_last_message(user_id)
    for phone in agent_phones:
        agent_user_id = user.phone_to_id(phone)
        message = { 'user_id': user.phone_to_id(phone)}
        agent_name = user.agents()[phone]['name']

        text_alert = f"Acaba de llegar un mensaje de: {user_context['name']}({user_context['phone']})"
        chat_api.reply(text_alert, message)

        text_alert = f"*Ultimo mensaje: {last_message}*"
        chat_api.reply(text_alert, message)

        user.update(agent_user_id, {'last_message_user': user_context['id']})
        user.update(agent_user_id, {'last_message_name': user_context['name']})
        user.update(agent_user_id, {'last_message_phone': user_context['phone']})

        text_alert = f"Escribe 'p' para poner un timer de 5 min a esta conversación y entrar en la conversación con {user_context['name']}({user_context['phone']}). Por lo contrario sigue escribiendo."
        chat_api.reply(text_alert, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
