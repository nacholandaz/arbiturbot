import user
from vendors import chat_api
from interactions import list_users, list_pending_conversations
import conversation
import pending_conversations

def logic(interaction, message):
    # We can also use the command number detected before
    user_id = message['user_id']
    user_data = user.get(user_id)
    agent_name = user_data.get('name')
    user_context = conversation.context(user_id)
    current_p_conversation_id = user_context.get('current_pending_conversation')

    if current_p_conversation_id is None:
        list_pending_conversations.logic(interaction, message)
        return None

    p_convo_data = pending_conversations.get(current_p_conversation_id)
    client_id = p_convo_data.get('user_id')
    client_data = user.get(client_id)
    client_name = client_data.get('name')

    conversation.update_context(client_id, 'is_closing', True)

    s_msg = f"Se ha invitado confirmar al usuari@ {client_name}({current_p_conversation_id}) a confirmar el cierre de su caso."
    chat_api.reply(s_msg, message)

    message_client = {'user_id': client_id}
    c_msg = f"Agente {agent_name} ha informado que ya tu caso ya no requiere seguimiento ¿Puedes confirmar? Responde si o no."
    chat_api.reply(c_msg, message_client)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
