import logging
from controller import bot
import handler

# Configure logging
logging.basicConfig(level=logging.INFO)

handler.register_handlers_client()
handler.register_handlers_admin()
handler.register_handlers_other()


if __name__ == '__main__':
    bot.polling(none_stop=True)
