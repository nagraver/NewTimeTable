from connection.connections import col

from logic.append_data import append_data
from connection.data import user_list
from connection.connections import bot
from markup.markup import inst_buttons, group_buttons, menu_buttons


async def check_parameter(parameter, user, message, markup):
    if parameter is None:
        await bot.send_message(user, message, reply_markup=markup)
        raise ValueError


async def check_user_id(user):
    for item in user_list:
        if item.get('_id') == user:
            await check_parameter(item.get('inst'), user, "Выбери институт", await inst_buttons())
            await check_parameter(item.get('group'), user, "Выбери группу", await group_buttons(item.get('inst')))
            await check_parameter(item.get('mode'), user, "Выбери меню", await menu_buttons())
            return item

    col.insert_one({'_id': user, 'mode': 0})
    await append_data(user_list)
    await bot.send_message(user, "Выбери институт", reply_markup=await inst_buttons())
    raise ValueError
