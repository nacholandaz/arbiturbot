from vendors import chat_api
import notification
import conversation
import user

def logic(interaction, message):

    user_id = message.get('user_id')
    user_context = conversation.context(user_id)
    current_user_id = user_context.get('redirect_user')

    if current_user_id is not None:
      current_user_name = user_context['redirect_name']
      current_user_phone = user_context['redirect_phone']
      notification.create(user_id, current_user_id, 0, settings = {'minutes': 5})
      reply_text = 'Acabas de poner un timer de 5 min con en tu (conversación) con {current_user_name} ({current_user_phone})'
      chat_api.reply(reply_text, message)

    new_message_user = user_context.get('last_message_user')
    user_new_message = user.get(new_message_user)

    if user_new_message.get('owner') is None:
      user.update('owner', user_id)

    if new_message_user is None:
      chat_api.reply('Falle en encontrar el usuario para hablar', message)
      return True

    new_message_name = user_context['last_message_name']
    new_message_phone = user_context['last_message_phone']

    conversation.update_context(user_id, 'redirect_user', new_message_user)
    conversation.update_context(user_id, 'redirect_name', new_message_name)
    conversation.update_context(user_id, 'redirect_phone', new_message_phone)
    conversation.update_context(user_id, 'conversational_level', 'user')


    return True

def get_next_interaction(interaction, message):
    return interaction['next_interaction']
