print("STARTING BOT...")

import os
import telebot
import openai

# Загружаем ключи из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Устанавливаем ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Промт для Софи
BASE_PROMPT = (
    "You are Sophie, a virtual girlfriend. You're flirty, caring, slightly sarcastic, and very charming. "
    "Always stay in character. Use emojis sometimes. Don't mention you're an AI. Keep answers short and seductive."
)

# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def chat_with_sophie(message):
    user_message = message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": BASE_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.8
        )
        reply = response.choices[0].message['content']
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        print("ERROR:", e)
        bot.send_message(message.chat.id, "Oops! Something went wrong.")

# Запуск бота
bot.polling(none_stop=True, interval=0, timeout=20, skip_pending=True)
