import httpx
from datetime import datetime
from urllib.parse import quote_plus
import asyncio


async def get_groups(inst):
    url = 'https://sevsu.samrzhevsky.ru/api/groups?v=3.1&section=0&institute=' + inst
    async with httpx.AsyncClient() as client:
        task = client.get(url)
        response = await asyncio.create_task(task)

    return response.json().get('groups')


async def get_schedule(inst, group, the_day):
    start_date = datetime.strptime('280823', "%d%m%y").date()
    week_number = (the_day - start_date).days // 7 + 1

    url = 'https://sevsu.samrzhevsky.ru/api/schedule?v=3.1&section=0&institute=' + inst + '&group=' + str(
        quote_plus(group)) + '&week=' + str(week_number)
    async with httpx.AsyncClient() as client:
        task = client.get(url)
        response = await asyncio.create_task(task)

    try:
        return response.json().get('schedule')

    except KeyError:
        return None
