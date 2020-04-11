from vendors import chat_api
import conversation
import user

def logic(interaction, message):
    return True

def get_next_interaction(interaction, message):
    user_id = message['user_id']
    text = message['text']
    if message['text'] == interaction['quit_keyword']:
      return interaction['next_interaction_when_exit']

    user_context = conversation.context(user_id)
    redirect_user = user_context['redirect_user']
    message_redirect = { 'user_id': redirect_user}
    message_text = text.replace('m=','')
    print(message_text, message_redirect)
    chat_api.reply(message_text, message_redirect)
    chat_api.reply('Mensaje Enviado', {'user_id': user_id})
    return interaction['interaction_name']


