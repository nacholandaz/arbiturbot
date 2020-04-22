from vendors import chat_api
import conversation

def logic(interaction, message):
    return True

def get_next_interaction(interaction, message):
    user_id = message['user_id']
    conv_level = conversation.context(user_id).get('conversational_level')
    if conv_level == 'user': return interaction['user_interaction']
    return interaction['general_interaction']
