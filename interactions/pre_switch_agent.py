from geo import get_country_name_and_flag
import conversation
import user
from vendors import chat_api
from interactions import list_users, list_agents

def logic(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    redirect_user = user_context.get('redirect_user')
    conversation.update_context(user_id, 'no_redirect_user', False)

    if redirect_user is None:
        conversation.update_context(user_id, 'no_redirect_user', True)
        list_users.logic(interaction, message)
        return True

    list_agents.logic(interaction, message)
    return True


def get_next_interaction(interaction, message):
    user_id = message['user_id']
    user_context = conversation.context(user_id)
    no_redirect_user = user_context.get('no_redirect_user')
    if no_redirect_user == True:
      next_interaction = interaction['no_redirect_user']
      conversation.update_context(user_id, 'no_redirect_user', False)
    else:
      next_interaction = interaction['next_interaction']
    return next_interaction

