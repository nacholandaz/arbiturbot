from vendors import chat_api
from interactions import list_users, list_cases, list_pending_conversations
import user
import thread
import conversation

def logic(interaction, message):
    ls_type = message['text'].split(' ')[1]
    if ls_type == 'u':
      list_users.logic(interaction, message)
    elif ls_type == 'c':
      list_cases.logic(interaction, message)
    elif ls_type == 'p':
      list_pending_conversations.logic(interaction, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
