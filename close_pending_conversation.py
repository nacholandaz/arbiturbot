import user
from vendors import chat_api
from interactions import list_users
import conversation
import pending_conversations

def logic(interaction, message):
    # We can also use the command number detected before
    user_id = message['user_id']

    user_context = conversation.context(user_id)
    current_p_conversation = user_context.get('current_pending_conversation')
    current_p_conversation_id = current_p_conversation.get('id')

    if current_p_conversation is None:
        s_msg = "No se ha encontrado una conversación pendiente"
        chat_api.reply(s_msg, message)
        return None

    pending_conversations.close(current_p_conversation_id)
    redirect_pending_conversation = message['text'].split(' ')[0].lower()
    conversation.update_context(user_id, 'redirect_user', None)
    conversation.update_context(user_id, 'redirect_name', None)
    conversation.update_context(user_id, 'redirect_phone', None)
    conversation.update_context(user_id, 'conversational_level', 'user')
    conversation.update_context(user_id, 'current_pending_conversation', None)

    s_msg = "La conversacion pendiente "+ current_p_conversation_id + " ha sido cerrada."
    chat_api.reply(s_msg, message)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']

