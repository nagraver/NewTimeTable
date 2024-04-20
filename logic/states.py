from aiogram.fsm.state import State, StatesGroup


class Schedule(StatesGroup):
    text = State()
    mailing = State()
