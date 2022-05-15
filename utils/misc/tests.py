from typing import List, Tuple


def get_prev_and_next_question_id(question_id: int, questions: List[Tuple[int]]):
    if questions[0][0] == question_id:
        prev_question_id = None
    else:
        prev_question_id = [value for index, value in enumerate(questions) if value[0] < question_id][-1][0]

    if questions[-1][0] == question_id:
        next_question_id = None
    else:
        next_question_id = [value for index, value in enumerate(questions) if value[0] > question_id][0][0]
    return prev_question_id, next_question_id
