# Main logic brain to handle conversations, recieves messages and handles them
from datetime import datetime

import conversation
import interaction
import dialog
import user
import os
import thread

from vendors import luis_ai

def recieve_message(message):
    """
    Caller function to start moving conversation.

    Parameters
    ----------
    message : dictionary
        Message information recieved from the API.

    Attributes
    ----------
    None

    Methods
    -------
    None
    """
    move_conversation(message)
    return True


def save_answer_context(last_interaction, message, user_id):
    print(message)
    field = last_interaction.get('save_answer_context')
    text = message['text']
    conversation.update_context(user_id, field, text)
    return True

def save_field_context(next_interaction, message, user_id):
    field_data = next_interaction.get('save_field_context')
    conversation.update_context(user_id, field_data.get('field'), field_data.get('value'))
    return True

def attend_new_message(message):
    if message.get('text').split(' ')[0] == 'p' and len(message.get('text')) == 1:
        return True
    return False

def move_conversation(message):
    # Past interaction actions
    user_id = message.get('user_id')
    if conversation.is_finished(user_id): return True
    last_message = conversation.find_last_message(user_id)
    print(last_message)
    last_interaction_name = last_message.get('interaction_name')
    print(last_interaction_name)
    last_interaction = dialog.get_interaction(last_interaction_name, user_id)

    if 'save_answer_context' in last_interaction: save_answer_context(last_interaction, message, user_id)
    if last_interaction.get('save_intent') == 'true':
        utterance_intent = luis_ai.get_label(message['text'])
        conversation.update_context(user_id, 'intent', utterance_intent)
    if attend_new_message(message) == True and user.get_user_type(user_id) == 'agent':
        next_interaction_name = 'attend_new_message'
    else:
        next_interaction_name = interaction.get_next_interaction_name(last_interaction, message)
    print(next_interaction_name)

    next_interaction = dialog.get_interaction(next_interaction_name, user_id)
    interaction.run_interaction(next_interaction, message)
    conversation.update(next_interaction, next_interaction_name, message)

    if next_interaction.get('requires_user_response') == 'false':
        if attend_new_message(message) != 'p':
            message['text'] = 'done'
        recieve_message(message)
    if next_interaction.get('finishes_conversation') == 'true': conversation.set_finished(user_id)
    if 'save_field_context' in next_interaction: save_field_context(next_interaction, message, user_id)
    if next_interaction.get('create_thread') == 'true':
        thread_label = conversation.context(user_id).get('intent')
        message_id = conversation.get_last_canonical_message_id(user_id)
        thread.create(user_id, message_id, thread_label)
    return True
