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

      current_name = user_context.get('new_user_info_name')
      current_phone = user_context.get('new_user_info_phone')

      if current_name is None:
        s_msg = "No esta seleccionado ningún usuario"
        chat_api.reply(s_msg, message)
        return True

      users_match = user.find(phone=current_phone, name=current_name)
      current_user_id = users_match[0].get('id')
      convo = user.get_printable_conversation(current_user_id)
      s_msg = "Los mensajes con el usuario actual es:"
      chat_api.reply(s_msg, message)
      chat_api.reply(convo, message)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
