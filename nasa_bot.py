from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
import sqlite3

def get_db():
    connect = sqlite3.connect('../../../nasa/nasa.sqlite')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM satellites")
    result = cursor.fetchall()
    connect.close
    return result

database = get_db()

vagabond_table = ""

for row in database:
    nasa_text = str(row[0]) + ". Название: " + str(row[1]) + ". Производитель: " + str(row[2]) + "\n"
    nasa_table += nasa_text

print(nasa_table)

# Объявление переменной бота
bot = TeleBot(settings.BOT_KEY_KAMILA, threaded=False)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Добрый день! Вы запустили бот NASA. Посмотреть список команд: /help.
""")

@bot.message_handler(commands=['help'])
    bot.reply_to(message, """\
/view - узнать список спутников NASA
""")

@bot.message_handler(commands=['view'])
def view(message):
    bot.reply_to(message, str(nasa_table))

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling() 