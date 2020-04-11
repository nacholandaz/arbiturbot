from phone_iso3166.country import phone_country
import conversation
import user
import thread

def logic(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    name = user_context.get('new_user_info_name')
    phone = user_context.get('new_user_info_phone')
    country = user_context.get('new_user_info_country')

    replace_chars = [' ', '+', "-", ")"]
    for char in replace_chars:
      phone = phone.replace(char, '')

    id_create_user = user.phone_to_id(phone)

    user_data = {
      'name': name,
      'phone': phone,
      'country': country,
      'owner': user_id,
    }

    user.create(id_create_user, user_data, 'outbound')
    thread.create(id_create_user, -1)
    user.update(user_id, {'redirect_user': id_create_user})
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
