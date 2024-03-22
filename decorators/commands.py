from aiogram import Router, types
from aiogram.filters import Command
from datetime import date

from logic import check_user_id, send_main_menu, send_settings_menu
from markup import settings_buttons
from connection.data import institutes_arr

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    try:
        user_info = await check_user_id(user)
        await send_main_menu(user, user_info, date.today())

    except ValueError:
        pass


@router.message(Command("settings"))
async def start(message: types.Message):
    user = str(message.from_user.id)
    try:
        user_info = await check_user_id(user)
        await send_settings_menu(user, user_info)

    except ValueError:
        pass
