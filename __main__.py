from logging import DEBUG
import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message

from . import app, log
from .logger import log_command
from .utils import convert_message


media_filter = (filters.audio | filters.video | filters.voice | filters.video_note)

@app.on_message(filters.command("start"))
async def start(app: Client, msg: Message):
    log_command(msg, log)

    await msg.reply(
        "**Привет!** Отправь мне **любой** аудио или видео **файл**, "
        "и я превращу его в **голосовое сообщение**.\n\n"

        "Также ты можешь **добавить** меня **в группу** и отправить команду /voice "
        "в **ответ** на любое сообщение, чтобы я сделал из него **голосовое**!"
    )

@app.on_message(filters.private & media_filter)
async def converter(app: Client, msg: Message):
    if not msg.command:
        msg.command = ["__dm_media_received"]
        log_command(msg, log)

    try:
        # Download and convert received audio
        converting = await msg.reply("⌛ Конвертируем аудио... Это может занять некоторое время")
        await app.send_chat_action(msg.chat.id, ChatAction.RECORD_AUDIO)

        voice = await convert_message(msg)

        # Send converted audio as a voice message
        await converting.delete()
        await app.send_chat_action(msg.chat.id, ChatAction.UPLOAD_AUDIO)

        await msg.reply_voice(voice)

    # Notify the user if something went wrong
    except Exception as e:
        if hasattr(e, "__message__"):
            await msg.reply(getattr(e, "__message__"))
        raise


@app.on_message(filters.command("voice") & filters.group)
async def voice(app: Client, msg: Message):
    log_command(msg, log)

    if not msg.reply_to_message or not await media_filter(app, msg):
        return await msg.reply(
            "Пожалуйста, отправь команду /voice "
            "в ответ на любое сообщение с **аудио** или **видео** файлом!"
        )

    await converter(app, msg)

@app.on_message(filters.command("voice") & filters.private)
async def voice_dm(app: Client, msg: Message):
    msg.command = ["voice (DM)"]
    log_command(msg, log)

    await msg.reply(
        "**Привет!** Отправь мне **любой** аудио или видео **файл**, "
        "и я превращу его в **голосовое сообщение**."
    )

app.run()