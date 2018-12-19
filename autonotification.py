from customs_status import exch_status
import telebot
import time

bot = telebot.TeleBot(config.tg_token)


def autonotification_of_pool():
    chat_list = dbworker.chat_list()
    msg_type = 'notific'
    for chat_id in chat_list:
        for container in dbworker.container_list_for_chat(chat_id):
            test_flag = (chat_id[0], container[0])
            flag = dbworker.container_flag(test_flag)
            if flag[0] == 2:
                msg = tracking.exch_status(container[0], msg_type)
                if container[1] != msg[1]:
                    row = (msg[1], chat_id[0], container[0])
                    dbworker.write_new_status(row)
                    bot.send_message(chat_id[0], msg[0])
                    if msg[1] == 'ЭТД: завершён транзит':
                        row = (chat_id[0], container[0], '2')
                        dbworker.delete_cont_from_pool(row)
                        bot.send_message(chat_id[0],
                                         container[0] + ' - Слежение завершено')
            else:
                rw_notification(chat_id[0], container[0])


def rw_notification(chat_id, container):
    msg = tracking.rw_get_one_time(container)
    if msg == 'wait':
        return
    elif msg == 'nf':
        #        logger.warning('Not found '+chat_id+' - '+container)
        print('Not found ' + chat_id + ' - ' + container)

    else:
        row = (chat_id, container, '1')
        dbworker.delete_cont_from_pool(row)
        bot.send_message(chat_id, msg)


def delay_60sec():
    while True:
        try:
            autonotification_of_pool()
            time.sleep(60)
        except Exception as err:
            print(err)
#            logger.exception('notific delay' + err)

# logging.basicConfig(filename="notific_log.log", level=logging.info)
# logger = logging.getLogger("notification")
# logger.info("Program started")

