from settings import TELEGRAM_API_TOKEN, DATABASES
from db.worker import autonotification_list, delete_from_notification
from customs_status import exch_status
from datetime import datetime
import redis
import telebot
import time

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
LAST_STATUS = 'ЭТД: завершён транзит'
last_location_time = datetime.now()


def customs_notification(notification_list):
    for row in notification_list:
        if REDIS.get(row.cont_id + 'customs'):
            current_exch_status = REDIS.get(row.cont_id + 'customs')
        else:
            current_exch_status = exch_status(row.cont_id)
            REDIS.set(row.cont_id + '_customs', current_exch_status['msg'])
            REDIS.expire(row.cont_id + '_customs', 585)
        bot.send_message(row.chat_id, current_exch_status['msg'])
        if current_exch_status['status'] == LAST_STATUS:
            bot.send_message(row.chat_id, row.cont_id + ' - Слежение завершено')
            delete_from_notification(row.cont_id)


def location_notification(notification_list):
    for row in notification_list:
        current_location = REDIS.hgetall(row.cont_id)
        msg = '{} - temperature= {}, lat= {}, lng={}'.format(
            current_location['cont_id'],
            current_location['temperature'],
            current_location['longitude'],
            current_location['latitude']
        )
        bot.send_message(row.chat_id, msg)


if __name__ == "__main__":
    REDIS = redis.StrictRedis(**DATABASES['REDIS'])
    while True:
        list_from_db = autonotification_list()
        customs_notification(list_from_db)
        current_time = datetime.now()
        if current_time.hour - last_location_time.hour >= 12:
            location_notification(list_from_db)
            last_location_time = datetime.now()
        time.sleep(600)
