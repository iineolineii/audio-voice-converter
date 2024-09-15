from datetime import datetime
import os
from pathlib import Path
from tempfile import tempdir
from typing import BinaryIO

from pydub import AudioSegment
from pyrogram.types import Message
from pyrogram.errors import RPCError

from . import log


async def convert_message(msg: Message):
    try:
        audio = await msg.download(tempdir or "")
    except Exception as e:
        await log_error(msg, e, "download")
        raise

    try:
        voice = convert(audio)
    except Exception as e:
        await log_error(msg, e, "conversion")
        raise

    # Remove temporary files
    os.remove(audio)
    os.remove(voice.name)

    return voice


def convert(input_path: str) -> BinaryIO:
    output_path = Path(input_path).with_suffix(".ogg")

    audio = AudioSegment.from_file(input_path)
    voice = audio.export(output_path, format="ogg", codec="libopus")

    return voice # type: ignore

async def log_error(msg: Message, e: Exception, error_type: str):
    now = datetime.now().strftime("%d.%m.%Y, %H:%M:%S.%f")

    dm_log: Message = await msg.forward("iineolineii") # type: ignore
    await dm_log.reply(f'{now}: {error_type.capitalize()} error "<code>{type(e).__name__}</code>" from {msg.from_user.mention}')

    e.__dict__.update(__message__ = (
        f"😢 Не удалось {"скачать" if error_type.lower() == "download" else "конвертировать"} твой аудио файл! "
        f"Возникла ошибка <code>{type(e).__name__}</code>\n\n"

        "🙏 Пожалуйста, перешли это сообщение @iineolineii "
        "и в ближайшее время он постарается всё исправить\n\n"

        f"<i>Дата: {now}</i>"
    ))
    log.error(f'{error_type.capitalize()} error "{type(e).__name__}" from {msg.from_user.id} ({msg.from_user.full_name})')