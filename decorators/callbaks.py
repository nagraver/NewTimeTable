from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from datetime import datetime

from logic.process import process_the_settings, process_the_message
from keyboards.markup import settings_buttons, time_buttons, menu_buttons, group_buttons, inst_buttons
from storage.connection import Mongo
from logic.states import Schedule

router = Router()
db = Mongo()


@router.callback_query(F.data[:3] == 'day')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    the_day = datetime.strptime(callback.data[3:], "%Y-%m-%d").date()
    await process_the_message(user=user, the_day=the_day, msg=mess_id)


@router.callback_query(F.data == 'settings')
async def handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    markup = await settings_buttons(user)
    await process_the_settings(user, markup, mess_id, include_all=True)


@router.callback_query(F.data == 'i_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    markup = await inst_buttons()
    await process_the_settings(user, markup, mess_id, include_institute=True)


@router.callback_query(F.data == 'g_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    user_info = await db.get_user_info(user)
    inst = user_info.get('inst')
    if inst is None:
        markup = await inst_buttons()
        await process_the_settings(user, markup, include_group=True)
        return
    markup = await group_buttons(inst)
    await process_the_settings(user, markup, mess_id, include_group=True)


@router.callback_query(F.data == 'm_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    markup = await menu_buttons()
    await process_the_settings(user, markup, mess_id, include_mode=True)


@router.callback_query(F.data == 's_choice')
async def handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    markup = await time_buttons()

    await process_the_settings(user, markup, mess_id, include_send=True)
    await state.set_state(Schedule.text)


@router.callback_query(F.data[:4] == 'inst')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    inst = callback.data[4:]
    markup = await group_buttons(inst)
    await db.update_data(user=user, inst=inst)
    await process_the_settings(user, markup, mess_id, include_group=True)


@router.callback_query(F.data[:5] == 'group')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    group = callback.data[5:]
    markup = await settings_buttons(user)
    await db.update_data(user=user, group=group)
    await process_the_settings(user, markup, mess_id, include_all=True)


@router.callback_query(F.data[:4] == 'mode')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    mode = int(callback.data[4:])
    markup = await settings_buttons(user)
    await db.update_data(user=user, mode=mode)
    await process_the_settings(user, markup, mess_id, include_all=True)


@router.callback_query(F.data[:3] == 's_t')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    markup = await time_buttons()
    send_day = 0 if callback.data == 's_today' else 1
    await db.update_data(user=user, send_day=send_day)
    await process_the_settings(user, markup, mess_id, include_send=True)


@router.callback_query(F.data == 'off_schedule')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    markup = await time_buttons()
    await db.update_data(user=user, send='')
    await process_the_settings(user, markup, mess_id, include_send=True)


@router.message(F.text, Schedule.text)
async def time_handler(message: types.Message):
    user = str(message.chat.id)
    user_time = message.text
    markup = await time_buttons()
    try:
        datetime.strptime(user_time, '%H:%M')
        await db.update_data(user=user, send=user_time)
        await process_the_settings(user=user, markup=markup, include_send=True)

    except ValueError:
        await message.reply("Не соответствие формату ЧЧ:ММ", reply_markup=markup)
