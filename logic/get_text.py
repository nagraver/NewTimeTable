from storage.lists import week_day, time_list, institutes_arr
from logic.get_dict import get_schedule
from datetime import datetime, date


async def settings_text(user_info):
    inst = user_info.get('inst')
    inst = institutes_arr[int(inst)] if inst is not None else None
    group = user_info.get('group')
    mode = user_info.get('mode')
    send = user_info.get('send')

    txt = f'*Институт:* _{inst}_\n*Группа:* _{group}_\n*Меню:* _{(mode + 1) * 4}_\n*Рассылка:* _{send}_'
    return txt


async def schedule_text(user_info, the_day):
    inst = user_info.get('inst')
    group = user_info.get('group')
    array = await get_schedule(inst, group, the_day)
    if array is None:
        return "Непредвиденная ошибка"

    message = f"_{week_day(the_day)}, {the_day.strftime('%d.%m.%y')}, {group}_"
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

    return message
