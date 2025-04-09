from telethon import TelegramClient, events

api_id = 21656727
api_hash = '561e1c275ae2a89cc2b8670bb1a3a178'

client = TelegramClient('forwarder_session', api_id, api_hash)

target_group_id = -4674552364
source_bot_username = 'HUMOcardbot'

@client.on(events.NewMessage(from_users=source_bot_username))
async def handler(event):
    text = event.raw_text
    if '💳 HUMOCARD *0108' in text:
        # Формируем сообщение с заменой имени на AUA
        custom_message = f"AUA\n{text}"
        await client.send_message(target_group_id, custom_message)

client.start()
print("Userbot is running ✅")
client.run_until_disconnected()
