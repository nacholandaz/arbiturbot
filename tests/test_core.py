import os
import sys
from datetime import datetime
sys.path.append(".")
import core
import conversation

message_example = {
    'created_at': datetime.now(),
    'user_id': "528117649489@c.us",
    'text': "Ricardo Alanis",
}

message_p = {
    'created_at': datetime.now(),
    'user_id': "528117649489@c.us",
    'text': "p",
}

message_p_falsy = {
    'created_at': datetime.now(),
    'user_id': "528117649489@c.us",
    'text': "p Ricardo",
}


interaction_persists = {
    'type': 'text',
    'text': 'Excelente. Cual es tu nombre?',
    'requires_user_response': 'true',
    'next_interaction': 'close_conversation_name',
    'save_answer_context': 'name',
}

interaction_field_context = {
    'type': 'text',
    'text': 'Excelente. Cual es tu nombre?',
    'requires_user_response': 'true',
    'next_interaction': 'close_conversation_name',
    'save_field_context': {
        'field': 'name',
        'value': 'Ricardo Alanis'
    },
}


def mock_move_conversation(message):
    mock_move_conversation.has_been_called = True
    mock_move_conversation.params = [message]
    return True
mock_move_conversation.has_been_called = False
mock_move_conversation.params = []


def mock_update_context(user_id, field, text):
    mock_update_context.has_been_called = True
    mock_update_context.params = [user_id, field, text]
    return True
mock_update_context.has_been_called = False
mock_update_context.params = []


# When message is received, move the conversation forward
def test_recieve_message(mocker):
    mock_move_conversation.has_been_called = False
    mock_move_conversation.params = []
    mocker.patch("core.move_conversation", side_effect=mock_move_conversation)
    result = core.recieve_message(message_example)
    assert mock_move_conversation.has_been_called == True and \
            len(mock_move_conversation.params) == len([message_example])


# When interaction contains save_answer_context, save to context the given text by user
def test_save_answer_context(mocker):
    mock_update_context.has_been_called = False
    mock_update_context.params = []
    user_id = message_example['user_id']
    mocker.patch("conversation.update_context", side_effect=mock_update_context)
    field = interaction_persists['save_answer_context']
    text = message_example['text']
    result = core.save_answer_context(interaction_persists, message_example, user_id)
    assert mock_update_context.has_been_called == True and \
            set(mock_update_context.params) == set([user_id, field, text])


# When interaction contains save_field_context, save to context the given values
def test_save_field_context(mocker):
    mock_update_context.has_been_called = False
    mock_update_context.params = []
    user_id = message_example['user_id']
    mocker.patch("conversation.update_context", side_effect=mock_update_context)
    field = interaction_field_context['save_field_context'].get('field')
    value = interaction_field_context['save_field_context'].get('value')
    result = core.save_field_context(interaction_field_context, message_example, user_id)
    assert mock_update_context.has_been_called == True and \
            set(mock_update_context.params) == set([user_id, field, value])


# When text recieved is p, attend new message should be True
def test_attend_new_message_true(mocker):
    result = core.attend_new_message(message_p)
    assert result == True

# When text recieved does not contain p, attend new message should be False
def test_attend_new_message_false(mocker):
    result = core.attend_new_message(message_example)
    assert result == False

# When text recieved starts with p but other text is given, attend new message should be False
def test_attend_new_message_false(mocker):
    result = core.attend_new_message(message_p_falsy)
    assert result == False
