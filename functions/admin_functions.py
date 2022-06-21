from controller import bot
from config import ADMIN_ID
import datetime
from logger_app import get_logger

# Configure logging
logger = get_logger(__name__)


def send_message_to_admin(message, step, info=''):
    try:
        mess_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        if step == 1:
            mess = f'[{mess_time}] - Заявка на установку игры ' \
                   f'<b>"{message.text}</b>" от {message.from_user.first_name} - <b>[{message.from_user.id}]</b>'
            bot.send_message(ADMIN_ID, mess, parse_mode='html')
            return 1
        if step == 2:
            mess = f'[{mess_time}] - Новый пользователь -<b>[{info} - {message.from_user.id}]</b>- добавлен в базу'
            bot.send_message(ADMIN_ID, mess, parse_mode='html')
            return 1
        if step == 3:
            mess = f'Возникла ошибка в боте: \n <b>{info}</b>'
            bot.send_message(ADMIN_ID, mess, parse_mode='html')
    except Exception as ex:
        logger.error(ex)
        return -1
