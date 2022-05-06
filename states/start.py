from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    phone_number = State()
