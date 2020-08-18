from dotenv import load_dotenv
load_dotenv()

# This is the message handler from the server
from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import core
import os
import user
import conversation
import notification
import pending_conversations
import log_handler
import atexit
from vendors import chat_api
import geo
import user
import sentry_sdk
# Sentry connected to arbi gmail
sentry_sdk.init(os.getenv('SENTRY_URL'))

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=notification.run_notifications, trigger="interval", seconds=60)
scheduler.start()

user.agents()

def build_message(user_id, text, body = None):
    message = {
        'created_at': datetime.now(),
        'user_id': user_id,
        'text': text,
    }
    if body and 'BEGIN:VCARD' in body:
        print('******* Card Found, printing contents: *********')
        print(body)
        print('*******')
        card_info = body
        card_separated = card_info.split('\n')
        user_phone = user.clean_phone(card_separated[3].split(':')[-1])
        message['card'] = {
            'name':card_separated[2].replace('FN:',''),
            'phone': user_phone,
            'country':geo.get_country_name_and_flag(user_phone)
        }
    return message

def hard_reset():
    list(user.users.remove())
    list(conversation.conversations.remove())
    print('<< Conversations reset >>')
    return True

def respond(data):
    print(data)
    text = data.get('body')
    user_id = data.get('author')
    body = data.get('body')
    print(data)
    if os.getenv('ARBITRUR_PHONE') in user_id: return True
    message = build_message(user_id, text, body)
    log_handler.insert_message(message)
    print(message)

    if message['text'] == 'KABOOM!':
        hard_reset(message)
        return True

    RECIEVER_ID = user.phone_to_id(os.getenv('ARBITRUR_PHONE'))

    new_user_phone = data.get('chatId').replace('@c.us','')
    user_data = {
        'name': data.get('senderName'),
        'phone':new_user_phone,
        'country':  geo.get_country_name_and_flag(new_user_phone)
    }
    if user.get(user_id) is None: user.create(user_id, user_data)
    # Demote or promote user if there is a change in the agent list
    user.demote_to_user_if_needed(user_id, user_data)
    user.promote_to_agent_if_needed(user_id, user_data)

    # If we are already handling a message and we are not done, ignore.
    conversation.update_canonical_conversation(user_id, RECIEVER_ID, text, 'user')
    if user.is_bot_answering(user_id) == True: return True
    user.set_user_answering(user_id)
    print('Moving Convo')
    core.recieve_message(message)
    user.remove_user_answering(user_id)
    return True


@app.route('/', methods=['GET','POST'])
def index_route():
    return jsonify({'greeting': 'welcome to the arbitrur bot'})

@app.route('/messages', methods=['GET','POST'])
def messages_route():
    os.environ['CLI_ON'] = "0"
    data = request.get_json().get('messages')[0]
    text = data.get('body')
    user_id = data.get('author')
    message = build_message(user_id, text)

    if text == '//HARDRESET':
        chat_api.reply('Reseteando status...', message, False)
        try:
            canonical_convo = conversation.get_printable_conversation(user_id)
        except:
            canonical_convo = "- Ningún mensaje encontrado"
        log_handler.create(canonical_convo)
        chat_api.reply(canonical_convo, message, False)
        list(user.users.remove())
        list(conversation.conversations.remove())
        list(notification.notifications.remove())
        list(pending_conversations.pending_conversations.remove({}))
        list(user.agents_source.remove({}))
        chat_api.reply('Reseteado',message, False)
        chat_api.reply('*Log creado*', message, False)

    elif text == '//DOCUMENT':
        chat_api.reply('Retornando conversación...', message, False)
        canonical_convo = conversation.get_printable_conversation(user_id)
        chat_api.reply(canonical_convo, message, False)
        log_handler.create(canonical_convo)
        chat_api.reply('*Log creado*', message, False)

    elif text == '//LOGS':
        log_handler.return_logs(message)

    else:
        respond(data)

    return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

atexit.register(lambda: scheduler.shutdown())
