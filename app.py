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
import log_handler
import atexit
from vendors import chat_api

scheduler = BackgroundScheduler()
scheduler.add_job(func=notification.run_notifications, trigger="interval", seconds=60)
scheduler.start()

app = Flask(__name__)


def build_message(user_id, text):
    message = {
        'created_at': datetime.now(),
        'user_id': user_id,
        'text': text,
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
    print(data)
    if os.getenv('ARBITRUR_PHONE') in user_id: return True
    message = build_message(user_id, text)
    print(message)

    if message['text'] == 'KABOOM!':
        hard_reset(message)
        return True

    RECIEVER_ID = user.phone_to_id(os.getenv('ARBITRUR_PHONE'))
    if user.get(user_id) is None: user.create(user_id)
    if conversation.find(message) is None: conversation.create(message)
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
        canonical_convo = conversation.get_printable_conversation(user_id)
        log_handler.create(canonical_convo)
        chat_api.reply(canonical_convo, message, False)
        list(user.users.remove())
        list(conversation.conversations.remove())
        list(notification.notifications.remove())
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
