import os
import json
from flask import Flask, request
from telegram import Bot

app = Flask(__name__)

# Убедитесь, что токен передан в переменной окружения
TOKEN = os.getenv("8171400853:AAGLdEEbD2TJJZ__iYPr67xjK-FYGOaCZhw")

# Создаем экземпляр бота
bot = Bot(token=TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем данные из запроса
    update = request.get_json()
    
    # Проверяем, есть ли сообщение
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        # Отправляем ответ на сообщение
        bot.send_message(chat_id=chat_id, text="Спасибо за ваше сообщение: " + text)

    return "Webhook received!", 200

if __name__ == '__main__':
    app.run(debug=True)
