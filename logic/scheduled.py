from datetime import datetime, date, timedelta
import asyncio

from connection import col
from logic.send_message import send_main_menu


async def scheduled():
    while True:
        user_list = col.find()
        now = datetime.now() + timedelta(hours=3)
        for doc in user_list:
            user = doc.get("_id")
            if doc.get("send"):
                time_obj = datetime.strptime(doc.get("send"), "%H:%M")
                if time_obj.hour == now.hour and time_obj.minute == now.minute and now.weekday != 6:
                    try:
                        user_info = col.find_one({'_id': user})
                        await send_main_menu(user, user_info, date.today())
                        await asyncio.sleep(0.5)

                    except Exception:
                        continue

        await asyncio.sleep(60)
