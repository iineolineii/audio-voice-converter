from pyrogram import Client

from . import config
from .logger import setup_logging

# Logging configuration
app = Client(**config.BOT)
log = setup_logging(__name__)
