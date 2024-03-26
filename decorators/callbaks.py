from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from datetime import datetime, date

from logic import (send_inst_menu, send_group_menu, send_mode_menu, send_time_menu,
                   send_main_menu, send_settings_menu, send_error)
from connection import col
from logic.states import Schedule

router = Router()


@router.callback_query(F.data[:3] == 'day')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    the_day = datetime.strptime(callback.data[3:], "%Y-%m-%d").date()
    user_info = col.find_one({'_id': user})
    try:
        await send_main_menu(user, user_info, the_day)
        col.update_one({'_id': user}, {'$set': {'usage': date.today().strftime('%Y.%m.%d')}})

    except Exception as e:
        await send_error(user, e, user_info)


@router.callback_query(F.data[:4] == 'inst')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    inst = callback.data[4:]

    col.update_one({'_id': user}, {'$set': {'inst': inst}})

    await send_group_menu(user, inst)


@router.callback_query(F.data[:5] == 'group')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    group = callback.data[5:]

    col.update_one({'_id': user}, {'$set': {'group': group}})
    user_info = col.find_one({'_id': user})
    await send_settings_menu(user, user_info)


@router.callback_query(F.data[:4] == 'mode')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mode = int(callback.data[4:])

    col.update_one({'_id': user}, {'$set': {'mode': mode}})
    user_info = col.find_one({'_id': user})
    await send_settings_menu(user, user_info)


@router.callback_query(F.data == 'i_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    await send_inst_menu(user)


@router.callback_query(F.data == 'g_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    user_info = col.find_one({'_id': user})
    try:
        inst = user_info.get('inst')
        await send_group_menu(user, inst)

    except Exception as e:
        await send_error(user, e, user_info)


@router.callback_query(F.data == 'm_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    user_info = col.find_one({'_id': user})
    try:
        print(user_info)
        await send_mode_menu(user)

    except Exception as e:
        await send_error(user, e, user_info)


@router.callback_query(F.data == 's_choice')
async def handler(callback: types.CallbackQuery, state: FSMContext):
    user = str(callback.message.chat.id)
    user_info = col.find_one({'_id': user})
    try:
        await send_time_menu(user_info.get('_id'))
        await state.set_state(Schedule.text)

    except Exception as e:
        await send_error(user, e, user_info)


@router.message(F.text, Schedule.text)
async def time_handler(message: types.Message):
    user = str(message.chat.id)
    user_time = message.text

    try:
        datetime.strptime(user_time, '%H:%M')
        col.update_one({'_id': user}, {'$set': {'send': user_time}})
        user_info = col.find_one({'_id': user})
        await send_settings_menu(user, user_info)

    except ValueError:
        await message.reply("Не соответствие 24-х часовому формату")
        await send_time_menu(user)


@router.callback_query(F.data == 'off_schedule')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)

    col.update_one({'_id': user}, {'$unset': {'send': ""}})
    user_info = col.find_one({'_id': user})

    await send_settings_menu(user, user_info)
