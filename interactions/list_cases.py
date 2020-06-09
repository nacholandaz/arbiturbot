from vendors import chat_api
import user
import thread
import conversation

def logic(interaction, message):
    chat_api.reply(interaction['text'], message)
    user_id = message['user_id']
    users_owned = list(user.users.find())
    found_threads = False
    for user_owned in users_owned:
        for thread_owned in user_owned['threads']:
            user_name = user_owned['name']
            user_phone = user_owned['phone']
            thread_label = thread.printable_label(thread_owned['label'])
            thread_status = thread.printable_status(thread_owned['solved'])
            if thread_owned['label'] == None or thread_owned['solved'] == False:
                message_label = 'Primer mensaje'
                message_fetch = conversation.get_canonical_message(user_owned['id'],thread_owned['first_canonical_message_id'])
            else:
                message_label = 'Último mensaje'
                message_fetch = conversation.get_canonical_message(user_owned['id'],thread_owned['last_canonical_message_id'])
            text_message = f"👤{user_name}\n☎️{user_phone}\n⚠️{thread_label}/{thread_status}\n🗣️{message_label}:*{message_fetch['text']}*"
            chat_api.reply(text_message, message)
            found_threads = True
    if found_threads == False:
        text_message = f"*No se encontraron casos*"
        chat_api.reply(text_message, message)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
