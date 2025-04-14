from telethon import TelegramClient, events

api_id = 21656727
api_hash = '561e1c275ae2a89cc2b8670bb1a3a178'

client = TelegramClient('forwarder_session', api_id, api_hash)

target_group_id = -4674552364
source_bot_username = 'HUMOcardbot'

# Храним ID уже обработанных сообщений, чтобы избежать дублирования
handled_messages = set()

@client.on(events.NewMessage(from_users=source_bot_username))
async def handler(event):
    message_id = event.id
    text = event.raw_text

    # Проверка: только для сообщений, содержащих "🎉 Пополнение" и нужную карту
    if message_id not in handled_messages and '🎉 Пополнение' in text and '💳 HUMOCARD *0108' in text:
        handled_messages.add(message_id)

        # Жирным сделаем 🎉 Пополнение и сумму ➕ ...
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if '🎉 Пополнение' in line or '➕' in line:
                line = f"<b>{line}</b>"
            formatted_lines.append(line)

        formatted_text = "\n".join(formatted_lines)
        custom_message = f"<b>AUA</b>\n{formatted_text}"

        await client.send_message(target_group_id, custom_message, parse_mode='html')

client.start()
print("Userbot is running ✅")
client.run_until_disconnected()
