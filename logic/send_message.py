from connection import bot, col

from markup import inst_buttons, group_buttons, menu_buttons, main_buttons, time_buttons, settings_buttons

from logic.output_text import settings_text, schedule_text


async def send_inst_menu(user, user_info):
    try:
        txt = await settings_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await inst_buttons()
        )

    except Exception:
        await send_error(user, user_info)


async def send_group_menu(user, user_info):
    try:
        txt = await settings_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await group_buttons(user_info.get('inst'))
        )

    except Exception:
        await send_error(user, user_info)


async def send_mode_menu(user, user_info):
    try:
        txt = await settings_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await menu_buttons()
        )

    except Exception:
        await send_error(user, user_info)


async def send_time_menu(user, user_info):
    try:
        txt = await settings_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await time_buttons()
        )
    except Exception:
        await send_error(user, user_info)


async def send_main_menu(user, user_info, the_day):
    try:
        txt = await schedule_text(user_info, the_day)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await main_buttons(user_info.get('mode'))
        )

    except Exception:
        await send_error(user, user_info)


async def send_settings_menu(user, user_info):
    try:
        txt = await settings_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await settings_buttons()
        )

    except Exception:
        await send_error(user, user_info)


async def send_error(user, user_info):
    if user_info is None:
        col.insert_one({'_id': user, 'mode': 0})
        user_info = col.find_one({'_id': user})
        await send_inst_menu(user, user_info)
    elif user_info.get('inst') is None:
        await send_inst_menu(user, user_info)
    elif user_info.get('group') is None:
        await send_group_menu(user, user_info)
