from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.default.start import TESTS_BUTTON
from keyboards.inline.callback_data import test_callback, tests_callback, start_test_callback, question_callback, \
    choose_answer_callback, finish_test_callback, choose_non_active_answer_callback
from keyboards.inline.tests import tests_keyboard, test_keyboard, question_keyboard
from loader import dp
from utils.db_api.database import Test, Result, Question, Answer, UserAnswer
from utils.misc.tests import get_prev_and_next_question_id


@dp.message_handler(text=TESTS_BUTTON)
@dp.message_handler(commands=["tests"])
async def bot_tests_command(message: types.Message):
    tests = await Test.all()
    user_result_ids = [result[0] for result in
                       await Result.filter(Result.user_id == message.from_user.id, select_values=['test_id'])]
    await message.answer(text="🧑🏻‍🏫 Выбери тест из списка ниже:",
                         reply_markup=tests_keyboard(tests=tests, user_result_ids=user_result_ids))


@dp.callback_query_handler(tests_callback.filter())
async def bot_tests_callback(call: CallbackQuery, callback_data: dict):
    tests = await Test.all()
    user_result_ids = [result[0] for result in
                       await Result.filter(Result.user_id == call.from_user.id, select_values=['test_id'])]
    await call.message.edit_text(text="🧑🏻‍🏫 Выбери тест из списка ниже:",
                                 reply_markup=tests_keyboard(tests=tests, user_result_ids=user_result_ids))


@dp.callback_query_handler(test_callback.filter())
async def bot_test_callback(call: CallbackQuery, callback_data: dict):
    test = await Test.get(Test.id == int(callback_data['test_id']))
    user_result = await Result.get(Result.user_id == call.from_user.id, Result.test_id == int(callback_data['test_id']))
    results = [result[0] for result in await Result.filter(Result.test_id == int(callback_data['test_id']),
                                                           select_values=['result'])]
    avg_result = int(sum(results) / len(results)) if results else None

    short_info_text = f"Тест был пройден {len(results)} раз\n"
    if avg_result:
        short_info_text += f"Средний результат: {avg_result}%\n"

    if user_result:
        text = f"✔️ <b>{test.name}</b>\n\n{short_info_text}\nТест пройден на {user_result.result}%\n"
    else:
        text = f"🧑🏻‍🏫 <b>{test.name}</b>\n\n{short_info_text}\n"

    await call.message.edit_text(text=text, reply_markup=test_keyboard(test_id=test.id, is_passed=bool(user_result),
                                                                       for_admin=call.from_user.id in ADMINS))


@dp.callback_query_handler(question_callback.filter())
async def bot_test_question_callback(call: CallbackQuery, callback_data: dict):
    question = await Question.get(Question.id == int(callback_data['question_id']))
    user_result = await Result.get(Result.user_id == call.from_user.id, Result.test_id == question.test_id)
    questions = await Question.filter(Question.test_id == question.test_id, select_values=['id'])
    answers = await Answer.filter(Answer.question_id == question.id)
    user_answer_id = await UserAnswer.get(UserAnswer.user_id == call.from_user.id,
                                          UserAnswer.question_id == question.id, select_values=['answer_id'])
    user_answer_id = user_answer_id[0] if user_answer_id else None
    question_number = [index + 1 for index, value in enumerate(questions) if question.id == value[0]][0]
    prev_question_id, next_question_id = get_prev_and_next_question_id(question_id=question.id, questions=questions)

    answers_text = '\n'.join(f"{index + 1}. {answer.text}" for index, answer in enumerate(answers))

    await call.message.edit_text(text=f"{question_number}. {question.text}\n\n{answers_text}",
                                 reply_markup=question_keyboard(test_id=question.test_id, answers=answers,
                                                                user_answer_id=user_answer_id,
                                                                prev_question_id=prev_question_id,
                                                                next_question_id=next_question_id,
                                                                is_passed=bool(user_result)))


@dp.callback_query_handler(start_test_callback.filter())
async def bot_test_start_callback(call: CallbackQuery, callback_data: dict):
    questions = await Question.filter(Question.test_id == int(callback_data['test_id']), select_values=['id'])

    await bot_test_question_callback(call=call, callback_data={"question_id": questions[0][0]})


@dp.callback_query_handler(choose_answer_callback.filter())
async def bot_test_choose_answer_callback(call: CallbackQuery, callback_data: dict):
    answer = await Answer.get(Answer.id == int(callback_data["answer_id"]))
    question = await Question.get(Question.id == answer.question_id)
    user_result = await Result.get(Result.user_id == call.from_user.id, Result.test_id == question.test_id)
    answers = await Answer.filter(Answer.question_id == question.id)
    user_answer = await UserAnswer.get(UserAnswer.user_id == call.from_user.id, UserAnswer.question_id == question.id)
    questions = await Question.filter(Question.test_id == question.test_id, select_values=['id'])
    prev_question_id, next_question_id = get_prev_and_next_question_id(question_id=question.id, questions=questions)

    if not user_result:
        if user_answer:
            await user_answer.update(answer_id=answer.id).apply()
        else:
            await UserAnswer.create(user_id=call.from_user.id, question_id=question.id, answer_id=answer.id)

    if next_question_id is None:
        await call.message.edit_reply_markup(reply_markup=question_keyboard(test_id=question.test_id, answers=answers,
                                                                            user_answer_id=answer.id,
                                                                            prev_question_id=prev_question_id,
                                                                            next_question_id=next_question_id,
                                                                            is_passed=bool(user_result)))
    else:
        await bot_test_question_callback(call=call, callback_data={"question_id": next_question_id})


@dp.callback_query_handler(finish_test_callback.filter())
async def bot_test_finish_callback(call: CallbackQuery, callback_data: dict):
    test = await Test.get(Test.id == int(callback_data['test_id']))
    questions = [question[0] for question in await Question.filter(Question.test_id == test.id, select_values=['id'])]
    user_answers = await UserAnswer.filter(UserAnswer.user_id == call.from_user.id,
                                           UserAnswer.question_id.in_(questions))
    user_result = await Result.get(Result.user_id == call.from_user.id, Result.test_id == test.id)

    if len(questions) > len(user_answers):
        return await call.answer("🧑🏻‍🏫 Для завершения теста нужно ответить на все вопросы!")

    if user_result:
        return await call.answer("🧑🏻‍🏫 Тест уже пройден!")

    count_of_right_answers = 0

    for user_answer in user_answers:
        answer = await Answer.get(Answer.id == user_answer.answer_id)
        if answer.is_right:
            count_of_right_answers += 1

    await Result.create(user_id=call.from_user.id, test_id=test.id,
                        result=int(count_of_right_answers / len(questions) * 100))

    await bot_test_callback(call=call, callback_data={"test_id": test.id})


@dp.callback_query_handler(choose_non_active_answer_callback.filter())
async def bot_test_choose_non_active_answer_callback(call: CallbackQuery, callback_data: dict):
    await call.answer("🧑🏻‍🏫 Нельзя изменить ответ, тест уже пройден!")
