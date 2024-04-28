from pymongo import MongoClient
from pymongo.server_api import ServerApi
from aiogram import Bot
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

bot = Bot(os.getenv("BOT"), parse_mode="MARKDOWN")
uri = os.getenv("URI")


class Mongo:
    def __init__(self):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client.timetable
        self.col = self.db.data

    async def get_user_info(self, user):
        user_info = self.col.find_one({"_id": user})
        if user_info is None:
            self.col.insert_one({"_id": user, "mode": 0, "send_day": 0})
            user_info = self.col.find_one({"_id": user})
        return user_info

    async def update_data(self, user, inst=None, group=None, mode=None, send=None, send_day=None, usage=None):
        if inst:
            self.col.update_one({'_id': user}, {'$set': {'inst': inst}})
        elif group:
            self.col.update_one({'_id': user}, {'$set': {'group': group}})
        elif mode:
            self.col.update_one({'_id': user}, {'$set': {'mode': mode}})
        elif send is not None:
            if send == '':
                self.col.update_one({'_id': user}, {'$unset': {'send': ''}})
            else:
                self.col.update_one({'_id': user}, {'$set': {'send': send}})
        elif send_day is not None:
            self.col.update_one({'_id': user}, {'$set': {'send_day': send_day}})
        elif usage:
            self.col.update_one({'_id': user}, {'$set': {'usage': date.today().strftime('%Y.%m.%d')}})
