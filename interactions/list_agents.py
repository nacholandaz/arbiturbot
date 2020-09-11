from vendors import chat_api
import user
import thread
import conversation
import pending_conversations

def logic(interaction, message):
  chat_api.reply("Estos son l@s agentes disponibles:", message)
  user_id = message['user_id']
  user.clean_agent_index()
  users_list = list(user.users.find({'type': 'agent'})) #message['user_id']
  if len(users_list) == 0:
      chat_api.reply("No hay agentes dados de alta", message)
      return True

  #Double check if uuids are correctly setup
  for user_info in users_list:
      if 'name' not in user_info: continue
      user_id = user_info['id']
      user_uuid = user_info['uuid']
      user_name = user_info['name']
      user_phone = user_info['phone']
      user_pending = pending_conversations.find(user_id = user_id, closed=False, new_messages=False)
      if len(user_pending)>0:
          string_pending = '* '
      else:
          string_pending = ''
      text_message = f"👤{user_uuid} {string_pending}= {user_name} ({user_phone})"
      chat_api.reply(text_message, message)
  return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
