from controller import bot
from keyboards import user_keyboard
from functions import user_functions
from controller import db
from logger_app import get_logger

# Configure logging
logger = get_logger(__name__)


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
        if correct_data == -1:
            mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
            bot.send_message(message.chat.id, mess, parse_mode='html')
        if correct_data:
            user_id = message.from_user.id
            if user_exists:
                user_login = db.get_user_login(user_id)
                if user_info['login'] != user_login:
                    db.post_change_login(user_id, user_info['login'])
                db.post_user_logged_status(user_id, 1)
            else:
                db.post_add_user(user_id, user_info['login'])
                logger.info(f"A new user - [{user_info['login']}] added in database")
                user_login = db.get_user_login(user_id)
            mess = f'Авторизация успешна, {user_login}!'
            markup = user_keyboard.user_logged_kb()
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неверный логин или пароль', parse_mode='html')


# @bot.message_handler(commands=['login'])
def start_authorization(message):
    try:
        user_info = {'login': '', 'password': ''}
        user_exists = db.get_user_exists(message.from_user.id)
        if user_exists == -1:
            mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
            bot.send_message(message.chat.id, mess, parse_mode='html')
            return -1
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
    except Exception as ex:
        logger.error(ex)
        mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
        bot.send_message(message.chat.id, mess, parse_mode='html')


# @bot.message_handler(commands=['logout'])
def logout_user(message):
    try:
        user_id = message.from_user.id
        db.post_user_logged_status(user_id, 0)
        mess = 'Вы вышли из аккаунта'
        markup = user_keyboard.start_kb()
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    except Exception as ex:
        logger.error(ex)
        mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
        bot.send_message(message.chat.id, mess, parse_mode='html')


# @bot.message_handler(commands=['back'])
def back_button(message):
    mess = 'Общие функции'
    markup = user_keyboard.start_kb()
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


# @bot.message_handler(commands=['balance'])
def user_balance(message):
    try:
        user_id = message.from_user.id
        user_exists = db.get_user_exists(user_id)
        user_logged = db.get_user_logged_status(user_id)
        if user_exists * user_logged == 0:
            mess = 'Для продолжения необходимо авторизоваться.'
            bot.send_message(message.chat.id, mess, parse_mode='html')
        else:
            user_login = db.get_user_login(user_id)
            mess = user_functions.get_user_balance(user_login)
            bot.send_message(message.chat.id, mess, parse_mode='html')
    except Exception as ex:
        logger.error(ex)
        mess = 'Ой! Кажется что-то сломалось, повторите попытку позже...'
        bot.send_message(message.chat.id, mess, parse_mode='html')


def register_handlers_client():
    bot.register_message_handler(start_authorization, commands=['login'])
    bot.register_message_handler(logout_user, commands=['logout'])
    bot.register_message_handler(back_button, commands=['back'])
    bot.register_message_handler(user_balance, commands=['balance'])
