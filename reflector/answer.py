import re

from config import settings


def answer_questions_dict(questions_dict):
    answer_list = []
    for question, answer_setting in questions_dict.items():
        answer = answer_question(question, **answer_setting)
        answer_list.append(answer)
    return answer_list


def answer_questions(question_list, answer_type, show_question_index=False, **kwargs):
    all_answer_list = []
    for question in question_list:
        if show_question_index:
            question += create_question_index_suffix(question, question_list)
        question_answer = answer_question(question, answer_type, **kwargs)
        all_answer_list.append(question_answer)
    return all_answer_list


def create_question_index_suffix(question, question_list):
    question_index_suffix = f' ({question_list.index(question) + 1} out of {len(question_list)})'
    return question_index_suffix


def answer_question(question, answer_type, **kwargs):
    answer = ''  # Just to temporarily resolve answer unbound error until I find better solution
    if answer_type == 'inline':
        answer = answer_question_as_inline(question, **kwargs)
    elif answer_type == 'text':
        answer = answer_question_as_text(question)
    elif answer_type == 'list':
        answer = answer_question_as_list(question, '• ', **kwargs)
    determine_linebreak(answer_type)
    return answer


def answer_question_as_inline(question, yesno=False, choice_list=None, display_choice_list=None, spacer='/'):
    if yesno:
        answer = answer_as_yesno(question)
    elif choice_list:
        answer = answer_as_inline_choice(question, choice_list, display_choice_list, spacer)
    else:
        answer = answer_as_inline(question)
    return answer


def answer_as_yesno(question):
    answer = answer_as_inline_choice(question, ['yes', 'y', 'no', 'n'], display_choice_list=['y', 'n'], spacer='/')
    return answer


def answer_as_inline_choice(question, choice_list, display_choice_list=None, spacer="/"):
    validate_choice_lists(choice_list, display_choice_list)
    question += create_choice_help_text(choice_list, display_choice_list, spacer)
    answer = answer_as_inline(question)
    validate_choice(answer, choice_list)
    return answer


def validate_choice_lists(choice_list, display_choice_list):
    validate_choice_list(choice_list)
    validate_display_choice_list(display_choice_list)


def validate_choice_list(choice_list):
    if len(choice_list) <= 1:
        feedback = create_choice_list_error_feedback(choice_list)
        help_text = f'choice_list must contain AT LEAST 2 items {feedback}'
        raise ValueError(help_text)


def validate_display_choice_list(display_choice_list):
    if display_choice_list and len(display_choice_list) <= 1:
        feedback = create_choice_list_error_feedback(display_choice_list)
        help_text = f'display_choice_list must contain AT LEAST 2 items {feedback}'


def create_choice_list_error_feedback(choice_list):
    feedback = f'(currently contains {len(choice_list)}'
    return feedback


def create_choice_help_text(choice_list, display_choice_list, spacer):
    choice_list = display_choice_list if display_choice_list else choice_list
    choice_help_text = f' ({spacer.join(choice_list)})'
    return choice_help_text


def answer_as_inline(input_prefix):
    answer = input(f'{input_prefix}: ')
    return answer


def validate_choice(answer, choice_list):
    answer, choice_list = casefold_all(answer, choice_list)
    error = 'Invalid answer.'
    help_text = create_choice_error_help_text(choice_list)
    error_message = f'{error} {help_text}'
    if answer and answer not in choice_list:
        raise ValueError(error_message)


def casefold_all(*vars) -> list:
    return_list = []
    for var in vars:
        if var and type(var) is str:
            return_list.append(var.casefold())
        elif var and type(var) in {list, tuple, set}:
            return_list.append(list(map(str.casefold, var)))
        else:
            return_list.append(var)
    return return_list


def create_choice_error_help_text(choice_list):
    if len(choice_list) == 1:
        help_text = f'Available choice is {choice_list[0]}.'
    elif len(choice_list) == 2:
        help_text = f'Available choices are either {choice_list[0]} or {choice_list[1]}.'
    else:
        help_text = f'Available choices are {", ".join(choice_list[:-1])}, or {choice_list[-1]}.'
    return help_text


def answer_question_as_text(question):
    print(question)
    help_text = '(linebreaks are enabled. To end reflection, press "." on a new line and press enter)'
    print(help_text)
    answer = answer_as_text()
    return answer


def answer_as_text():
    answer_list = []
    while True:
        answer = input('')
        answer = '\n' if not answer else answer
        if answer == '.':
            break
        answer_list.append(answer)
    text_answer = '\n'.join(answer_list)
    return text_answer


def answer_question_as_list(question, input_prefix='• ', ordered=False, cap=None, input_suffix=''):
    if cap == 'auto':
        cap = get_cap_in_answer_prefix(question)
    if cap and not ordered:
        answer_list = answer_as_list(question, ordered, cap, input_suffix)
    else:
        print(question)
        answer_list = answer_as_list(input_prefix, ordered, cap, input_suffix)
    return answer_list


def answer_as_list(input_prefix, ordered=False, cap=None, input_suffix=''):
    answer_list = []
    validate_list_answer_cap(cap)
    if cap == 'auto':
        cap = get_cap_in_answer_prefix(input_prefix)
    while len(answer_list) != cap if cap else True:
        i = len(answer_list) + 1
        answer_prefix = create_list_answer_prefix(input_prefix, i, ordered, cap, input_suffix)
        answer = input(answer_prefix)
        if not answer:
            break
        answer_list.append(answer)
    return answer_list


def create_list_answer_prefix(input_prefix, iteration, ordered, cap, input_suffix):
    cap_suffix = create_cap_suffix(iteration, cap)
    if ordered:
        answer_prefix = f'{cap_suffix}. ' if cap else f'{iteration}. '
    elif cap:
        answer_prefix = f'{input_prefix} ({cap_suffix}): '
    else:
        answer_prefix = input_prefix
    if input_suffix:
        answer_prefix += input_suffix
    return answer_prefix


def create_cap_suffix(iteration, cap):
    cap_suffix = f'{iteration} in {cap}' if cap else None
    return cap_suffix


def get_cap_in_answer_prefix(answer_prefix):
    pattern = "\d+"  # TODO: Make Regex ignore inside of parenthesis "(...)"
    regex = re.compile(pattern)
    match = regex.search(answer_prefix)
    answer_cap = int(match.group()) if match else None
    return answer_cap


def validate_list_answer_cap(cap):
    help_text = 'cap must be set to \'auto\' or an integer greater than or equal to 1.'
    if (type(cap) is int and cap < 1) or (type(cap) is str and cap != 'auto'):
        raise ValueError(help_text)


def determine_linebreak(answer_type):
    if answer_type in {'text', 'list'}:
        print()










