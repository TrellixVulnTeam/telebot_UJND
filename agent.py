from telethon import TelegramClient, events
import sqlite3
import asyncio
import sys
import traceback


api_id = api_id
api_hash = 'api_hash'
phone = 'phone_num'


async def send_rec(mes, aid):
    try:
        await client.forward_messages(-1001393645013, mes, aid)
    except sqlite3.OperationalError:
        await send_rec(mes, aid)


client = TelegramClient('test', api_id, api_hash)


@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        if event.from_id == 123456789:
            await client.forward_messages(987654321, event.message.id, event.from_id)
        if event.from_id == 987654321:
            if event.media:
                mes = await client.get_messages(987654321, ids=event.message.id-2)
                aid = str(event.reply_markup.rows[0].buttons[0].url).replace("http://t.me/Gozilla_bot?start=", "")
                await client.send_message(-channel_id, mes.message + "+" + str(aid), link_preview=False)
                await send_rec(event.message.id, event.from_id)
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        from bot import Bot
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))

client.start()
client.run_until_disconnected()
