# Defines interactions and their internal logic
import interactions.multiple_choice as multiple_choice
import interactions.text as text
import interactions.upload_drive as upload_drive
import interactions.ai as ai
import interactions.new_conversation_alert as new_conversation_alert
import conversation

def get_next_interaction_name(interaction, message):
    interaction_type = interaction.get('type')
    next_interaction_function = {
        'text': text.get_next_interaction,
        'multiple_choice': multiple_choice.get_next_interaction,
        'upload_drive': upload_drive.get_next_interaction,
        'ai': ai.get_next_interaction,
        'new_conversation_alert': new_conversation_alert.get_next_interaction,
    }
    return next_interaction_function[interaction_type](interaction, message)

def run_interaction(interaction, message):
    interaction_type = interaction.get('type')
    logic_function = {
        'text': text.logic,
        'multiple_choice': multiple_choice.logic,
        'upload_drive': upload_drive.logic,
        'ai': ai.logic,
        'new_conversation_alert': new_conversation_alert.logic,
    }
    return logic_function[interaction_type](interaction, message)

def get_values_from_context(interaction, message):
    context = conversation.context(message['user_id'])
    for key in context:
        key_store = '${' + key + '}'
        if key_store in interaction['text']:
            interaction['text'] = interaction['text'].replace(key_store, context[key])
    return interaction
