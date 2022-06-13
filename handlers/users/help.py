from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help_command(message: types.Message):
    text = (
        "Список команд:",
        "/start - Начать диалог",
        "/help - Получить справку",
        "/tests - Получить список доступных тестов",
    )

    await message.answer("\n".join(text))
