import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote_plus


async def get_groups(inst):
    url = 'https://sevsu.samrzhevsky.ru/api/groups?v=3.1&section=0&institute=' + inst
    response = requests.get(url).text
    bs = BeautifulSoup(response, "lxml").text

    return json.loads(bs)['groups']


async def get_schedule(inst, group, the_day):
    start_date = datetime.strptime('280823', "%d%m%y").date()
    week_number = (the_day - start_date).days // 7 + 1

    url = 'https://sevsu.samrzhevsky.ru/api/schedule?v=3.1&section=0&institute=' + inst + '&group=' + str(
        quote_plus(group)) + '&week=' + str(week_number)
    response = requests.get(url).text
    bs = BeautifulSoup(response, "lxml").text

    try:
        return json.loads(bs)['schedule']
    except KeyError:
        return None

