import asyncio
from aiogram import Dispatcher
from dotenv import load_dotenv

from decorators import commands, callbaks
from connection import user_list, bot
from logic import append_data, scheduled

load_dotenv()


async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router, callbaks.router)
    await asyncio.gather(append_data(user_list), dp.start_polling(bot), scheduled())

if __name__ == "__main__":
    asyncio.run(main())
