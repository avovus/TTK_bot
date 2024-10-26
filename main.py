
import yandex_speech
from pip._internal.cli.cmdoptions import python
import telebot

TOKEN = "7579877505:AAGpMjFpSAtXzIi59ocaC7DP6I24RHE8J5c"
bot = telebot.TeleBot(TOKEN)

import json
with open("messages.json", "r") as file:
    messages = json.load(file)

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler

def request_contract_number(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введите ваш номер договора:")
    
def verify_contract(update: Update, context: CallbackContext) -> None:
    contract_number = update.message.text
    if check_contract_in_db(contract_number):
        update.message.reply_text("Идентификация успешна. Добро пожаловать!")
    else:
        update.message.reply_text("Номер договора не найден. Проверьте номер и попробуйте снова.")

def check_contract_in_db(contract_number):
    # Здесь будет логика обращения к базе данных
    return True  # или False в зависимости от проверки

from telegram import ReplyKeyboardMarkup

def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["Войти как клиент ТТК", "Заключить договор"]]
    update.message.reply_text(
        "Выберите действие:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

def handle_intent(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    if "привет" in message:
        update.message.reply_text(messages["greetings"])
    elif "пока" in message:
        update.message.reply_text(messages["farewell"])
    # Добавить сюда ещё намерений

#from yandex_speech import Speech

def voice_to_text(audio_file_path):
    speech = Speech("your_yandex_api_key")
    speech.recognize(audio_file_path)
    return speech.response_text

updater = Updater("7579877505:AAGpMjFpSAtXzIi59ocaC7DP6I24RHE8J5c") # Это наш токен

updater.start_webhook(
    listen="46.16.36.160", #Сюда вместо нуля вписать IP-Адресс VPS`ки
    port=3306,#Её порт
    url_path="7579877505:AAGpMjFpSAtXzIi59ocaC7DP6I24RHE8J5c"# Это наш токен
)

updater.bot.setWebhook("http://46.16.36.160/phpmyadmin/index.php?route=/database/structure&server=1&db=telegram_bot/7579877505:AAGpMjFpSAtXzIi59ocaC7DP6I24RHE8J5c")# Ссылка на домен с токеном

