from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
  chat_api.reply(interaction['text'], message)
  user_id = message['user_id']
  users_list = list(user.users.find()) #message['user_id']
  for user_info in users_list:
      if 'name' not in user_info: continue
      user_id = user_info['id']
      user_name = user_info['name']
      user_phone = user_info['phone']
      user_last_message = conversation.get_last_message(user_id)
      text_message = f"👤{user_name}\n☎️{user_phone}\n🗣️Último mensaje:{user_last_message}"
      chat_api.reply(text_message, message)
  return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
