import send
from conversation import context
import os

def logic(interaction, message):
    user_context = context(message['user_id'])
    message = { 'user_id': os.environ['TESTING_ADMIN']}
    text_alert = f"Nos hablo el usuario con nombre: {user_context['user_name']}"
    send.reply(text_alert, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
