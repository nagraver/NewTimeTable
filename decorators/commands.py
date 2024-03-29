from aiogram import Router, types
from aiogram.filters import Command
from datetime import date

from connection import col
from logic import send_main_menu, send_settings_menu

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    user_info = col.find_one({'_id': user})
    await send_main_menu(user, user_info, date.today())


@router.message(Command("settings"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    user_info = col.find_one({'_id': user})
    await send_settings_menu(user, user_info)
