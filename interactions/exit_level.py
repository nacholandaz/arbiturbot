import user
import conversation

def logic(interaction, message):
    user_id = message['user_id']
    conversation.update_context(user_id, 'redirect_user', None)
    conversation.update_context(user_id, 'redirect_name', None)
    conversation.update_context(user_id, 'redirect_phone', None)
    conversation.update_context(user_id, 'conversational_level', 'general')
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
