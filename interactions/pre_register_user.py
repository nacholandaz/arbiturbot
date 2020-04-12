from geo import get_country_name_and_flag
import conversation

def logic(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    new_user_info = user_context['new_user_info']

    new_user_info = new_user_info.replace('+u ', '')
    name, phone = new_user_info.split(' (')
    pre_phone = phone.replace(')', '')
    replace_chars = [' ', '+', "-", ")"]
    for char in replace_chars:
      phone = phone.replace(char, '')

    country = get_country_name_and_flag(phone)

    conversation.update_context(user_id, 'new_user_info_name', name)
    conversation.update_context(user_id, 'new_user_info_phone', pre_phone)
    conversation.update_context(user_id, 'new_user_info_country', country)

    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']