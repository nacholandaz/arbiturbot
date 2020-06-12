import user
from vendors import chat_api
import conversation

def logic(interaction, message):
    user_id = message['user_id']
    redirect_user_id = user.phone_to_id(message['text'].replace('u ', ''))
    user_found = user.get(redirect_user_id)
    if user_found is not None:
        conversation.update_context(user_id, 'redirect_user', user_found['id'])
        conversation.update_context(user_id, 'redirect_name', user_found['name'])
        conversation.update_context(user_id, 'redirect_phone', user_found['phone'])
        conversation.update_context(user_id, 'conversational_level', 'user')

        chat_api.reply('La conversación con este usuario es:', message)
        user_messages = conversation.get_printable_conversation(user_id)
        chat_api.reply(user_messages, message)

    else:
        chat_api.reply('No encontramos dicho usuario', message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
