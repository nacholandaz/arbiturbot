from pymongo import MongoClient
from datetime import datetime, timedelta
from operator import itemgetter
import os
from geo import get_country_name_and_flag
import user

from vendors import chat_api
from interactions import list_pending_conversations

client = MongoClient(os.getenv('ARBITRUR_MONGO_URL'))
notifications = client.bot.notifications

def create(agent_id, notification_type = 'interval', notification_nature = 'timed', settings = None):
    if settings == None:
      if notification_type == 'interval':
        settings = {
          'minutes': 30,
        }
      elif notification_type == 'set_time':
        settings = {
          'hour': 15,
          'minute': 0
        }

    notification = {
        'agent_id': agent_id,
        'created_at': datetime.now(),
        'last_notification_at': datetime.now(),
        'type': notification_type,
        'nature': notification_nature, # urgent, pending, timed
        'settings': settings,
    }

    return notifications.insert_one(notification)

def requires_notification(notification):
    if notification['type'] == 'interval':
      interval_so_far = datetime.now() - notification['last_notification_at']
      if int(interval_so_far.seconds/60) >= notification['settings']['minutes']:
        return True
    if notification['type'] == 'set_time':
      notification_time = notification['settings']
      n_hour = notification_time['hour']
      n_minute = notification_time['minute']
      corrected_now = datetime.now() - timedelta(hours=5)
      t_hour = corrected_now.hour
      t_minute = corrected_now_now.minute
      if n_hour == t_hour and n_minute == t_minute:
        return True
    return False

def send_notification(agent_id):
    message = {'user_id': agent_id}
    text_alert = f"Hola, este es un recordatorio automatizado de tus conversaciones pendientes"
    chat.api.reply(text_alert, message)
    list_pending_conversations.logic({}, message)
    return True

def notify(notification):
    agent_id = notification['agent_id']
    send_notification(agent_id)
    print(f'({datetime.now().isoformat()}) Alerting user: {agent_id}')
    notifications.find_one_and_update(
        {"_id": notification['_id']},
        {"$set": {'last_notification_at': datetime.now()}},
        upsert=True
      )
    return True


def run_notifications():
    notifications_to_run = list(notifications.find({}))
    print('Running notifications scheduler')
    for pending_notification in notifications_to_run:
      if requires_notification(pending_notification):
        notify(pending_notification)
    print('Succesfully Ran Notifications')
    return True
