from vendors import chat_api

def logic(interaction, message):
    chat_api.reply(interaction['text'], message)
    return True

def get_next_interaction(interaction, message):
    next_interaction_object = interaction.get('available_commands')
    text = message.get('text')
    options = list(next_interaction_object.keys())
    for option in options:
        if option == text.lower().split(' ')[0]:
          return next_interaction_object[option]
    print('Command not found, default failure route')
    return interaction['next_interaction_failure']
