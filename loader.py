import asyncio
from config.config import BOT_TOKEN
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop = loop, storage=storage)