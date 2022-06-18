from telebot import types


def start_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    free_host = types.KeyboardButton('Свободные ПК')
    stock = types.KeyboardButton('Акции')
    website = types.InlineKeyboardButton('Сайт клуба')
    group_vk = types.InlineKeyboardButton('Группа VK')
    help_user = types.InlineKeyboardButton('Помощь')
    authorization = types.InlineKeyboardButton('Авторизация')
    markup.add(free_host, stock, website, group_vk, authorization, help_user)
    return markup


def user_logged_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    free_host = types.KeyboardButton('Свободные ПК')
    go_back = types.KeyboardButton('Назад')
    balance = types.KeyboardButton('Баланс')
    logout = types.KeyboardButton('Выйти')
    markup.add(free_host, balance, go_back, logout)
    return markup
