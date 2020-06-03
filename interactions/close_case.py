from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
    agent_id = message['user_id']
    user_id = get_current_redirect_user(agent_id)
    label = interaction.get('label')
    user_open_threads = thread.find(user_id, label = label, solved = False)
    if user_open_threads == None:
        text_message = f"El/La usuari@ seleccionad@ no tiene casos abiertos..."
        chat_api.reply(text_message, message)
    if len(user_open_threads)>=0:
        thread.close(user_id)
        text_message = f"Caso cerrado satisfactoriamente"
        chat_api.reply(text_message, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
