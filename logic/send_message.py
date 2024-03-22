from connection import bot, week_day, time_list, institutes_arr
from datetime import datetime
from markup import inst_buttons, group_buttons, menu_buttons, main_buttons, time_buttons, settings_buttons
from logic import get_schedule


async def send_inst_menu(user):
    await bot.send_message(user, "Выбери институт", reply_markup=await inst_buttons())


async def send_group_menu(user, inst):
    await bot.send_message(user, text='Выбери группу', reply_markup=await group_buttons(inst))


async def send_mode_menu(user):
    await bot.send_message(user, text="Выбери меню", reply_markup=await menu_buttons())


async def send_time_menu(user):
    await bot.send_message(user, text="Введи желаемое время для отправки расписания или",
                           reply_markup=await time_buttons())


async def send_main_menu(user, user_info, the_day):
    inst = user_info.get('inst')
    group = user_info.get('group')
    mode = user_info.get('mode')
    array = await get_schedule(inst, group, the_day)
    if array is None:
        return "Непредвиденная ошибка"

    message = f"_{week_day(the_day)}, {the_day.strftime('%d.%m.%y ')}, {group}_"
    flag = True
    prev_lesson, prev_date, prev_n = None, None, None

    for item in array:
        formatted_date = datetime.strptime(item['date'], "%d.%m.%Y").date()
        if the_day == formatted_date:  # and item['subgroup'] in sub
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

    await bot.send_message(user, text=message, reply_markup=await main_buttons(mode))


async def send_settings_menu(user, user_info):
    inst = user_info.get('inst')
    group = user_info.get('group')
    mode = user_info.get('mode')
    send = user_info.get('send')
    await bot.send_message(
        chat_id=user,
        text=f'*Институт:* _{institutes_arr[int(inst)]}_\n*Группа:* _{group}_\n*Меню:* _{(mode + 1) * 4}_\n*Рассылка:* _{send}_',
        reply_markup=await settings_buttons()
    )
