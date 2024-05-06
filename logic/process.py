from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from logic.get_dict import get_schedule
from keyboards.markup import inst_buttons, group_buttons, main_buttons
from storage.connection import bot, Mongo
from storage.lists import week_day, time_list, institutes_arr


db = Mongo()


async def process_the_message(user, the_day, msg=False):
    user_info = await db.get_user_info(user)
    inst = user_info.get('inst')
    group = user_info.get('group')
    mode = user_info.get('mode')

    if inst is None:
        markup = await inst_buttons()
        await process_the_settings(user, markup, include_institute=True)
        return
    elif group is None:
        inst = user_info.get('inst')
        markup = group_buttons(inst)
        await process_the_settings(user, markup, include_group=True)
        return

    array = await get_schedule(inst, group, the_day)
    if array is None:
        await bot.send_message(user, "Проверь соответствие института и группы")
        return

    message = f"_{week_day(the_day)}, {the_day.strftime('%d.%m.%y')}, {group}_"
    flag = True
    prev_lesson, prev_date, prev_n = None, None, None

    for item in array:
        formatted_date = datetime.strptime(item['date'], "%d.%m.%Y").date()
        if the_day == formatted_date:
            flag = False
            if item['n'] != prev_n or item['date'] != prev_date:
                message += f"\n\n*{time_list[item['n']]}*"
            if item['lesson'] != prev_lesson or item['n'] != prev_n:
                message += f"\n_{item['lesson']}_"
            if item['subgroup'] == '0':
                message += f"\n• {item['location']} | {item['type']}"
            else:
                message += f"\n• {item['location']} | {item['type']} | {item['subgroup']}"

            prev_date = item['date']
            prev_n = item['n']
            prev_lesson = item['lesson']

    if flag:
        message += f"\n\nЗанятий нет, либо расписание еще не появилось"

    if msg:
        try:
            await bot.edit_message_text(
                chat_id=user,
                message_id=msg,
                text=message,
                reply_markup=await main_buttons(mode)
            )
        except TelegramBadRequest:
            pass
    else:
        await bot.send_message(
            chat_id=user,
            text=message,
            reply_markup=await main_buttons(mode)
        )
    await db.update_data(user=user, usage=True)


async def process_the_settings(
        user, markup, msg=False, include_all=False,
        include_institute=False, include_group=False,
        include_mode=False, include_send=False):
    user_info = await db.get_user_info(user)

    inst = user_info.get('inst')
    inst = institutes_arr[int(inst)] if inst is not None else None
    group = user_info.get('group')
    mode = user_info.get('mode')
    send = user_info.get('send')
    send_day = user_info.get('send_day')
    send_day = ["сегодня", "завтра"][send_day] if send_day is not None else None

    txt = ""
    if include_institute:
        txt += f'\n*Институт:* _{inst}_'
    if include_group:
        txt += f"\n*Группа:* _{group}_"
    if include_mode:
        txt += f"\n*Меню:* _{(2 ** mode) * 4}_"
    if include_send:
        txt += (f"\n*Рассылка:* _{send} на {send_day}_"
                f"\n\nВведи время в формате ЧЧ:ММ")
    if include_all:
        txt = (f'*Институт:* _{inst}_\n'
               f'*Группа:* _{group}_\n'
               f'*Меню:* _{(2 ** mode) * 4}_\n'
               f'*Рассылка:* _{send} на {send_day}_')

    if msg:
        await bot.edit_message_text(
            chat_id=user,
            message_id=msg,
            text=txt,
            reply_markup=markup
        )
    else:
        await bot.send_message(
            chat_id=user,
            text=txt,
            reply_markup=markup
        )
