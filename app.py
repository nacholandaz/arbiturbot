from dotenv import load_dotenv
load_dotenv()

# This is the message handler from the server
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import core
import os
import user
import conversation


app = Flask(__name__)

def build_message(user_id, text):
    message = {
        'created_at': datetime.now(),
        'user_id': user_id,
        'text': text,
    }
    return message

def hard_reset(message):
    list(user.users.remove())
    list(conversation.conversations.remove())
    print('LOL RESET!', message)
    return jsonify({'success': 'true'})

@app.route('/')
def index_route():
    return jsonify({'greeting': 'welcome to the arbitrur bot'})


@app.route('/messages', methods=['POST'])
def messages_route():
    data = request.get_json().get('messages')[0]
    text = data.get('body')
    user_id = data.get('author')
    print(data)
    if os.getenv('ARBITRUR_PHONE') in user_id: return jsonify({'success': 'true'})
    message = build_message(user_id, text)
    print(message)

    if message['text'] == 'KABOOM!':
        return hard_reset(message)

    RECIEVER_ID = user.phone_to_id(os.getenv('ARBITRUR_PHONE'))
    if user.get(user_id) is None: user.create(user_id)
    if conversation.find(message) is None: conversation.create(message)
    conversation.update_canonical_conversation(user_id, RECIEVER_ID, text, 'user')
    core.recieve_message(message)
    return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
