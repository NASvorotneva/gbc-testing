from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("tests", "Список доступных тестов"),
            types.BotCommand("create_test", "[АДМИН] Добавить новый тест"),
        ]
    )
