from controller import bot
import handler
import time
from logger_app import get_logger

# Configure logging
logger = get_logger(__name__)

handler.register_handlers_client()
handler.register_handlers_admin()
handler.register_handlers_other()


def main():
    try:
        logger.info('Bot starting...')
        bot.polling(none_stop=True)
    except Exception as ex:
        logger.exception(ex)
        logger.warning('Bot start failed, try restart...')
        time.sleep(5)
        main()


if __name__ == '__main__':
    main()
