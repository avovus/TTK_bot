import os
import json
import wave

from vosk import Model, KaldiRecognizer
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

c = 0

VALID_CODES = {"516000001", "516000002", "516000003", "516000004", "516000005", "516000006", "516000007", "516000008", "516000009"}
needCheckCode = False
TOKEN = "8111640966:AAH4GeOlltSX7Qnu0woBD4voyEzLkqNm4b0"
model_path = "C://Users//Eden Despoyno//Desktop//vosk-model-ru-0.22" #тут должен быть путь к локальной модели
messages = {}
try:
    model = Model(model_path)
    with open("messages.json", "r", encoding="utf-8") as file:
        messages = json.load(file)
except Exception as e:
    print(f"Ошибка загрузки модели или JSON файла: {e}")
def voice_to_text(audio_file_path):
    try:
        with wave.open(audio_file_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                raise ValueError("Аудио должно быть в формате WAV (Mono PCM)")

            recognizer = KaldiRecognizer(model, wf.getframerate())
            result_text = ""

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result_text += recognizer.Result()
                else:
                    recognizer.PartialResult()

            result_text += recognizer.FinalResult()

        return json.loads(result_text).get("text", "")
    except Exception as e:
        print(f"Ошибка при распознавании текста: {e}")
        return ""


import requests
async def handle_voice_message(update: Update, context: CallbackContext) -> None:
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    voice_file_path = "voice_message.ogg"
    global c
    global needCheckCode
    file_url = voice_file.file_path
    response = requests.get(file_url)
    with open(voice_file_path, "wb") as f:
        f.write(response.content)

    wav_file_path = "voice_message.wav"
    os.system(f"ffmpeg -i {voice_file_path} -ar 16000 -ac 1 {wav_file_path}")
    wav_file_path = "voice_message.wav"
    recognized_text = voice_to_text(wav_file_path)

    message = recognized_text
    if needCheckCode and message in VALID_CODES:
        await update.message.reply_text(messages.get("yescon"))
        needCheckCode = False
    elif needCheckCode and not(message in VALID_CODES):
        await update.message.reply_text(messages.get("nocon"))
        needCheckCode = False
    elif "тариф" in message:
        await update.message.reply_text(messages.get("tariffs", "Вот тарифы на выбор:"))
    elif "клиент" in message:
        await update.message.reply_text(messages.get("client", "Добро пожаловать!"))
    elif "договор" in message:
        await update.message.reply_text(messages.get("contract", "Введите данные"))
        needCheckCode = True
    elif "поддержка" in message:
        await update.message.reply_text(messages.get("hotline", "номера поддержки"))
    elif "привет" in message:
        await update.message.reply_text(messages.get("greetings", "Привет!"))
    elif "пока" in message:
        await update.message.reply_text(messages.get("farewell", "До свидания!"))
    else:
        await update.message.reply_text(messages.get("error", "ошибули"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [["Войти как клиент ТТК", "Заключить договор"]]
    await update.message.reply_text(
        "Поздоровайтесь с умным ботом компании ТТК",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

def check_contract_in_db(contract_number):
    return True

async def request_contract_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите ваш номер договора:")

async def verify_contract(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contract_number = update.message.text
    if check_contract_in_db(contract_number):
        await update.message.reply_text("yescon")
    else:
        await update.message.reply_text("nocon")

async def handle_intent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global needCheckCode
    message = update.message.text.lower()
    if needCheckCode and message in VALID_CODES:
        await update.message.reply_text(messages.get("yescon"))
        needCheckCode = False
    elif needCheckCode and not (message in VALID_CODES):
        await update.message.reply_text(messages.get("nocon"))
        needCheckCode = False
    elif "тариф" in message:
        await update.message.reply_text(messages.get("tariffs", "Вот тарифы на выбор:"))
    elif "услуги" in message:
        await update.message.reply_text(messages.get("services", "Вот список доп. усулг:"))
    elif "клиент" in message:
        await update.message.reply_text(messages.get("client", "Добро пожаловать!"))
    elif "договор" in message:
        await update.message.reply_text(messages.get("contract", "Введите данные"))
        needCheckCode = True
    elif "поддержка" in message:
        await update.message.reply_text(messages.get("hotline", "номера поддержки"))
    elif "привет" in message:
        await update.message.reply_text(messages.get("greetings", "Привет!"))
    elif "пока" in message:
        await update.message.reply_text(messages.get("farewell", "До свидания!"))
    else:
        await update.message.reply_text(messages.get("error", "ошибули"))

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_intent))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
