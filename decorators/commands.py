from datetime import date
from aiogram import types

from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from logic.process import process_the_settings, process_the_message
from keyboards.markup import settings_buttons

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    user = str(message.from_user.id)
    await process_the_message(user=user, the_day=date.today())


@router.message(Command("settings"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    user = str(message.from_user.id)
    markup = await settings_buttons(user)
    await process_the_settings(user=user, markup=markup, include_all=True)
