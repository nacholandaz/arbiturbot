import user
from vendors import chat_api
from interactions import list_pending_conversations
import conversation
import pending_conversations

def logic(interaction, message):
    # We can also use the command number detected before
    user_id = message['user_id']
    current_p = message['text'].split(' ')[0].lower()

    current_p_object = pending_conversations.get(current_p)

    redirect_user_number= current_p_object['user_id']
    user_found = user.get(redirect_user_number)

    if user_found is not None:
        conversation.update_context(user_id, 'redirect_user', user_found['id'])
        conversation.update_context(user_id, 'redirect_name', user_found['name'])
        conversation.update_context(user_id, 'redirect_phone', user_found['phone'])
        conversation.update_context(user_id, 'conversational_level', 'user')

        if user_found.get('owner') is None:
            user.update(user_found['id'], { 'owner': user_id } )

        conversation.update_context(user_id, 'current_pending_conversation', current_p)
        pending_conversations.add_owner(current_p, user_id)
        pending_conversations.remove_new_messages(current_p)

        s_msg = "Haz selecionado al "+user_found['uuid']+" "+user_found['name']
        chat_api.reply(s_msg, message)

        s_msg = "Con la conversacion pendiente "+ current_p
        chat_api.reply(s_msg, message)

    else:
        already_selected_p = conversation.context('current_pending_conversation')
        if already_selected_p is None:
            list_pending_conversations.logic(interaction, message)
        else:
            already_p_object = pending_conversations.get(already_selected_p)
            already_user = user.get(already_p_object['user_id'])
            already_user_name = already_user.get('name')
            s_msg = "Sigues hablando con "+ already_user_name
            chat_api.reply(s_msg, message)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']

