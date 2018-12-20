import telebot
from settings import TELEGRAM_API_TOKEN
from telebot import types
from db.worker import user_permission
from db.models import UserInfo

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
ACCESS = 10
NOT_REGISTRED = 0
BAN = -5
WAITING = 5
BUTTONS = ['Статус', 'Отслеживание']
YES_NO = ['Да', 'Нет']



class User:
    def __init__(self, nickname):
        self.id = id
        self.nickname = None
        self.firm = None
        self.name = None
        self.email = None

    def check_permissions(self, message):
        permission = user_permission(self.nickname)
        if permission == UserInfo.ACCESS:
            bot.send_message(message.chat.id,
                             'Вы загеристрированный пользователь'
                             )
        elif permission == UserInfo.NOT_REGISTRED:
            bot.send_message(message.chat.id,
                             'Вы не зарегистрированный пользователь'
                             )
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in YES_NO])
            bot.send_message(message.chat.id,
                             'Согласны ли вы на регистрацию?',
                             reply_markup=keyboard
                             )
            pass
        elif permission < UserInfo.BAN:
            bot.send_message(message.chat.id,
                             'Доступ запрещен'
                             )
        else:
            bot.send_message(message.chat.id,
                             'Выша заявка рассматривается'
                             )

    def welcome_message(self, message):
        bot.send_message(message.chat.id,
                         str(message.from_user.first_name) + ', Здравствуйте!')
        bot.send_message(message.chat.id, 'Я приветствует Вас!')


@bot.message_handler(commands=['start'])
def start(message):
    user = User(message.from_user.id)
    user.welcome_message(message)
    user.check_permissions(message)

@bot.message_handler(content_types=["text"])
def make_action(message):
    if message.text in BUTTONS:
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(*[types.KeyboardButton(button) for button in BUTTONS])
        bot.send_message(message.chat.id,
                         'Выберите действие',
                         reply_markup=keyboard
                         )
        #####bot NEXT STEP

