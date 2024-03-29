from connection import bot, col

from markup import inst_buttons, group_buttons, main_buttons

from logic.output_text import settings_text, schedule_text


async def edit_to_error(user, user_info, msg):
    if user_info is None:
        col.insert_one({'_id': user, 'mode': 0})
        user_info = col.find_one({'_id': user})
        await edit_to_settings(user, user_info, msg, await inst_buttons())
    elif user_info.get('inst') is None:
        await edit_to_settings(user, user_info, msg, await inst_buttons())
    elif user_info.get('group') is None:
        inst = user_info.get('inst')
        await edit_to_settings(user, user_info, msg, await group_buttons(inst))


async def edit_to_schedule(user, user_info, msg, the_day):
    try:
        txt = await schedule_text(user_info, the_day)
        mode = user_info.get('mode')
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=await main_buttons(mode)
        )
    except Exception:
        await edit_to_error(user, user_info, msg)


async def edit_to_settings(user, user_info, msg, markup):
    try:
        txt = await settings_text(user_info)
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=markup
        )
    except Exception:
        await edit_to_error(user, user_info, msg)
