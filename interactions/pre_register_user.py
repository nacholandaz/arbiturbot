from geo import get_country_name_and_flag
import conversation
import user
from vendors import chat_api

def logic(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    new_user_info = message.get('text')

    new_user_info = new_user_info.replace('+u ', '')
    if ' (' not in new_user_info or len(new_user_info.split(' '))!=2:
      chat_api.reply('El formato que debes usar es "+u Nombre (5218121231234)" - usando siempre (', message)
      return True

    name_phone_split = new_user_info.split(' (')
    if len(name_phone_split) != 2:
      chat_api.reply('No se detecta la separacion de nombre y telefono', message)
      return True

    name = name_phone_split[0]
    phone = name_phone_split[1]
    phone = user.clean_phone(phone)

    print(phone)

    country = get_country_name_and_flag(phone)

    conversation.update_context(user_id, 'new_user_info_name', name)
    conversation.update_context(user_id, 'new_user_info_phone', pre_phone)
    conversation.update_context(user_id, 'new_user_info_country', country)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
