from connection import bot, col

from markup import inst_buttons, group_buttons, main_buttons

from logic.output_text import settings_text, schedule_text


async def send_error(user, user_info):
    if user_info is None:
        col.insert_one({'_id': user, 'mode': 0})
        user_info = col.find_one({'_id': user})
        await send_settings(user, user_info, await inst_buttons())
    elif user_info.get('inst') is None:
        await send_settings(user, user_info, await inst_buttons())
    elif user_info.get('group') is None:
        inst = user_info.get('inst')
        await send_settings(user, user_info, await group_buttons(inst))


async def send_schedule(user, user_info):
    try:
        txt = await schedule_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=await main_buttons(user_info.get('mode'))
        )

    except Exception:
        await send_error(user, user_info)


async def send_settings(user, user_info, markup):
    try:
        txt = await settings_text(user_info)
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=markup
        )

    except Exception:
        await send_error(user, user_info)
