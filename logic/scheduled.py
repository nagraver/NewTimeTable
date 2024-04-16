from datetime import datetime, date, timedelta
import asyncio

from storage.connection import Mongo
from logic.process import process_the_message

db = Mongo()
col = db.col


async def scheduled():
    while True:
        user_list = col.find({'send': {'$exists': True}})
        # now = datetime.now() + timedelta(hours=3)
        now = datetime.now()
        for doc in user_list:
            time_obj = datetime.strptime(doc.get("send"), "%H:%M")
            if time_obj.hour == now.hour and time_obj.minute == now.minute and now.weekday != 6:
                try:
                    day = doc.get("send_day")
                    the_day = date.today() + timedelta(days=day)
                    await process_the_message(user=doc.get('_id'), the_day=the_day)
                    await asyncio.sleep(0.5)

                except Exception as e:
                    print(e)

        await asyncio.sleep(60)
