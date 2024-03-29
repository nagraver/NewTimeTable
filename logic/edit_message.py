from connection import bot, col

from markup import inst_buttons, group_buttons, menu_buttons, main_buttons, time_buttons, settings_buttons

from logic.output_text import settings_text, schedule_text


async def edit_to_inst_menu(user, user_info, msg):
    try:
        txt = await settings_text(user_info)
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await inst_buttons()
        )
    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_group_menu(user, user_info, msg):
    try:
        txt = await settings_text(user_info)
        inst = user_info.get('inst')
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await group_buttons(inst)
        )
    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_mode_menu(user, user_info, msg):
    try:
        txt = await settings_text(user_info)
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await menu_buttons()
        )
    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_time_menu(user, user_info, msg):
    try:
        txt = await settings_text(user_info)
        user = user_info.get('_id')
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await time_buttons()
        )

    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_main_menu(user, user_info, msg, the_day):
    try:
        txt = await schedule_text(user_info, the_day)
        user = user_info.get('_id')
        mode = user_info.get('mode')
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await main_buttons(mode)
        )
    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_settings_menu(user, user_info, msg):
    try:
        txt = await settings_text(user_info)
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await settings_buttons()
        )
    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_error(user, user_info, msg):
    if user_info is None:
        col.insert_one({'_id': user, 'mode': 0})
        user_info = col.find_one({'_id': user})
        await edit_to_inst_menu(user, user_info, msg)
    elif user_info.get('inst') is None:
        await edit_to_inst_menu(user, user_info, msg)
    elif user_info.get('group') is None:
        await edit_to_group_menu(user, user_info, msg)
