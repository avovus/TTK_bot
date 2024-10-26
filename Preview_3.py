import telebot
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

TOKEN = "8111640966:AAH4GeOlltSX7Qnu0woBD4voyEzLkqNm4b0" # токен менять тут
bot = telebot.TeleBot(TOKEN)

import json
with open("messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

library = ["заключить", "договор", "зайти", "клиент", "телефон", "адрес", "услуга", "подключить"]
library.sort()

# Проверка номера договора (в реальной ситуации это была бы функция доступа к базе данных)
def check_contract_in_db(contract_number):
    return True  # Здесь может быть реальная проверка

async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["Войти как клиент ТТК", "Заключить договор"]]
    await update.message.reply_text(
        "Поздоровайтесь с умным ботом компании ТТК",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
async def request_contract_number(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Введите ваш номер договора:")

# Верификация номера договора
async def verify_contract(update: Update, context: CallbackContext) -> None:
    contract_number = update.message.text
    if check_contract_in_db(contract_number):
        await update.message.reply_text("Идентификация успешна. Добро пожаловать!")
    else:
        await update.message.reply_text("Номер договора не найден. Проверьте номер и попробуйте снова.")

# Обработчик сообщений с намерениями
async def handle_intent(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    if "привет" in message:
        await update.message.reply_text(messages.get("greetings", "Привет!"))
    elif "пока" in message:
        await update.message.reply_text(messages.get("farewell", "До свидания!"))
    elif "тариф" in message:
        await update.message.reply_text(messages.get("tariffs", "Вот тарифы на выбор:"))
    elif "клиент" in message:
        await update.message.reply_text(messages.get("client", "Добро пожаловать!"))
    elif "контракт" in message:
        await update.message.reply_text(messages.get("contract", "Введите данные"))
    # Добавить больше намерений
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_intent))
    app.add_handler(MessageHandler(filters.TEXT, request_contract_number))
    app.run_polling()

if __name__ == '__main__':
    main()
