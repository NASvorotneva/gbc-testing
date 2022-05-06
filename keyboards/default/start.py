from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

request_phone = ReplyKeyboardMarkup(
    [

        [KeyboardButton('Отправить свой контакт ☎️', request_contact=True)]

    ], resize_keyboard=True)
