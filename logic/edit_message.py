from connection import bot, col

from markup import inst_buttons, group_buttons, menu_buttons, main_buttons, time_buttons, settings_buttons

from logic.output_text import settings_text, schedule_text


async def edit_to_inst_menu(user_info, msg):
    txt = await settings_text(user_info)
    user = user_info.get('_id')
    await bot.edit_message_text(
        chat_id=user,
        message_id=msg,
        text=txt,
        reply_markup=await inst_buttons()
    )


async def edit_to_group_menu(user_info, msg):
    txt = await settings_text(user_info)
    user = user_info.get('_id')
    inst = user_info.get('inst')
    await bot.edit_message_text(
        chat_id=user,
        message_id=msg,
        text=txt,
        reply_markup=await group_buttons(inst)
    )


async def edit_to_mode_menu(user_info, msg):
    txt = await settings_text(user_info)
    user = user_info.get('_id')
    await bot.edit_message_text(
        chat_id=user,
        message_id=msg,
        text=txt,
        reply_markup=await menu_buttons()
    )


async def edit_to_time_menu(user_info, msg):
    txt = await settings_text(user_info)
    user = user_info.get('_id')
    await bot.edit_message_text(
        chat_id=user,
        message_id=msg,
        text=txt,
        reply_markup=await time_buttons()
    )


async def edit_to_error(user_info, msg):
    user = user_info.get('_id')
    if user_info is None:
        col.insert_one({'_id': user, 'mode': 0})
        user_info = col.find_one({'_id': user})
        await edit_to_inst_menu(user_info, msg)
    elif user_info.get('inst') is None:
        await edit_to_inst_menu(user_info, msg)
    elif user_info.get('group') is None:
        await edit_to_group_menu(user_info, msg)


async def edit_to_main_menu(user_info, msg, the_day):
    txt = await schedule_text(user_info, the_day)
    user = user_info.get('_id')
    mode = user_info.get('mode')
    await bot.edit_message_text(
        chat_id=user,
        message_id=msg,
        text=txt,
        reply_markup=await main_buttons(mode)
    )


async def edit_to_settings_menu(user_info, msg):
    txt = await settings_text(user_info)
    user = user_info.get('_id')
    await bot.edit_message_text(
        chat_id=user,
        message_id=msg,
        text=txt,
        reply_markup=await settings_buttons()
    )
