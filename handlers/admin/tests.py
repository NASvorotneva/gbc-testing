from aiogram.types import CallbackQuery, InputFile

from handlers.users.tests import bot_tests_callback
from keyboards.inline.callback_data import check_test_results_callback, \
    delete_test_callback
from loader import dp
from utils.db_api.database import Test, Result, Question, Answer, UserAnswer
from utils.excel.results_exporter import export_test_results


@dp.callback_query_handler(check_test_results_callback.filter(), is_admin=True)
async def bot_test_check_results_callback(call: CallbackQuery, callback_data: dict):
    test = await Test.get(Test.id == int(callback_data['test_id']))
    bytes_io = await export_test_results(test=test)
    document = InputFile(path_or_bytesio=bytes_io, filename=f"{test.name}.xlsx")

    await call.message.answer_document(document=document)


@dp.callback_query_handler(delete_test_callback.filter(), is_admin=True)
async def bot_test_delete_callback(call: CallbackQuery, callback_data: dict):
    test = await Test.get(Test.id == int(callback_data['test_id']))
    question_ids = [question_id[0] for question_id in
                    await Question.filter(Question.test_id == test.id, select_values=['id'])]
    await UserAnswer.delete.where(UserAnswer.question_id.in_(question_ids)).gino.status()
    await Answer.delete.where(Answer.question_id.in_(question_ids)).gino.status()
    await Question.delete.where(Question.id.in_(question_ids)).gino.status()
    await Result.delete.where(Result.test_id == test.id).gino.status()
    await test.delete()

    await bot_tests_callback(call=call, callback_data=callback_data)
