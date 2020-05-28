# ARBITRURBOT

A service oriented intelligent engine to provide a chat interface to costumer management.

## Setup

* Install docker and docker-compose
* Create environment file .env
```
SPREAD_URL={if this is to connect to a spreadsheet, insert url here}
GPT_URL=https://transformer.huggingface.co/autocomplete/gpt
ARBITRUR_PHONE={phone number format: 8111231234}
ARBITRUR_MONGO_URL={from cluster url https://www.mongodb.com/, make sure to setup networking access and username}
CHAT_TOKEN={from chat-api.com}
CLI_ON=0 // 1 for CLI Mode
LUIS_AI_ID={from luis.ai, setup intelligence with two modes: report/sale}
LUIS_AI_KEY={from luis.ai}

```

root directory should also include `credentials.json` file (https://cran.r-project.org/web/packages/gargle/vignettes/get-api-credentials.html follow "OAuth client ID and secret" guide in that site for that)

* run docker-compose build

## Start server

* Run ngrok locally (https://ngrok.com/) using `ngrok http 5000`
* Setup ngrok manually using a function of type, using a function like:
```python
def set_webhook():
    meta_chat = {
        "set": True,
        "webhookUrl": '(local ngrok url)'
    }
    return requests.post('https://api.chat-api.com/instance99459/webhook?token=(chat_api_token)', data=meta_chat).json()
```
* run docker-compose up (-d if daemon)

## Run terminal client
* run docker-compose run web python3 cli.py

This will run the terminal client. It will ask if the database should be clear after using the client.
Keep in mind that if you use the configuration given that points to atlas, this could delete all information
stored.


## Run tests

```
docker-compose run web pytest
```

### Example objects on database

#### Example conversation object
```python
{'_id': ObjectId('5e938eee9b41d7afbc3d4cd4'),
 'user_id': '5218186861502@c.us',
 'messages': [{'sender': 'user',
   'message': {'created_at': datetime.datetime(2020, 4, 12, 16, 58, 3, 234000),
    'user_id': '5218186861502@c.us',
    'text': 'Hola'},
   'type': 'user_utterance',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 3, 234000),
   'interaction_name': 'initial_user_message'},
  {'sender': 'bot',
   'message': {'created_at': datetime.datetime(2020, 4, 12, 16, 58, 3, 234000),
    'user_id': '5218186861502@c.us',
    'text': 'Hola'},
   'type': 'bot_response',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 8, 275000),
   'interaction_name': 'start'},
  {'sender': 'bot',
   'message': {'created_at': datetime.datetime(2020, 4, 12, 16, 58, 3, 234000),
    'user_id': '5218186861502@c.us',
    'text': 'Hola'},
   'type': 'bot_response',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 9, 554000),
   'interaction_name': 'what_name'},
  {'sender': 'bot',
   'message': {'created_at': datetime.datetime(2020, 4, 12, 16, 58, 13, 439000),
    'user_id': '5218186861502@c.us',
    'text': 'Ric'},
   'type': 'bot_response',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 16, 458000),
   'interaction_name': 'finish_conversation'},
  {'sender': 'bot',
   'message': {'created_at': datetime.datetime(2020, 4, 12, 16, 58, 13, 439000),
    'user_id': '5218186861502@c.us',
    'text': 'Ric'},
   'type': 'bot_response',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 25, 484000),
   'interaction_name': 'alert_conversation'}],
 'canonical_conversation': [{'sender_type': 'user',
   'sender_id': '5218186861502@c.us',
   'reciever_id': '5218118283133@c.us',
   'text': 'Hola',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 6, 969000)},
  {'sender_type': 'bot',
   'sender_id': '5218118283133@c.us',
   'reciever_id': '5218186861502@c.us',
   'text': 'Bienvenid@!',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 8, 223000)},
  {'sender_type': 'bot',
   'sender_id': '5218118283133@c.us',
   'reciever_id': '5218186861502@c.us',
   'text': 'Cuál es tu nombre?',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 9, 504000)},
  {'sender_type': 'user',
   'sender_id': '5218186861502@c.us',
   'reciever_id': '5218118283133@c.us',
   'text': 'Ric',
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 13, 579000)},
  {'sender_type': 'bot',
   'sender_id': '5218118283133@c.us',
   'reciever_id': '5218186861502@c.us',
   'text': "Ok, dame un segundo...'",
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 16, 398000)}],
 'context': {},
 'finished': 'true'}
```

#### Example User object
```python
{'_id': ObjectId('5e938eee9b41d7afbc3d4cd3'),
 'id': '5218186861502@c.us',
 'source': 'inbound',
 'type': 'user',
 'name': 'Ric',
 'uuid': 'inbound_61502',
 'phone': '5218186861502',
 'country': '🇲🇽MX',
 'created_at': datetime.datetime(2020, 4, 12, 16, 58, 6, 102000),
 'owners': [],
 'context': {},
 'threads': [{'label': None,
   'first_canonical_message_id': None,
   'last_canonical_message_id': 4,
   'solved': False,
   'created_at': datetime.datetime(2020, 4, 12, 16, 58, 25, 629000),
   'updated_at': datetime.datetime(2020, 4, 12, 16, 58, 25, 629000)}]}
```

### Example Notification Object
```python
[{'_id': ObjectId('5e93e56ccf39f61f8b2bf0e9'),
  'agent_id': '5218117649489@c.us',
  'user_id': '5218186861502@c.us',
  'thread_id': 0,
  'created_at': datetime.datetime(2020, 4, 12, 23, 7, 8, 639000),
  'last_notification_at': datetime.datetime(2020, 4, 13, 4, 18, 54, 449000),
  'type': 'interval',
  'settings': {'minutes': 30}}]
```
