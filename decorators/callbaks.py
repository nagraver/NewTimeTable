from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from datetime import datetime, date

from logic import (
    edit_to_inst_menu, edit_to_group_menu, edit_to_mode_menu, edit_to_time_menu, edit_to_settings_menu,
    edit_to_main_menu, send_settings_menu, send_time_menu
)
from connection import col
from logic.states import Schedule

router = Router()


@router.callback_query(F.data[:3] == 'day')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    the_day = datetime.strptime(callback.data[3:], "%Y-%m-%d").date()
    user_info = col.find_one({'_id': user})
    await edit_to_main_menu(user, user_info, mess_id, the_day)
    col.update_one({'_id': user}, {'$set': {'usage': date.today().strftime('%Y.%m.%d')}})


@router.callback_query(F.data[:4] == 'inst')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    inst = callback.data[4:]

    col.update_one({'_id': user}, {'$set': {'inst': inst}})
    user_info = col.find_one({'_id': user})

    await edit_to_group_menu(user, user_info, mess_id)


@router.callback_query(F.data[:5] == 'group')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    group = callback.data[5:]

    col.update_one({'_id': user}, {'$set': {'group': group}})
    user_info = col.find_one({'_id': user})

    await edit_to_settings_menu(user, user_info, mess_id)


@router.callback_query(F.data[:4] == 'mode')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    mode = int(callback.data[4:])

    col.update_one({'_id': user}, {'$set': {'mode': mode}})
    user_info = col.find_one({'_id': user})
    await edit_to_settings_menu(user, user_info, mess_id)


@router.callback_query(F.data == 'i_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    user_info = col.find_one({'_id': user})
    await edit_to_inst_menu(user, user_info, mess_id)


@router.callback_query(F.data == 'g_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    user_info = col.find_one({'_id': user})
    await edit_to_group_menu(user, user_info, mess_id)


@router.callback_query(F.data == 'm_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    user_info = col.find_one({'_id': user})
    await edit_to_mode_menu(user, user_info, mess_id)


@router.callback_query(F.data == 's_choice')
async def handler(callback: types.CallbackQuery, state: FSMContext):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id
    user_info = col.find_one({'_id': user})
    await edit_to_time_menu(user, user_info, mess_id)
    await state.set_state(Schedule.text)


@router.message(F.text, Schedule.text)
async def time_handler(message: types.Message, state: FSMContext):
    user = str(message.chat.id)
    user_time = message.text

    try:
        datetime.strptime(user_time, '%H:%M')
        col.update_one({'_id': user}, {'$set': {'send': user_time}})
        user_info = col.find_one({'_id': user})
        await send_settings_menu(user, user_info)
        await state.clear()

    except ValueError:
        await message.reply("Не соответствие 24-х часовому формату")
        user_info = col.find_one({'_id': user})
        await send_time_menu(user, user_info)


@router.callback_query(F.data == 'off_schedule')
async def handler(callback: types.CallbackQuery, state: FSMContext):
    user = str(callback.message.chat.id)
    mess_id = callback.message.message_id

    col.update_one({'_id': user}, {'$unset': {'send': ''}})
    user_info = col.find_one({'_id': user})

    await edit_to_settings_menu(user, user_info, mess_id)
    await state.clear()
