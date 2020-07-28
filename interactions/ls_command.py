from vendors import chat_api
from interactions import list_users, list_cases, list_pending_conversations
import user
import thread
import conversation

def logic(interaction, message):
    user_id = message.get('user_id')
    try:
      ls_type = message['text'].split(' ')[1]
    except:
      ls_type = None

    if ls_type == 'u':
      list_users.logic(interaction, message)
    elif ls_type == 'c':
      list_cases.logic(interaction, message)
    elif ls_type == 'p':
      list_pending_conversations.logic(interaction, message)
    else:
      user_id = message['user_id']
      user_context = conversation.context(user_id)
      current_id = user_context.get('redirect_user')

      if current_id is None:
        s_msg = "No esta seleccionado ningún usuario"
        chat_api.reply(s_msg, message)
        return True

      convo = conversation.get_printable_conversation(current_id)
      s_msg = "Los mensajes con el usuario actual es:"
      chat_api.reply(s_msg, message)
      chat_api.reply(convo, message)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
