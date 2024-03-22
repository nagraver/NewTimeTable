from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date, timedelta
from connection import institutes_arr, week_day
from logic import get_groups


async def main_buttons(mode):
    buttons = []
    key = [4, 8, 16][mode]
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

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def settings_buttons():
    inst_choice = InlineKeyboardButton(text="Институт", callback_data='i_choice')
    group_choice = InlineKeyboardButton(text="Группа", callback_data='g_choice')
    menu_choice = InlineKeyboardButton(text="Меню", callback_data='m_choice')
    schedule_choice = InlineKeyboardButton(text="Рассылка", callback_data='s_choice')
    return InlineKeyboardMarkup(inline_keyboard=[[inst_choice, group_choice], [menu_choice, schedule_choice]])


async def inst_buttons():
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in range(len(institutes_arr)):
        markup.inline_keyboard.append([InlineKeyboardButton(text=institutes_arr[i], callback_data='inst' + str(i))])
    return markup


async def group_buttons(inst):
    groups = await get_groups(inst)
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in range(0, len(groups), 2):
        group1 = groups[i]['group_name']
        group2 = groups[i - 1]['group_name']
        button1 = InlineKeyboardButton(text=group1, callback_data='group' + str(group1))
        button2 = InlineKeyboardButton(text=group2, callback_data='group' + str(group2))
        markup.inline_keyboard.append([button1, button2])
    return markup


async def menu_buttons():
    four_days = InlineKeyboardButton(text='4 дня', callback_data='mode0')
    week = InlineKeyboardButton(text='8 дней', callback_data='mode1')
    fortnight = InlineKeyboardButton(text='16 дней', callback_data='mode2')
    return InlineKeyboardMarkup(inline_keyboard=[[four_days, week, fortnight]])


async def time_buttons():
    button = InlineKeyboardButton(text='Отключи отправку', callback_data='off_schedule')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


