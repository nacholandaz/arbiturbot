from vendors import chat_api
import conversation

def logic(interaction, message):
    return True

def get_next_interaction(interaction, message):
    user_id = message['user_id']
    context_variable = interaction['context_variable']
    if_value = interaction['if_value']
    context_value_current = conversation.context(user_id).get(context_variable)
    if context_value_current == if_value: return interaction['true_next_interaction']
    return interaction['false_next_interaction']
