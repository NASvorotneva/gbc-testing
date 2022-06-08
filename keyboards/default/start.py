from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

REQUEST_PHONE_BUTTON = '☎️ Отправить свой контакт'

TESTS_BUTTON = '⏱ Тесты'

request_phone = ReplyKeyboardMarkup(
    [
        [KeyboardButton(REQUEST_PHONE_BUTTON, request_contact=True)]

    ],
    resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton(TESTS_BUTTON)]

    ],
    resize_keyboard=True
)
