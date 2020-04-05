from vendors import gpt
from vendors import chat_api

def logic(interaction, message):
    gpt_answer = gpt.answer(message['text'])
    chat_api.reply(gpt_answer, message)
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
