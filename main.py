from aiogram import executor
from config.config import admin_id
from loader import bot


async def on_startup(dp):
    # await asyncio.sleep(10)
    await bot.send_message(admin_id, "I'm running")


async def on_shutdown(dp):
    await bot.send_message(admin_id, "Powering down")
    await bot.close()


if __name__ == "__main__":
    from handlers.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)