import re

from config import settings
from .utils import casefold_all

__all__ = ['answer_question', 'answer_questions', 'answer_question_dict']


def _answer_as_inline(input_prefix):
    answer = input(f'{input_prefix}: ')
    return answer


def _create_choice_error_help_text(choice_list):
    if len(choice_list) == 1:
        help_text = f'Available choice is {choice_list[0]}.'
    elif len(choice_list) == 2:
        help_text = f'Available choices are either {choice_list[0]} or {choice_list[1]}.'
    else:
        help_text = f'Available choices are {", ".join(choice_list[:-1])}, or {choice_list[-1]}.'
    return help_text

def _create_choice_list_error_feedback(choice_list):
    feedback = f'(currently contains {len(choice_list)}'
    return feedback


def _validate_choice_list(choice_list):
    if len(choice_list) <= 1:
        feedback = _create_choice_list_error_feedback(choice_list)
        help_text = f'choice_list must contain AT LEAST 2 items {feedback}'
        raise ValueError(help_text)

def _validate_display_choice_list(display_choice_list):
    if display_choice_list and display_choice_list <= 1:
        feedback = _create_choice_list_error_feedback(display_choice_list)
        help_text = f'display_choice_list must contain AT LEAST 2 items {feedback}'

def _validate_choice_lists(choice_list, display_choice_list):
    _validate_choice_list(choice_list)
    _validate_display_choice_list(display_choice_list)


def _create_choice_help_text(choice_list, display_choice_list, spacer):
    choice_list = display_choice_list if display_choice_list else choice_list
    choice_help_text = f' ({spacer.join(choice_list)})'
    return choice_help_text


def _validate_answer_choice(answer, choice_list):
    answer, choice_list = casefold_all(answer, choice_list)
    error = 'Invalid answer.'
    help_text = _create_choice_error_help_text(choice_list)
    error_message = f'{error} {help_text}'
    if answer and answer not in choice_list:
        raise ValueError(error_message)


def _answer_as_inline_choice(question, choice_list, display_choice_list=None, spacer="/"):
    _validate_choice_lists(choice_list, display_choice_list)
    question += _create_choice_help_text(choice_list, display_choice_list, spacer)
    answer = _answer_as_inline(question)
    _validate_answer_choice(answer, choice_list)
    return answer


def _answer_as_yesno(question):
    answer = _answer_as_inline_choice(question, ['yes', 'y', 'no', 'n'], display_choice_list=['y', 'n'], spacer='/')
    return answer


def _answer_question_as_inline(question, yesno=False, choice_list=None, display_choice_list=None, spacer='/'):
    if yesno:
        answer = _answer_as_yesno(question)
    elif choice_list:
        answer = _answer_as_inline_choice(question, choice_list, display_choice_list, spacer)
    else:
        answer = _answer_as_inline(question)
    return answer


def _validate_list_answer_cap(cap):
    help_text = 'cap must be set to \'auto\' or an integer greater than or equal to 1.'
    if (type(cap) is int and cap < 1) or (type(cap) is str and cap != 'auto'):
        raise ValueError(help_text)


def _get_cap_in_answer_prefix(answer_prefix):
    pattern = "\d+"  # TODO: Make Regex ignore inside of parenthesis "(...)"
    regex = re.compile(pattern)
    match = regex.search(answer_prefix)
    answer_cap = int(match.group()) if match else None
    return answer_cap


def _create_cap_suffix(iteration, cap):
    cap_suffix = f'{iteration} in {cap}' if cap else None
    return cap_suffix


def _create_list_answer_prefix(input_prefix, iteration, ordered, cap, input_suffix):
    cap_suffix = _create_cap_suffix(iteration, cap)
    if ordered:
        answer_prefix = f'{cap_suffix}. ' if cap else f'{iteration}. '
    elif cap:
        answer_prefix = f'{input_prefix} ({cap_suffix}): '
    else:
        answer_prefix = input_prefix
    if input_suffix:
        answer_prefix += input_suffix
    return answer_prefix


def _answer_as_list(input_prefix, ordered=False, cap=None, input_suffix=''):
    answer_list = []
    _validate_list_answer_cap(cap)
    if cap == 'auto':
        cap = _get_cap_in_answer_prefix(input_prefix)
    while len(answer_list) != cap if cap else True:
        i = len(answer_list) + 1
        answer_prefix = _create_list_answer_prefix(input_prefix, i, ordered, cap, input_suffix)
        answer = input(answer_prefix)
        if not answer:
            break
        answer_list.append(answer)
    return answer_list


def _answer_question_as_list(question, input_prefix='• ', ordered=False, cap=None, input_suffix=''):
    if cap == 'auto':
        cap = _get_cap_in_answer_prefix(question)
    if cap and not ordered:
        answer_list = _answer_as_list(question, ordered, cap, input_suffix)
    else:
        print(question)
        answer_list = _answer_as_list(input_prefix, ordered, cap, input_suffix)
    return answer_list


def _answer_as_text():
    answer_list = []
    while True:
        answer = input('')
        answer = '\n' if not answer else answer
        if answer == '.':
            break
        answer_list.append(answer)
    text_answer = '\n'.join(answer_list)
    return text_answer


def _answer_question_as_text(question):
    print(question)
    help_text = '(linebreaks are enabled. To end reflection, press "." on a new line and press enter)'
    print(help_text)
    answer = _answer_as_text()
    return answer


def determine_linebreak(answer_type):
    if answer_type in {'text', 'list'}:
        print()


def answer_question(question, answer_type, **kwargs):
    answer = ''  # Just to temporarily resolve answer unbound error until I find better solution
    if answer_type == 'inline':
        answer = _answer_question_as_inline(question, **kwargs)
    elif answer_type == 'text':
        answer = _answer_question_as_text(question)
    elif answer_type == 'list':
        answer = _answer_question_as_list(question, '• ', **kwargs)
    determine_linebreak(answer_type)
    return answer


def _create_question_index_suffix(question, question_list):
    question_index_suffix = f' ({question_list.index(question) + 1} out of {len(question_list)})'
    return question_index_suffix


def answer_questions(question_list, answer_type, show_question_index=False, **kwargs):
    all_answer_list = []
    for question in question_list:
        if show_question_index:
            question += _create_question_index_suffix(question, question_list)
        question_answer = answer_question(question, answer_type, **kwargs)
        all_answer_list.append(question_answer)
    return all_answer_list


def answer_question_dict(question_dict):
    answer_list = []
    for question, answer_setting in question_dict.items():
        answer = answer_question(question, **answer_setting)
        answer_list.append(answer)
    return answer_list
