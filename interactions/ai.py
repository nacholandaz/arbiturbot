from vendors import gpt
import send

def logic(interaction, message): 
    gpt_answer = gpt.answer(message['text'])
    send.reply(gpt_answer, message)
    return True

def get_next_interaction(interaction, message): 
    return interaction['next_interaction']