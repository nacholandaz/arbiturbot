from vendors import chat_api

def logic(interaction, message):
    chat_api.reply(interaction['text'], message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
