from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.start import request_phone
from loader import dp
from states.start import RegisterState
from utils.db_api.database import User


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await RegisterState.phone_number.set()
    await message.answer("Привет!\nДля регистрации нам нужны твои контакты. Нажми кнопку", reply_markup=request_phone)


@dp.message_handler(content_types=["contact"], state=RegisterState.phone_number)
async def bot_start_phone_number(message: types.Message, state: FSMContext):
    await User.get_or_create(id=message.from_user.id, full_name=message.from_user.full_name,
                             username=message.from_user.username, phone_number=message.contact.phone_number)
    await state.reset_state()
    await message.answer("Спасибо! Вы добавлены в список пользователей.")
