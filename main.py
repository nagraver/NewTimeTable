import asyncio
import logging
import sys
import sentry_sdk
from aiogram import Dispatcher
from dotenv import load_dotenv

from decorators import commands, callbaks
from connection import bot
from logic import scheduled

load_dotenv()

sentry_sdk.init(
    dsn="https://d17d039bf9f9e14353fc6e77290e743d@o4506192017424384.ingest.sentry.io/4506192102227968",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

try:
    async def main():
        dp = Dispatcher()
        dp.include_routers(commands.router, callbaks.router)
        await asyncio.gather(dp.start_polling(bot), scheduled())


    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())

except Exception as e:
    sentry_sdk.capture_exception(e)
