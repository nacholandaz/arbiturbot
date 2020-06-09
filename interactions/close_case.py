from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
    agent_id = message['user_id']
    user_id = conversation.get_current_redirect_user(agent_id)
    label = interaction.get('label')
    user_open_threads = thread.find_all(user_id, label = label, solved = False)
    # Not sure if im going to check array size
    if len(user_open_threads)>=0:
        closed_thread = thread.close(user_id)
        if closed_thread == True:
            text_message = f"Caso cerrado satisfactoriamente"
            chat_api.reply(text_message, message)
            return True
    text_message = f"El/La usuari@ seleccionad@ no tiene casos de este tipo abiertos..."
    chat_api.reply(text_message, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
