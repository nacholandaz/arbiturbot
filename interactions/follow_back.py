from vendors import chat_api
import conversation
import pending_conversations
from datetime import datetime, timedelta

def logic(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    last_reply_time = user_context.get('last_reply_time')

    user_id = message['user_id']
    current_p_convo_id = user_context.get('current_pending_conversation')
    is_closing = user_context.get('is_closing')

    current_p_data = pending_conversation.get(current_p_convo_id)
    current_user = user.get(user_id)
    user_name = current_user.get('name')

    if current_p_convo_id is not None and is_closing == True:
        text = message.get('message').lower().split(' ')[0]

        if text == 'si':
            pending_conversations.close(current_p_convo_id)

            for owner in current_p_data['owners']:
                agent_context = conversation.context(owner)
                redirect_user = agent_context.get('redirect_user')
                agent_p_convo = agent_context.get('current_pending_conversation')
                message = {'user_id': owner}
                c_msg = 'La conversación pendiente con {user_name}({current_p_convo_id}) se ha cerrado'
                chat_api.reply(interaction['text'], message)

                if redirect_user == user_id and current_p_convo_id == agent_p_convo:
                    conversation.update_context(owner, 'redirect_user', None)
                    conversation.update_context(owner, 'redirect_name', None)
                    conversation.update_context(owner, 'redirect_phone', None)
                    conversation.update_context(owner, 'conversational_level', 'user')
                    conversation.update_context(owner, 'current_pending_conversation', None)

        elif text == 'no':
            for owner in current_p_data['owners']:
                agent_context = conversation.context(owner)
                message = {'user_id': owner}
                c_msg = 'El usuario {redirect_name} no ha confirmado el cierre de su conversación'
                chat_api.reply(interaction['text'], message)

        conversation.update_context(user_id, 'is_closing', False)
        return True


    if last_reply_time is None:
        conversation.update_context(user_id, 'last_reply', datetime.now())
        chat_api.reply(interaction['text'], message)
    else:
        if last_reply_time > last_reply_time + timedelta(hours = 24):
            conversation.update_context(user_id, 'last_reply', datetime.now())
            chat_api.reply(interaction['text'], message)
        else:
            None
            # Do nothing if 24 before last reply did not happen
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
