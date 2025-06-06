from pymongo import MongoClient
from pymongo.server_api import ServerApi
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
import os
import redis
from dotenv import load_dotenv
from datetime import date

load_dotenv()

BOT = os.getenv("BOT")
TESTBOT = os.getenv("TESTBOT")
URI = os.getenv("URI")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

bot = Bot(BOT, default=DefaultBotProperties(parse_mode="MARKDOWN"))


red = redis.Redis(host="redis", port=6379, db=0, password=REDIS_PASSWORD)


def cache_message(key, value, expiration=60 * 60 * 24):
    red.set(key, value, ex=expiration)


class Mongo:
    def __init__(self):
        self.client = MongoClient(URI, server_api=ServerApi("1"))
        self.db = self.client.timetable
        self.col = self.db.data

    async def get_user_info(self, user):
        user_info = self.col.find_one({"_id": user})
        if user_info is None:
            self.col.insert_one({"_id": user, "mode": 4, "send_day": 0})
            user_info = self.col.find_one({"_id": user})
        return user_info

    async def update_data(
        self,
        user,
        inst=None,
        group=None,
        mode=None,
        send=None,
        send_day=None,
        usage=None,
    ):
        if inst:
            self.col.update_one({"_id": user}, {"$set": {"inst": inst}})
        elif group:
            self.col.update_one({"_id": user}, {"$set": {"group": group}})
        elif mode:
            self.col.update_one({"_id": user}, {"$set": {"mode": mode}})
        elif send is not None:
            if send == "":
                self.col.update_one({"_id": user}, {"$unset": {"send": ""}})
            else:
                self.col.update_one({"_id": user}, {"$set": {"send": send}})
        elif send_day is not None:
            self.col.update_one({"_id": user}, {"$set": {"send_day": send_day}})
        elif usage:
            self.col.update_one({"_id": user}, {"$set": {"usage": date.today().strftime("%Y.%m.%d")}})
