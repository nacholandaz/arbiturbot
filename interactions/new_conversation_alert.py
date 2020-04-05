import os

from vendors import chat_api
from conversation import context

def logic(interaction, message):
    user_context = context(message['user_id'])
    # TODO(ricalanis): Change to broadcast
    message = { 'user_id': os.getenv('TESTING_AGENT')}
    text_alert = f"Nos hablo el usuario con nombre: {user_context['name']}"
    chat_api.reply(text_alert, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
