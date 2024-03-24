from aiogram.fsm.state import State, StatesGroup


class UserInfo(StatesGroup):
    id = State()
    inst = State()
    group = State()
    mode = State()
    send = State()
