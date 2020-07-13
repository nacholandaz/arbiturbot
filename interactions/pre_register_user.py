from geo import get_country_name_and_flag
import conversation
import user
from vendors import chat_api

def logic(interaction, message):
    user_id = message['user_id']
    conversation.update_context(user_id, 'syntax_error_u_plus', False)
    user_context = conversation.context(user_id)
    new_user_info = message.get('text')

    new_user_info = new_user_info.replace('+u ', '')
    name_phone_split = new_user_info.split('(')

    # Flow, check syntax
    if '(' not in new_user_info:
      conversation.update_context(user_id, 'syntax_error_u_plus', True)
      return True

    name = name_phone_split[0]
    phone = name_phone_split[1]
    phone = user.clean_phone(phone)

    print(phone)

    country = get_country_name_and_flag(phone)

    conversation.update_context(user_id, 'new_user_info_name', name)
    conversation.update_context(user_id, 'new_user_info_phone', phone)
    conversation.update_context(user_id, 'new_user_info_country', country)

    return True

def get_next_interaction(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    did_not_follow_syntax = user_context.get('syntax_error_u_plus')
    if did_not_follow_syntax == True:
      next_interaction = interaction['syntax_error']
      conversation.update_context(user_id, 'syntax_error_u_plus', False)
    else:
      next_interaction = interaction['next_interaction']
    return next_interaction
