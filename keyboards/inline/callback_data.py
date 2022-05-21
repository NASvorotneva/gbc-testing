from aiogram.utils.callback_data import CallbackData

tests_callback = CallbackData("tests")
test_callback = CallbackData("test", "test_id")
start_test_callback = CallbackData("start_test", "test_id")
finish_test_callback = CallbackData("finish_test", "test_id")
question_callback = CallbackData("question", "question_id")
choose_answer_callback = CallbackData("choose_answer", "answer_id")
choose_non_active_answer_callback = CallbackData("choose_non_active_answer")
check_test_results_callback = CallbackData("check_test_results", "test_id")
delete_test_callback = CallbackData("delete_test", "test_id")
