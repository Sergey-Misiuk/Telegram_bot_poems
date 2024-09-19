from aiogram.fsm.state import StatesGroup, State


class Reg_poem(StatesGroup):
    title = State()
    text = State()
