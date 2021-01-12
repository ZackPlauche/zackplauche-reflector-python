from datetime import datetime


def casefold_all(*vars) -> tuple:
    casefolded_vars_list = []
    for var in vars:
        if type(var) is str:
            casefolded_vars_list.append(var.casefold())
        elif type(var) in {list, tuple, set}:
            casefolded_vars_list.append(list(map(str.casefold, var)))
    return tuple(casefolded_vars_list)


def get_datetime_now_vars():
    date = datetime.now().strftime('%#m/%#d/%Y')
    day = datetime.now().strftime('%A')
    time = datetime.now().strftime('%I:%H %p').lstrip('0').lower()
    return date, day, time


def get_integrity_status(yesno_question_list, yesno_answer_list):
    integrity_slice = 100 / len(yesno_question_list)
    integrity = sum([integrity_slice for answer in yesno_answer_list if answer in {'y', 'yes'}]).__int__()
    integrity_status = f'{integrity}%'
    return integrity_status


def debug(*args):
    print('DEBUG: ', *args)
