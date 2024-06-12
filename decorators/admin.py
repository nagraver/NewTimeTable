from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
import logging
import asyncio

from keyboards.markup import settings_buttons, back_button
from logic.states import Schedule
from storage.connection import bot
from logic.process import process_the_settings
from storage.connection import Mongo

router = Router()
db = Mongo()
col = db.col


@router.callback_query(F.data == "mailing")
async def mailing(callback: types.CallbackQuery, state: FSMContext) -> None:
    markup = await back_button()
    await callback.message.answer("Введи сообщение", reply_markup=markup)
    await state.set_state(Schedule.mailing)


@router.message(Schedule.mailing)
async def mailing_message(message: types.Message, state: FSMContext) -> None:
    user = str(message.chat.id)
    user_list = col.find()
    for item in user_list:
        try:
            _id = item.get("_id")
            await bot.send_message(chat_id=str(_id), text=message.text)
            await asyncio.sleep(0.2)
        except Exception as e:
            logging.error(f"{e}")

    await message.answer("Рассылка завершена. Выход из состояния рассылки.")
    markup = await settings_buttons(user=user)
    await process_the_settings(user=user, markup=markup, include_all=True)
    await state.clear()

# @router.message()
# async def grab(message: types.Message):
#     text = str(message.message_id.)
#     await bot.send_message(chat_id=message.chat.id, text=text)
