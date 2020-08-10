# Main logic brain to handle conversations, recieves messages and handles them
from datetime import datetime

import conversation
import interaction
import dialog
import user
import os
import thread
import pending_conversations
from vendors import chat_api
import traceback
import random

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
    try:
        user_id = message['user_id']
        if user.get_user_type(user_id) == 'user':
            set_pending_conversation(message, user_id)
        move_conversation(message)
    except Exception as e:
        print(e)
        exception_flow(message)
        tb = traceback.format_exc()
        print(tb)
    return True

def set_pending_conversation(message, user_id):
    u_p_conversations = pending_conversations.find(user_id, closed = False)
    if u_p_conversations is None or len(u_p_conversations)==0:
        pending_conversation = pending_conversations.create(user_id)
    else:
        pending_conversation = u_p_conversations[0]
        pending_conversations.received_new_messages(user_id)
    pending_conversations.alert_admins_pending(pending_conversation)
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
    if message.get('text').split(' ')[0].lower() == 'blocknewmessagesnow':
        return True
    return False

def get_random_phrase():
    phrases = [
        '*Se me cruzaron los cables!*',
        '*Se me chispoteo!*',
        '*Santos archibugs batman!*'
    ]
    return random.choice(phrases)

def exception_flow(message):
    chat_api.reply(get_random_phrase(), message, False)
    return True

def set_new_user_pre_register(user_id, message):
    card = message['card']
    conversation.update_context(user_id, 'new_user_info_name', card.get('name'))
    conversation.update_context(user_id, 'new_user_info_phone', card.get('phone'))
    conversation.update_context(user_id, 'new_user_info_country', card.get('country'))
    return True

def move_conversation(message):
    # Past interaction actions
    user_id = message.get('user_id')

    # Get where this user was left
    if conversation.is_finished(user_id): return True
    last_message = conversation.find_last_message(user_id)
    # This fixes referencing a conversation with a user we dont have, but good to see why this would happen
    if last_message is None:
        conversation.create(message)
    print(last_message)
    last_interaction_name = last_message.get('interaction_name')
    print(last_interaction_name)
    last_interaction = dialog.get_interaction(last_interaction_name, user_id)

    # Save context if needed
    if 'save_answer_context' in last_interaction:
        save_answer_context(last_interaction, message, user_id)

    if last_interaction.get('save_intent') == 'true':
        utterance_intent = luis_ai.get_label(message['text'])
        conversation.update_context(user_id, 'intent', utterance_intent)

    if attend_new_message(message) == True and user.get_user_type(user_id) == 'agent':
        next_interaction_name = 'attend_new_message'
    elif 'card' in message and user.get_user_type(user_id) == 'agent':
        set_new_user_pre_register(user_id, message)
        next_interaction_name = 'register_user'
    else:
        next_interaction_name = interaction.get_next_interaction_name(last_interaction, message)
    print(next_interaction_name)

    next_interaction = dialog.get_interaction(next_interaction_name, user_id)
    interaction.run_interaction(next_interaction, message)
    conversation.update(next_interaction, next_interaction_name, message)

    if next_interaction.get('requires_user_response') == 'false':
        if attend_new_message(message) != 'p':
            message['text'] = 'done'
        if 'card' in message: del message['card']
        move_conversation(message)
    if next_interaction.get('finishes_conversation') == 'true': conversation.set_finished(user_id)
    if 'save_field_context' in next_interaction: save_field_context(next_interaction, message, user_id)
    if next_interaction.get('create_thread') == 'true':
        thread_label = conversation.context(user_id).get('intent')
        first_message_id = conversation.get_canonical_user_message(user_id, 0)
        last_message_id = conversation.get_canonical_user_message(user_id, -1)
        thread.create(user_id, first_message_id, None, None, 'arbi')
    return True
