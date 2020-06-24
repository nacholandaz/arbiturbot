from phone_iso3166.country import phone_country
import conversation
import user
import thread
from vendors import chat_api


def logic(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    name = user_context.get('new_user_info_name')
    phone = user_context.get('new_user_info_phone')
    country = user_context.get('new_user_info_country')
    id_create_user = user.phone_to_id(phone)

    user_data = {
      'name': name,
      'phone': phone,
      'country': country,
      'owner': user_id,
    }

    # Find users with same name
    users_by_name = user.find(name=name)
    if len(users_by_name) > 0:
      user_same_name = users_by_name[0]
    else:
      user_same_name = None

    users_by_name = user.find(name=name)
    user_same_name = users_by_name[0] if len(users_by_name) > 0 else None

    users_by_phone = user.find(phone=phone)
    user_same_phone = users_by_phone[0] if len(users_by_phone) > 0 else None

    no_change = False
    if users_by_name is None and user_same_phone is None:
      user.create(id_create_user, user_data, 'outbound')
      thread.create(id_create_user, -1)
      user_register = f"Haz registrado a un nuevo usuario. {user_data['name']} ({user_data['phone']})"
      chat_api.reply(user_register, message)


    elif user_same_phone is not None:
      if user_same_phone['name'] != user_data['name']:
        user.update(user_same_phone['id'],  {'name': name})
        name_change = f"Haz cambiado el nombre del usuario con {user_data['phone']}"
        chat_api.reply(name_change, message)
      else:
        no_change = True

    elif user_same_name is not None:
      if user_same_name['phone'] != user_data['phone']:
        user.update(user_same_name['id'],  {'phone': phone})
        phone_change = f"Haz cambiado el telefono del usuario con nombre de {user_data['name']}"
        chat_api.reply(phone_change, message)
      else:
        no_change = True

    if no_change == True: chat_api.reply('El usuario no sufrio cambios', message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
