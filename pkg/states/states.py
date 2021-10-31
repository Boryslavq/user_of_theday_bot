from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeText(StatesGroup):
    add_text = State()
