from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
    agent_id = message['user_id']
    user_id = conversation.get_current_redirect_user(agent_id)
    label = interaction.get('label')
    current_thread = thread.current_open_thread(user_id, label=label)
    if current_thread:
        text_message = f"Advertencia: Hay un caso pendiente por cerrar con est@ usuari@"
        chat_api.reply(text_message, message)
    thread.create(user_id, label = label, label_set_by = 'agent')
    text_message = f"Caso creado satisfactoriamente"
    chat_api.reply(text_message, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
