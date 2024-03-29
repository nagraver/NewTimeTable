from aiogram import Router, types
from aiogram.filters import Command

from connection import col
from logic.send_message import send_settings, send_schedule
from markup import settings_buttons

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    user_info = col.find_one({'_id': user})
    await send_schedule(user, user_info)


@router.message(Command("settings"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    user_info = col.find_one({'_id': user})
    markup = await settings_buttons()
    await send_settings(user, user_info, markup)
