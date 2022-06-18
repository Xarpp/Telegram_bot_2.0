import telebot
from config import TOKEN
from db import BotDB

bot = telebot.TeleBot(TOKEN)

# prerequisites
if not TOKEN:
    exit("No token provided")

BotDB = BotDB("authorization.db")
