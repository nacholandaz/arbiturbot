import user

def logic(interaction, message):
    user_id = message['user_id']
    user.update(user_id, {'redirect_user': None})
    user.update(user_id, {'redirect_name': None})
    user.update(user_id, {'redirect_phone': None})
    user.update(user_id, {'conversational_level': 'general'})
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
