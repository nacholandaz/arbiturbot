import user
from vendors import chat_api
from interactions import list_users
import conversation

def logic(interaction, message):

    user_id = message['user_id']
    # We can also use the command number detected before
    redirect_user_number = redirect_user_id.split(' ')[0]
    users_uuid = user.find(uuid = redirect_user_number)
    try:
        user_found = users_uuid[0]
    except:
        user_found = None

    if user_found is not None:
        conversation.update_context(user_id, 'redirect_user', user_found['id'])
        conversation.update_context(user_id, 'redirect_name', user_found['name'])
        conversation.update_context(user_id, 'redirect_phone', user_found['phone'])
        conversation.update_context(user_id, 'conversational_level', 'user')

        if user_found.get('owner') is None:
            user.update(user_found['id'], { 'owner': user_id } )

    else:
        chat_api.reply('Selecciona un u#', message)
        list_users.logic()
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']

