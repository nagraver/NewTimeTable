import httpx
from datetime import datetime
import asyncio

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'referer': 'https://sevsu.samrzhevsky.ru/schedule'
}

async def get_groups(inst):
    url = 'https://schedule.sevsu.ru/api/groups'
    params = {
        'v': '4',
        'section': '0',
        'institute': inst,
    }
    async with httpx.AsyncClient() as client:
        task = client.get(url, params=params, headers=header)
        response = await asyncio.create_task(task)

    return response.json().get('groups')


async def get_schedule(inst, group, the_day):
    start_date = datetime.strptime('020924', "%d%m%y").date()
    week_number = (the_day - start_date).days // 7 + 1
    url = 'https://schedule.sevsu.ru/api/schedule'
    params = {
        'v': '4',
        'section': '0',
        'institute': inst,
        'group': str(group),
        'week': str(week_number),
    }
    async with httpx.AsyncClient() as client:
        task = client.get(url, params=params, headers=header)
        response = await asyncio.create_task(task)

    return response.json().get('schedule')
