from aiogram import Router, types, F
from datetime import datetime, date
from logic import (send_inst_menu, send_group_menu, send_mode_menu, send_time_menu,
                   append_data, check_user_id, send_main_menu, send_settings_menu
                   )
from connection import user_list, col

router = Router()


@router.callback_query(F.data[:3] == 'day')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    the_day = datetime.strptime(callback.data[3:], "%Y-%m-%d").date()

    try:
        user_info = await check_user_id(user)
        await send_main_menu(user, user_info, the_day)
        col.update_one({'_id': user}, {'$set': {'usage': date.today().strftime('%Y.%m.%d')}})
        await append_data(user_list)

    except ValueError:
        pass


@router.callback_query(F.data[:4] == 'id')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    await send_inst_menu(user)


@router.callback_query(F.data[:4] == 'inst')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    inst = callback.data[4:]
    await send_group_menu(user, inst)
    col.update_one({'_id': user}, {'$set': {'inst': inst}})
    await append_data(user_list)


@router.callback_query(F.data[:5] == 'group')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    group = callback.data[5:]
    user_info = await check_user_id(user)
    await send_settings_menu(user, user_info)
    col.update_one({'_id': user}, {'$set': {'group': group}})
    await append_data(user_list)


@router.callback_query(F.data[:4] == 'mode')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    mode = int(callback.data[4:])
    user_info = await check_user_id(user)
    await send_settings_menu(user, user_info)

    col.update_one({'_id': user}, {'$set': {'mode': mode}})
    await append_data(user_list)


@router.callback_query(F.data == 'off_schedule')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    user_info = await check_user_id(user)
    await send_settings_menu(user, user_info)

    col.update_one({'_id': user}, {'$unset': {'send': ""}})
    await append_data(user_list)


@router.callback_query(F.data == 'i_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    await send_inst_menu(user)


@router.callback_query(F.data == 'g_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    user_info = await check_user_id(user)
    inst = user_info.get('inst')
    await send_group_menu(user, inst)


@router.callback_query(F.data == 'm_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    await send_mode_menu(user)


@router.callback_query(F.data == 's_choice')
async def handler(callback: types.CallbackQuery):
    user = str(callback.message.chat.id)
    await send_time_menu(user)

    @router.message(F.text)
    async def time_handler(message: types.Message):
        user_time = message.text
        user_info = await check_user_id(user)
        try:
            datetime.strptime(user_time, '%H:%M')
            await send_settings_menu(user, user_info)
            col.update_one({'_id': user}, {'$set': {'send': user_time}})
            await append_data(user_list)

        except ValueError:
            await message.reply("Не соответствие 24-х часовому формату")
            await send_time_menu(user)
