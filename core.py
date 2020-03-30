# Main logic brain to handle conversations, recieves messages and handles them
from datetime import datetime

import conversation
import interaction
import dialog

def recieve_message(message):
    user_id = message.get('user_id')
    if conversation.find_user(message) is None: create_conversation(message)
    move_conversation(message)
    return True

def create_conversation(message): conversation.create(message)

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
    last_interaction = dialog.get_interaction(last_interaction_name)
    if 'save_answer_context' in last_interaction:
        save_context(last_interaction, message, user_id)

    # Next interaction action
    next_interaction_name = interaction.get_next_interaction_name(last_interaction, message)
    print(next_interaction_name)
    next_interaction = dialog.get_interaction(next_interaction_name)
    interaction.run_interaction(next_interaction, message)
    conversation.update(next_interaction, next_interaction_name, message)
    if 'requires_user_response' in next_interaction:
        if next_interaction['requires_user_response'] == 'false': recieve_message(message)
    if 'finishes_conversation' in next_interaction:
        if next_interaction['finishes_conversation'] == 'true':
            conversation.set_finished(user_id)
    return True
