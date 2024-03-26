import asyncio
import logging
import sys

from aiogram import Dispatcher
from dotenv import load_dotenv

from decorators import commands, callbaks
from connection import bot
from logic import scheduled

load_dotenv()


async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router, callbaks.router)
    await asyncio.gather(dp.start_polling(bot), scheduled())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
