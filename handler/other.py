from controller import bot
from telebot import types
from keyboards import user_keyboard
from functions import user_functions
from controller import db


# @bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>, это тестовый бот 2.0 компьютерного клуба Youplay, ' \
           f'нажми /help, чтобы узнать что я умею.'
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
    if mess == -1:
        mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
    bot.send_message(message.chat.id, mess, parse_mode='html')


# @bot.message_handler(commands=['host'])
def free_host(message):
    mess = user_functions.get_free_hosts()
    if mess == -1:
        mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
    bot.send_message(message.chat.id, mess, parse_mode='html')


def get_userdata_steps(message, step, user_info, user_exists):
    if step == 0:
        mess = bot.send_message(message.chat.id, 'Введите логин:')
        bot.register_next_step_handler(mess, get_userdata_steps, 1, user_info, user_exists)
    elif step == 1:
        user_info['login'] = message.text
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id)
        mess = bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(mess, get_userdata_steps, 2, user_info, user_exists)
    elif step == 2:
        user_info['password'] = message.text
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        correct_data = user_functions.authorization(user_info)
        if correct_data:
            user_id = message.from_user.id
            user_login = db.get_user_login(user_id)
            if user_exists:
                if user_info['login'] != user_login:
                    db.post_change_login(user_id, user_info['login'])
                db.post_user_logged_status(user_id, 1)
            else:
                db.post_add_user(user_id, user_info['login'])
            user_login = db.get_user_login(user_id)
            mess = f'Авторизация успешна, {user_login}!'
            markup = user_keyboard.user_logged_kb()
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неверный логин или пароль', parse_mode='html')


# @bot.message_handler(commands=['login'])
def start_authorization(message):
    user_info = {'login': '', 'password': ''}
    user_exists = db.get_user_exists(message.from_user.id)
    if user_exists:
        user_logged = db.get_user_logged_status(message.from_user.id)
        if user_logged:
            mess = 'Авторизация успешна'
            markup = user_keyboard.user_logged_kb()
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        else:
            get_userdata_steps(message, 0, user_info, user_exists)
    else:
        get_userdata_steps(message, 0, user_info, user_exists)


# @bot.message_handler(commands=['logout'])
def logout_user(message):
    user_id = message.from_user.id
    db.post_user_logged_status(user_id, 0)
    mess = 'Вы вышли из аккаунта'
    markup = user_keyboard.start_kb()
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


# @bot.message_handler(commands=['back'])
def back_button(message):
    mess = 'Общие функции'
    markup = user_keyboard.start_kb()
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


# @bot.message_handler(commands=['balance'])
def user_balance(message):
    user_id = message.from_user.id
    user_login = db.get_user_login(user_id)
    mess = user_functions.get_user_balance(user_login)
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
    bot.register_message_handler(start_authorization, commands=['login'])
    bot.register_message_handler(logout_user, commands=['logout'])
    bot.register_message_handler(back_button, commands=['back'])
    bot.register_message_handler(user_balance, commands=['balance'])
    bot.register_message_handler(support_button, commands=['support'])
    bot.register_message_handler(another_msg)
