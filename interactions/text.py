from vendors import chat_api
import conversation


def logic(interaction, message):
    context = conversation.context(message['user_id'])
    interaction_text= interaction['text']
    for key in context:
        key_store = '${' + key + '}'
        if key_store in interaction_text:
            interaction_text = interaction_text.replace(key_store, context[key])

    chat_api.reply(interaction_text, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
