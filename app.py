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
import atexit

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
    conversation.update_canonical_conversation(user_id, RECIEVER_ID, text, 'user')
    print('Moving Convo')
    core.recieve_message(message)
    return True


@app.route('/', methods=['GET','POST'])
def index_route():
    return jsonify({'greeting': 'welcome to the arbitrur bot'})

@app.route('/messages', methods=['GET','POST'])
def messages_route():
    os.environ['CLI_ON'] = "0"
    data = request.get_json().get('messages')[0]
    respond(data)
    return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

atexit.register(lambda: scheduler.shutdown())
