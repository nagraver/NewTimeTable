from aiogram import Router, types
from aiogram.filters import Command
from datetime import date
from pymongo.errors import DuplicateKeyError

from connection import col
from logic import send_main_menu, send_settings_menu, send_error

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    user_info = col.find_one({'_id': user})
    try:
        await send_main_menu(user, user_info, date.today())

    except Exception as e:
        await send_error(user, e, user_info)


@router.message(Command("settings"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    user_info = col.find_one({'_id': user})
    try:
        await send_settings_menu(user, user_info)

    except Exception as e:
        await send_error(user, e, user_info)
