import asyncio
import logging
import sys
from aiogram import Dispatcher
from dotenv import load_dotenv

from decorators import commands, callbaks, admin
from storage.connection import bot
from logic.dispatch import dispatch

load_dotenv()


async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router, callbaks.router, admin.router)
    # await asyncio.gather(dp.start_polling(bot), dispatch())
    await asyncio.gather(dp.start_polling(bot), dispatch(), return_exceptions=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Critical main error: {e}")
