import user
from vendors import chat_api
from interactions import list_users
import conversation
import pending_conversations

def logic(interaction, message):

    user_id = message['user_id']
    # We can also use the command number detected before
    redirect_user_number = message['text'].split(' ')[0].lower()
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

        current_p_results = pending_conversations.find(user_id = user_found['id'], closed = False)
        current_p = current_p_results[0].get('id') if len(current_p_results)>0 else None
        if current_p is None:
            pending_conversations.create(user_found['id'], owners= [user_id])
            current_p_results = pending_conversations.find(user_id = user_found['id'], closed = False)
            current_p = current_p_results[0].get('id') if len(current_p_results)>0 else None

        conversation.update_context(user_id, 'current_pending_conversation', current_p)
        pending_conversations.add_owner(current_p, user_id)
        pending_conversations.remove_new_messages(current_p)

        s_msg = "Haz selecionado al "+user_found['uuid']+" "+user_found['name']
        chat_api.reply(s_msg, message)

        s_msg = "Con la conversacion pendiente "+ str(current_p)
        chat_api.reply(s_msg, message)

    else:
        list_users.logic()
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']

