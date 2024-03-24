from pymongo import MongoClient
from pymongo.server_api import ServerApi
from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv("TESTBOT"), parse_mode="MARKDOWN")
uri = os.getenv("URI")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.timetable
col = db.data
