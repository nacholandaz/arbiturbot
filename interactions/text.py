import send

def logic(interaction, message): 
    send.reply(interaction['text'], message)
    return True

def get_next_interaction(interaction, message): 
    return interaction['next_interaction']