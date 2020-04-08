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

@app.route('/messages', methods=['POST'])
def index():
    data = request.get_json().get('messages')[0]
    user_id = data.get('chatId')
    text = data.get('body')
    author = data.get('author')
    message = build_message(user_id, text)
    print(message)
    RECIEVER_ID = user.phone_to_id(os.getenv('ARBITRUR_PHONE'))
    if user.get(user_id) is None: user.create(user_id)
    if conversation.find(message) is None: conversation.create(message)
    conversation.update_canonical_conversation(user_id, RECIEVER_ID, text, 'user')
    # TODO(ricalanis): Remove this when we go production
    if os.getenv('ARBITRUR_PHONE') not in author:
        core.recieve_message(message)
    return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
