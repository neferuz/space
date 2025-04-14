from telethon import TelegramClient, events
from flask import Flask
import threading

# --- Flask сервер для Healthcheck (wake-up URL) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# --- Настройки Telegram API ---
api_id = 21656727
api_hash = '561e1c275ae2a89cc2b8670bb1a3a178'

client = TelegramClient('forwarder_session', api_id, api_hash)

target_group_id = -4674552364
source_bot_username = 'HUMOcardbot'

# Храним ID уже обработанных сообщений
handled_messages = set()

@client.on(events.NewMessage(from_users=source_bot_username))
async def handler(event):
    message_id = event.id
    text = event.raw_text

    if message_id not in handled_messages and '🎉 Пополнение' in text and '💳 HUMOCARD *0108' in text:
        handled_messages.add(message_id)

        # Выделяем жирным Пополнение и Сумму
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if '🎉 Пополнение' in line or '➕' in line:
                line = f"<b>{line}</b>"
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)
        custom_message = f"<b>AUA</b>\n{formatted_text}"

        await client.send_message(target_group_id, custom_message, parse_mode='html')

# --- Запускаем Flask в отдельном потоке перед Telegram клиентом ---
threading.Thread(target=run_flask).start()

client.start()
print("Userbot is running ✅")
client.run_until_disconnected()
