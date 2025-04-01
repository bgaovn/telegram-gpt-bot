from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type == "private" or BOT_USERNAME in message.text:
        user_input = message.text.replace(BOT_USERNAME, '').strip()
        if user_input:
            try:
                chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                reply = chat_completion.choices[0].message.content
            except Exception as e:
                reply = f"Lỗi: {e}"
            await message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot đang chạy với GPT-3.5 Turbo...")
    app.run_polling()