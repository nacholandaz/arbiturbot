# Main logic brain to handle conversations, recieves messages and handles them
from datetime import datetime

import conversation
import interaction
import dialog
import user
import os
import thread

def recieve_message(message):
    move_conversation(message)
    return True


def save_context(last_interaction, message, user_id):
    print(message)
    field = last_interaction.get('save_answer_context')
    text = message['text']
    conversation.update_context(user_id, field, text)
    return True

def move_conversation(message):
    # Past interaction actions
    user_id = message.get('user_id')
    if conversation.is_finished(user_id): return True
    last_message = conversation.find_last_message(user_id)
    print(last_message)
    last_interaction_name = last_message.get('interaction_name')
    print(last_interaction_name)
    last_interaction = dialog.get_interaction(last_interaction_name, user_id)
    if 'save_answer_context' in last_interaction:
        save_context(last_interaction, message, user_id)

    # Next interaction action
    next_interaction_name = interaction.get_next_interaction_name(last_interaction, message)
    print(next_interaction_name)
    next_interaction = dialog.get_interaction(next_interaction_name, user_id)
    interaction.run_interaction(next_interaction, message)
    conversation.update(next_interaction, next_interaction_name, message)
    if 'requires_user_response' in next_interaction:
        if next_interaction['requires_user_response'] == 'false':
            recieve_message(message)
    if 'finishes_conversation' in next_interaction:
        if next_interaction['finishes_conversation'] == 'true':
            conversation.set_finished(user_id)
    if 'create_thread' in next_interaction:
        if next_interaction['create_thread'] == 'true':
            message_id = conversation.get_last_canonical_message_id(user_id)
            thread.create(user_id, message_id)
    return True
