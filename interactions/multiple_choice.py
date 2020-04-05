from vendors import chat_api

from fuzzywuzzy import process

def logic(interaction, message):
    chat_api.reply(interaction['text'], message)
    return True

def get_next_interaction(interaction, message):
    next_interaction_object = interaction.get('next_interaction')
    text = message.get('text')
    options = list(next_interaction_object.keys())
    selected_option_match = process.extractOne(text.lower(), options)
    if selected_option_match[1] > 90:
        return next_interaction_object[selected_option_match[0]]
    print('Option not found, default failure route')
    return interaction['next_interaction_failure']
