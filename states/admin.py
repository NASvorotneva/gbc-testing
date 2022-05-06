from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateTestState(StatesGroup):
    test = State()
