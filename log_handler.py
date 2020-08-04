# Interacts with the database to follow conversations
from pymongo import MongoClient
from datetime import datetime
from operator import itemgetter
import os
from vendors import chat_api

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
logs = client.bot.logs
message_logs = client.bot.message_logs
print(os.getenv('ARBITRUR_MONGO_URL'))

def create(conversation_log):

    log = {
        'conversation_log': conversation_log,
        'created_at': datetime.now(),
    }

    return logs.insert_one(log)


def return_logs(message):
  all_errors = list(logs.find({}))
  for ele in all_errors:
    chat_api.reply('---------',message, False)
    chat_api.reply(ele['created_at'].isoformat(),message, False)
    chat_api.reply(ele['conversation_log'],message, False)
  return True

# Keep track of all sent messages
def insert_message(message):
  return message_logs.insert(message)
