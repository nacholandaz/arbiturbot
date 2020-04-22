import user

def logic(interaction, message):
    user_id = message['user_id']
    redirect_user_id = user.phone_to_id(message['text'].split('u '))
    user_found = user.get(redirect_user_id)
    if user_found is not None:
          user.update(user_id, {'redirect_user': user_found['id']})
          user.update(user_id, {'redirect_name': user_found['name']})
          user.update(user_id, {'redirect_phone': user_found['phone']})
          user.update(user_id, {'conversational_level': 'user'})
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
