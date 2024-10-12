import requests
import asyncio
import aiogram
from bs4 import BeautifulSoup

session = requests.Session()

header = {
    'Accept': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
}

data = {
    "username": "ttolla25@gmail.com",
    "password": "8HUhZDod",
    "rememberMe": "on",
    "credentialId": ""
}


async def getting():
    # url = 'https://lk.sevsu.ru/student/index'
    url = 'https://auth.sevsu.ru/realms/portal/login-actions/authenticate?execution=c0d674fe-7cd0-4b2e-951d-f486c14139aa&client_id=do&tab_id=mkfJLk1nyWY'
    # response = requests.post(url, data=data, headers=header).text
    response = requests.post(url, headers=header, data=data).text
    print(response)


async def main():
    await getting()


if __name__ == "__main__":
    asyncio.run(main())
