import os

from vendors import chat_api
from conversation import context, get_printable_conversation
from user import agents, phone_to_id


def logic(interaction, message):
    user_id = message['user_id']
    user_context = context(message['user_id'])
    # TODO(ricalanis): Change to broadcast
    agent_phones = [key for key in agents().keys()]
    conversation = get_printable_conversation(user_id)
    for phone in agent_phones:
        message = { 'user_id': phone_to_id(phone)}
        agent_name = agents()[phone]['name']
        text_alert = f"Hola, {agent_name}!"
        chat_api.reply(text_alert, message)
        text_alert = f"Nos hablo el usuario con nombre: {user_context['name']}({user_context['phone']})"
        chat_api.reply(text_alert, message)
        text_alert = f"Mostrando mensajes iniciales:"
        chat_api.reply(text_alert, message)
        text_alert = f"{conversation}"
        chat_api.reply(text_alert, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
