from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
  user_id = message['user_id']
  chat_api.reply(interaction['text'], message)
  users_list = list(user.users.find()) #message['user_id']
  for user_info in users_list:
      user_name = user_info['name']
      user_phone = user_info['phone']
      user_last_message = find_last_message(user_info)
      text_message = f"👤{user_name}\n☎️{user_phone}\n🗣️Último mensaje:('{last_message['text']}')"
      chat_api.reply(text_message, message)
  return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
