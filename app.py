from dotenv import load_dotenv
load_dotenv()

# This is the message handler from the server
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import core
import os


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
    # TODO(ricalanis): Remove this when we go production
    if os.getenv('ARBITRUR_PHONE') not in author:
        core.recieve_message(message)
    return jsonify({'success': 'true'})

@app.route('/send_message', methods=['POST'])
def send_message():
    phone = request.get_json().get('phone')
    user_id = str(phone) + '@c.us'
    user_id = data.get('chatId')
    text = 'Bot starting conversation message'
    message = build_message(user_id, text)
    core.recieve_message(message)
    return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
