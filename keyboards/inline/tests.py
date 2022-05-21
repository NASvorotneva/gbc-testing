from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import test_callback, start_test_callback, tests_callback, choose_answer_callback, \
    choose_non_active_answer_callback, question_callback, finish_test_callback, check_test_results_callback, \
    delete_test_callback
from utils.db_api.database import Test, Answer


def tests_keyboard(tests: List[Test], user_result_ids: List[int]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for test in tests:
        button_text = test.name
        if test.id in user_result_ids:
            button_text = f"✔️ {test.name}"
        keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=test_callback.new(test_id=test.id))
        )
    return keyboard


def test_keyboard(test_id: int, is_passed: bool, for_admin: bool):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if is_passed:
        start_button_text = "Мои ответы"
    else:
        start_button_text = "Пройти тест"

    keyboard.add(
        InlineKeyboardButton(text=start_button_text, callback_data=start_test_callback.new(test_id=test_id))
    )

    if for_admin:
        keyboard.add(InlineKeyboardButton(text="📑 Просмотреть результаты",
                                          callback_data=check_test_results_callback.new(test_id=test_id)))
        keyboard.add(InlineKeyboardButton(text="❌ Удалить", callback_data=delete_test_callback.new(test_id=test_id)))

    keyboard.add(InlineKeyboardButton(text="🔙", callback_data=tests_callback.new()))
    return keyboard


def question_keyboard(
        test_id: int, answers: List[Answer], user_answer_id: int, prev_question_id: int, next_question_id: int,
        is_passed: bool
):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for answer in answers:
        if is_passed and answer.is_right:
            button_text = f"✅ {answer.text}"
        elif is_passed and answer.id == user_answer_id and not answer.is_right:
            button_text = f"❌ {answer.text}"
        elif answer.id == user_answer_id:
            button_text = f"✔️ {answer.text}"
        else:
            button_text = answer.text
        keyboard.add(
            InlineKeyboardButton(
                text=button_text,
                callback_data=choose_non_active_answer_callback.new() if is_passed else
                choose_answer_callback.new(answer_id=answer.id)
            )
        )

    nav_buttons = []
    if prev_question_id:
        nav_buttons.append(
            InlineKeyboardButton(text="🔙", callback_data=question_callback.new(question_id=prev_question_id))
        )
    else:
        nav_buttons.append(InlineKeyboardButton(text="🔙", callback_data=test_callback.new(test_id=test_id)))
    if next_question_id:
        nav_buttons.append(
            InlineKeyboardButton(text="🔜", callback_data=question_callback.new(question_id=next_question_id))
        )
    elif not is_passed:
        nav_buttons.append(
            InlineKeyboardButton(text="🏁", callback_data=finish_test_callback.new(test_id=test_id))
        )
    keyboard.row(*nav_buttons)

    return keyboard
