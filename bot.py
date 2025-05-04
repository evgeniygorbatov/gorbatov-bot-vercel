import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def start(update, context):
    keyboard = [[InlineKeyboardButton("Записаться на съёмку", callback_data='book')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Хочешь записаться на фотосессию?', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'book':
        context.user_data['step'] = 'name'
        query.edit_message_text(text="Как тебя зовут?")

def handle_message(update, context):
    step = context.user_data.get('step')
    text = update.message.text

    if step == 'name':
        context.user_data['name'] = text
        context.user_data['step'] = 'date'
        update.message.reply_text("Когда ты хочешь провести съёмку?")
    elif step == 'date':
        context.user_data['date'] = text
        context.user_data['step'] = 'details'
        update.message.reply_text("Расскажи подробнее о съёмке (локация, стиль и т.д.)")
    elif step == 'details':
        context.user_data['details'] = text
        name = context.user_data['name']
        date = context.user_data['date']
        details = context.user_data['details']

        message = f"Новая заявка 📸\n\nИмя: {name}\nДата съёмки: {date}\nДетали: {details}"
        bot.send_message(chat_id=OWNER_CHAT_ID, text=message)
        update.message.reply_text("Спасибо! Я получил твою заявку и скоро свяжусь с тобой.")
        context.user_data.clear()
    else:
        update.message.reply_text("Нажми кнопку ниже, чтобы начать.")
        start(update, context)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()