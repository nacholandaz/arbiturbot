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
    if last_interaction.get('save_answer_context') == 'true': save_context(last_interaction, message, user_id)
    if last_interaction.get('save_intent') == 'true':
        utterance_intent = luis_ai.get_label(message['text'])
        conversation.update_context(user_id, 'intent', utterance_intent)
    # Next interaction action
    next_interaction_name = interaction.get_next_interaction_name(last_interaction, message)
    print(next_interaction_name)
    next_interaction = dialog.get_interaction(next_interaction_name, user_id)
    interaction.run_interaction(next_interaction, message)
    conversation.update(next_interaction, next_interaction_name, message)
    if next_interaction.get('requires_user_response') == 'false': recieve_message(message)
    if next_interaction.get('finishes_conversation') == 'true': conversation.set_finished(user_id)
    if next_interaction.get('create_thread') == 'true':
        thread_label = conversation.context(user_id).get('intent')
        message_id = conversation.get_last_canonical_message_id(user_id)
        thread.create(user_id, message_id, thread_label)
    return True
