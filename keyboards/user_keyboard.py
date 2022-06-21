from telebot import types


def start_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    free_host = types.KeyboardButton('Свободные ПК')
    stock = types.KeyboardButton('Акции')
    website = types.InlineKeyboardButton('Сайт клуба')
    group_vk = types.InlineKeyboardButton('Группа VK')
    help_user = types.InlineKeyboardButton('Помощь')
    check_login = types.InlineKeyboardButton('Войти')
    support_button = types.InlineKeyboardButton('Поддержка')
    games = types.InlineKeyboardButton('Игры')
    markup.add(free_host, stock, website, group_vk, games, check_login, help_user, support_button)
    return markup


def user_logged_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    free_host = types.KeyboardButton('Свободные ПК')
    balance = types.KeyboardButton('Баланс')
    back_button = types.KeyboardButton('Назад')
    logout = types.KeyboardButton('Выйти')
    markup.add(free_host, balance, logout, back_button)
    return markup
