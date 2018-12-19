from customs_status import exch_status
from settings import TELEGRAM_API_TOKEN, DATABASES
from db.worker import autonotification_list, row_to_dict, add_state, \
    delete_from_notification
from customs_status import  exch_status
import redis
import telebot
import time

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
REDIS = redis.StrictRedis(**DATABASES['REDIS'])
LAST_STATUS = 'ЭТД: завершён транзит'

def notification():
    for row in autonotification_list():
        if REDIS.get(row.cont_id+'customs'):
            current_exch_status = REDIS.get(row.cont_id+'customs')
        else:
            current_exch_status = exch_status(row.cont_id)
            REDIS.set(row.cont_id+'_customs',current_exch_status['msg'])
            REDIS.expire(row.cont_id+'_customs', 585)
        bot.send_message(row.chat_id, current_exch_status['msg'])
        if current_exch_status['status']== LAST_STATUS:
            bot.send_message(row.chat_id, row.cont_id+' - Слежение завершено')
            delete_from_notification(row.cont_id)


# def rw_notification(chat_id, container):
#     msg = tracking.rw_get_one_time(container)
#     if msg == 'wait':
#         return
#     elif msg == 'nf':
#         #        logger.warning('Not found '+chat_id+' - '+container)
#         print('Not found ' + chat_id + ' - ' + container)
#
#     else:
#         row = (chat_id, container, '1')
#         dbworker.delete_cont_from_pool(row)
#         bot.send_message(chat_id, msg)
#
#
# def delay_60sec():
#     while True:
#         try:
#             autonotification_of_pool()
#             time.sleep(60)
#         except Exception as err:
#             print(err)
#            logger.exception('notific delay' + err)

# logging.basicConfig(filename="notific_log.log", level=logging.info)
# logger = logging.getLogger("notification")
# logger.info("Program started")

