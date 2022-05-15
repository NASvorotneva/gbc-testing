from io import BytesIO

import openpyxl
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from handlers.users.tests import bot_tests_command
from loader import dp
from states.admin import CreateTestState
from utils.db_api.database import Test, Question, Answer
from utils.excel.test_parser import parse_tests


@dp.message_handler(commands=["create_test"], is_admin=True)
async def bot_create_test_command(message: Message):
    await CreateTestState.test.set()
    await message.answer("🧑🏻‍🏫 Загрузи тест в формате .xls/.xlsx")


@dp.message_handler(content_types=["document"], is_admin=True, state=CreateTestState.test)
async def bot_create_test_upload_file(message: Message, state: FSMContext):
    bytes_io = BytesIO()
    await message.document.download(destination=bytes_io)
    try:
        excel_file = openpyxl.load_workbook(filename=bytes_io)
        tests = parse_tests(excel_file=excel_file)
    except Exception:
        await message.answer("🧑🏻‍🏫 Что-то пошло не так, пришли файл заново")
    else:
        for test in tests:
            test_object = await Test.create(name=test.name)
            for question in test.questions:
                question_object = await Question.create(test_id=test_object.id, text=question.text)
                for answer in question.answers:
                    await Answer.create(question_id=question_object.id, text=answer.text, is_right=answer.is_right)
        await state.reset_state(with_data=True)
        await bot_tests_command(message)
