from vendors import sheets
import conversation

def logic(interaction, message): 
    user_id = message.get('user_id')
    context = conversation.context(user_id)
    sheets.insert_row(context)
    return True

def get_next_interaction(interaction, message): 
    return interaction['next_interaction']