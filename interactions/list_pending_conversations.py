from vendors import chat_api
import user
import pending_conversations
import thread
import conversation

def logic(interaction, message):
  chat_api.reply("Selecciona una conversacion pendiente:", message)
  user_id = message['user_id']
  p_list = list(pending_conversations.find(owner = user_id, closed = False)) #message['user_id']
  if len(p_list) == 0:
      chat_api.reply("No hay casos pendientes a resolver", message)
      return True
  for p in p_list:
      p_user_uuid = p['uuid']
      star_messages = ''
      if p['new_messages'] == True:
          star_messages = '* '
      user_p = user.get(p['user_id'])
      #user_name = user_info['name']
      #user_phone = user_info['phone']
      text_message = f"👤{p['id']} {star_messages}= {user_p['name']}"
      chat_api.reply(text_message, message)
  return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
