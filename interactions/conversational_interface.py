from vendors import chat_api
import conversation
import user

def logic(interaction, message):
    #chat_api.reply(interaction['text'], message)
    return True

def get_next_interaction(interaction, message):
    user_id = message['user_id']
    conversation.update_context(user_id, 'command_number', None)
    next_interaction_object = interaction.get('available_commands')
    text = message.get('text')
    options = list(next_interaction_object.keys())
    user_command = text.lower().split(' ')[0]
    numbers_in_command = [s for s in str.split() if s.isdigit()]
    strings_in_command = [s for s in str.split() if not s.isdigit()]

    if len(numbers_in_command)>0:
        command_number = int(''.join(numbers_in_command))
        user_command = strings_in_command + '.'
        conversation.update_context(user_id, 'command_number', command_number)

    for option in options:
        if option == user_command:
          return next_interaction_object[option]
    print('Command not found, default failure route')
    return interaction['next_interaction_failure']
