from .client import start_authorization, logout_user, back_button, user_balance
from controller import bot
from telebot import types
from keyboards import user_keyboard
from functions import user_functions
from logger_app import get_logger

# Configure logging
logger = get_logger(__name__)


# @bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>, это бот компьютерного клуба <b>YouPlay</b>, ' \
           f'нажми <b>/help</b>, чтобы узнать что я умею.'
    markup = user_keyboard.start_kb()
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


# @bot.message_handler(commands=['help'])
def help_user(message):
    mess = '<b>/host</b> - свободные ПК\n<b>/stock</b> - наши акции\n' \
            '<b>/website</b> - сайт клуба\n<b>/vk</b> - группа vk\n' \
            '<b>/login</b> - войти в аккаунт\n<b>/support</b> - поддержка'
    bot.send_message(message.chat.id, mess, parse_mode='html')


# @bot.message_handler(commands=['VK'])
def group_vk(message):
    btn = types.InlineKeyboardMarkup()
    btn.add(types.InlineKeyboardButton('Перейти в группу', url="https://vk.com/youplay24"))
    bot.send_message(message.chat.id, 'Вступай в группу вк и участвуй в ежедневных розыгрышах!', reply_markup=btn)


# @bot.message_handler(commands=['website'])
def website(message):
    btn = types.InlineKeyboardMarkup()
    btn.add(types.InlineKeyboardButton('Открыть сайт', url="https://youplay24.ru/"))
    bot.send_message(message.chat.id, 'Самые актуальные акции и скидки тут!', reply_markup=btn)


# @bot.message_handler(commands=['stock'])
def stock(message):
    mess = user_functions.stock_parser()
    bot.send_message(message.chat.id, mess, parse_mode='html')


# @bot.message_handler(commands=['host'])
def free_host(message):
    mess = user_functions.get_free_hosts()
    if mess == -1:
        mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
    bot.send_message(message.chat.id, mess, parse_mode='html')


# @bot.message_handler(commands=['support'])
def support_button(message):
    mess = 'Жалобы и предложения по поводу работы бота можно написать <b>@Xarpp_s</b>\n\n' \
            '<b>Разработано специально для клуба YouPlay</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


def another_msg(message):
    mess = 'Я пока не понимаю, что ты пишешь, используй <b>/help</b>, чтобы узнать мои функции.'
    if message.text == 'Помощь':
        help_user(message)
    elif message.text == 'Группа VK':
        group_vk(message)
    elif message.text == 'Сайт клуба':
        website(message)
    elif message.text == 'Свободные ПК':
        free_host(message)
    elif message.text == 'Акции':
        stock(message)
    elif message.text == 'Войти':
        start_authorization(message)
    elif message.text == 'Выйти':
        logout_user(message)
    elif message.text == 'Назад':
        back_button(message)
    elif message.text == 'Баланс':
        user_balance(message)
    elif message.text == 'Поддержка':
        support_button(message)
    else:
        bot.send_message(message.chat.id, mess, parse_mode='html')


def register_handlers_other():
    bot.register_message_handler(start, commands=['start'])
    bot.register_message_handler(help_user, commands=['help'])
    bot.register_message_handler(group_vk, commands=['vk'])
    bot.register_message_handler(website, commands=['website'])
    bot.register_message_handler(stock, commands=['stock'])
    bot.register_message_handler(free_host, commands=['host'])
    bot.register_message_handler(support_button, commands=['support'])
    bot.register_message_handler(another_msg)
