from .answer import answer_question, answer_questions, answer_questions_dict
from .export import export


def activity(export_to, file_name, questions, column_list=None, **kwargs):
    answer = ""
    if type(questions) is str:
        answer = answer_question(questions, **kwargs)
    elif type(questions) is list:
        answer = answer_questions(questions, **kwargs)
    elif type(questions) is dict:
        answer = answer_questions_dict(questions)
        questions = list(questions.keys())
    if not column_list:
        column_list = questions
    export(export_to, file_name, answer, column_list)
    return answer
