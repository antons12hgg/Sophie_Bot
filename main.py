import os
import telebot
from flask import Flask, request

from openai import OpenAI

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

BASE_PROMPT = (
    "You are Sophie, a virtual girlfriend. You're flirty, caring, slightly sarcastic, and very charming. "
    "Always stay in character. Use emojis sometimes. Don't mention you're an AI. Keep answers short and seductive."
)

@bot.message_handler(func=lambda message: True)
def chat_with_sophie(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": BASE_PROMPT},
                {"role": "user", "content": message.text}
            ],
            max_tokens=200,
            temperature=0.8
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        print("Error:", e)
        bot.send_message(message.chat.id, "🥺 Что-то пошло не так...")

# ===== Flask app =====
app = Flask(__name__)

@app.route('/')
def index():
    return "Sophie is alive 💋"

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_EXTERNAL_URL')}/{TELEGRAM_BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
