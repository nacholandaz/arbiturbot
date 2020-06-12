from vendors import chat_api
import conversation
import user

def logic(interaction, message):
    user_id = message['user_id']
    text = message['text']
    user_context = conversation.context(user_id)
    redirect_user = user_context['redirect_user']
    redirect_name = user_context['redirect_name']
    redirect_phone = user_context['redirect_phone']
    message_redirect = { 'user_id': redirect_user}
    if len(text.split(' '))<=1:
        chat_api.reply('Asegurate de agregar un texto que enviar', {'user_id': user_id})
        return True
    message_text = ' '.join(text.split(' ')[1:])
    print(message_text, message_redirect)
    chat_api.reply(message_text, message_redirect)
    redirect_message = f"Mensage enviado a {redirect_name} ({redirect_phone})"
    chat_api.reply(redirect_message, {'user_id': user_id})
    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']


