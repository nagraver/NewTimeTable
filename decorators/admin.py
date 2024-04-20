from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

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
    txt = ''
    for i in user_list:
        txt += f"{i.get('_id')} \n"
    await bot.send_message("6103118179", message.text)
    await bot.send_message("6103118179", txt)
    await message.answer("Рассылка завершена. Выход из состояния рассылки.")

    markup = await settings_buttons(user=user)
    await process_the_settings(user=user, markup=markup, include_all=True)
    await state.clear()
