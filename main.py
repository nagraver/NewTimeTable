import asyncio
import logging
import sys
from aiogram import Dispatcher
from dotenv import load_dotenv

from decorators import commands, callbaks, admin
from storage.connection import bot
from logic.dispatch import dispatch

load_dotenv()

try:
    async def main():
        dp = Dispatcher()
        dp.include_routers(commands.router, callbaks.router, admin.router)
        await asyncio.gather(dp.start_polling(bot), dispatch())


    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())

except Exception as e:
    print(e)
