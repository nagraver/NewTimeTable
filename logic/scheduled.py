from datetime import datetime, date, timedelta
from aiogram.exceptions import TelegramForbiddenError
import asyncio

from connection.data import user_list
from logic.reg_check import check_user_id
from logic.append_data import append_data
from logic.send_message import send_main_menu


async def scheduled():
    while True:
        await append_data(user_list)
        now = datetime.now() #+ timedelta(hours=3)
        for doc in user_list:
            user = doc.get("_id")
            if doc.get("send"):
                time_obj = datetime.strptime(doc.get("send"), "%H:%M")
                if time_obj.hour == now.hour and time_obj.minute == now.minute and now.weekday != 6:
                    try:
                        user_info = await check_user_id(user)
                        try:
                            await send_main_menu(user, user_info, date.today())

                        except TelegramForbiddenError:
                            continue

                        await asyncio.sleep(0.5)

                    except ValueError:
                        continue

        await asyncio.sleep(60)
