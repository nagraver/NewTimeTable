from connection import bot, col

from markup import inst_buttons, group_buttons, menu_buttons, main_buttons, time_buttons, settings_buttons

from logic.output_text import settings_text, schedule_text


async def send_inst_menu(user):
    await bot.send_message(
        chat_id=user,
        text="Выбери институт",
        reply_markup=await inst_buttons()
    )


async def send_group_menu(user, inst):
    await bot.send_message(
        chat_id=user,
        text='Выбери группу',
        reply_markup=await group_buttons(inst)
    )


async def send_mode_menu(user):
    await bot.send_message(
        chat_id=user,
        text="Выбери меню",
        reply_markup=await menu_buttons()
    )


async def send_time_menu(user):
    await bot.send_message(
        chat_id=user,
        text="Введи желаемое время для отправки расписания",
        reply_markup=await time_buttons()
    )


async def send_error(user, user_info):
    if user_info is None:
        col.insert_one({'_id': user, 'mode': 0})
        await send_inst_menu(user)
    elif user_info.get('inst') is None:
        await send_inst_menu(user)
    elif user_info.get('group') is None:
        await send_group_menu(user, user_info.get('inst'))


async def send_main_menu(user, user_info, the_day):
    txt = await schedule_text(user_info, the_day)
    mode = user_info.get('mode')
    await bot.send_message(user, text=txt, reply_markup=await main_buttons(mode))


async def send_settings_menu(user, user_info):
    txt = await settings_text(user_info)
    await bot.send_message(
        chat_id=user,
        text=txt,
        reply_markup=await settings_buttons()
    )
