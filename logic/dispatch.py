import logging
from datetime import datetime, date, timedelta
import asyncio

from storage.connection import Mongo
from logic.process import process_the_message

db = Mongo()
col = db.col


async def dispatch():
    while True:
        user_list = col.find({'send': {'$exists': True}})
        now = datetime.now() + timedelta(hours=3)
        for doc in user_list:
            time_obj = datetime.strptime(doc.get("send"), "%H:%M")
            if time_obj.hour == now.hour and time_obj.minute == now.minute:
                day = doc.get("send_day")
                if day == 0 and now.weekday() == 6 or day == 1 and now.weekday() == 5:
                    continue
                try:
                    the_day = date.today() + timedelta(days=day)
                    await process_the_message(user=doc.get('_id'), the_day=the_day)
                    await asyncio.sleep(0.5)

                except Exception as e:
                    logging.error(f"Error:{e}")

        await asyncio.sleep(60)
