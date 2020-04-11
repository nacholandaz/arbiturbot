from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
  user_id = message['user_id']
  chat_api.reply(interaction['text'], message)
  users_owned = user.find(owner=user_id) #message['user_id']
  for user_owned in users_owned:
      for thread_owned in user_owned['threads']:
          user_name = user_owned['name']
          user_phone = user_owned['phone']
          thread_label = thread.printable_label(thread_owned['label'])
          thread_status = thread.printable_status(thread_owned['label'])
          last_message = conversation.get_canonical_message(user_owned['id'],thread_owned['last_canonical_message_id'])
          text_message = f"👤{user_name}\n☎️{user_phone}\n⚠️{thread_label}/{thread_status}\n🗣️Último mensaje:('{last_message['text']}')"
          chat_api.reply(text_message, message)
  return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
