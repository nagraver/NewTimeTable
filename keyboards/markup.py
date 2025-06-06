from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date, timedelta
from storage.lists import institutes_arr, week_day
from logic.get_dict import get_groups

settings = InlineKeyboardButton(text='Настройки', callback_data='settings')


async def main_buttons(mode):
    buttons = []
    key = mode
    i = 1
    while i < key:
        day_l = date.today() + timedelta(days=i - 1)
        day_r = date.today() + timedelta(days=i)
        i += 2
        if day_l.weekday() == 6:
            day_l += timedelta(days=1)
            day_r += timedelta(days=1)
            i += 1
            key += 1
        elif day_r.weekday() == 6:
            day_r += timedelta(days=1)
            i += 1
            key += 1

        buttons.append(
            [
                InlineKeyboardButton(text=f'{week_day(day_l)} {day_l.strftime("%d.%m")}',
                                     callback_data='day' + str(day_l)),
                InlineKeyboardButton(text=f'{week_day(day_r)} {day_r.strftime("%d.%m")}',
                                     callback_data='day' + str(day_r))
            ]
        )
    buttons.append([settings])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def settings_buttons(user):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Институт", callback_data='i_choice'),
                InlineKeyboardButton(text="Группа", callback_data='g_choice')
            ],
            [
                InlineKeyboardButton(text="Меню", callback_data='m_choice'),
                InlineKeyboardButton(text="Рассылка", callback_data='s_choice')
            ],
            [
                InlineKeyboardButton(text="Перейти к расписанию", callback_data="day" + str(date.today()))
            ]
        ]
    )

    if user == "1418418793":
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(text="Админ панель", callback_data='mailing')
            ]
        )

    return markup


async def inst_buttons():
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in range(len(institutes_arr)):
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(text=institutes_arr[i], callback_data='inst' + str(i))
            ]
        )
    markup.inline_keyboard.append(
        [settings]
    )
    return markup


async def group_buttons(inst):
    groups = await get_groups(inst)
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in range(0, len(groups), 2):
        group1 = groups[i]['group_name']
        group2 = groups[i - 1]['group_name']
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(text=group1, callback_data='group' + str(group1)),
                InlineKeyboardButton(text=group2, callback_data='group' + str(group2))
            ]
        )
    markup.inline_keyboard.append(
        [settings]
    )
    return markup


async def menu_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='4', callback_data='mode4'),
                InlineKeyboardButton(text='8', callback_data='mode8'),
                InlineKeyboardButton(text='16', callback_data='mode16')
            ],
            [
                settings
            ]
        ]
    )


async def time_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отключить рассылку', callback_data='off_schedule')
            ],
            [
                InlineKeyboardButton(text='На сегодня', callback_data='s_today'),
                InlineKeyboardButton(text='На завтра', callback_data='s_tomorrow')
            ],
            [
                settings
            ]
        ]
    )


async def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[[settings]])
