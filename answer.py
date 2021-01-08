def _create_choice_help_text(choices: list):
    if len(choices) == 1:
        help_text = f'Available choice is {choices[0]}.'
    elif len(choices) == 2:
        help_text = f'Available choices are either {choices[0]} or {choices[1]}.'
    else:
        help_text = f'Available choices are {", ".join(choices[:-1])} or {choices[-1]}'
    return help_text


def _validate_choice_answer(answer: str, choices: list):
    valid_answers = map(str.casefold, choices)
    help_text = _create_choice_help_text(choices)

    if answer and answer not in valid_answers:
        raise ValueError(f'Invalid answer. {help_text}')


def answer_question_as_inline(question, yesno=False):
    question += ' (y/n)' if yesno else question
    answer = input(f'{question}:')
    if yesno:
        _validate_choice_answer(answer, ['yes', 'y', 'no', 'n'])
    return answer


def _validate_list_answer_cap(cap):
    if cap < 1:
        raise ValueError('cap must be more than or equal to 1')


def _get_cap_in_answer_prefix(answer_prefix):
    pattern = "\d+"
    regex = re.compile(pattern)
    match = regex.search(answer_prefix).group()
    answer_cap = int(match) if match else False
    return answer_cap


def _create_cap_suffix(iteration, cap):
    cap_suffix = f'{iteration} in {cap}' if cap else None
    return cap_suffix


def _create_list_answer_prefix(input_prefix, iteration, ordered, cap):
    cap_suffix = _create_cap_suffix(iteration, cap)
    if ordered:
        answer_prefix = f'{cap_suffix}. ' if cap else f'{iteration}. '
    else:
        answer_prefix = f'{input_prefix} {cap_suffix}:' if cap else input_prefix
    return answer_prefix


def _answer_as_list(input_prefix, ordered=False, cap=None):
    answer_list = []
    if type(cap) is int:
        _validate_list_answer_cap(cap)
    cap = _get_cap_in_answer_prefix(input_prefix) if cap and cap == 'auto' else cap
    while True if not cap else len(answer_list) != cap:
        i = len(answer_list + 1)
        answer_prefix = _create_list_answer_prefix(input_prefix, i, ordered, cap)
        answer = input(answer_prefix)
        answer_list.append(answer)
    return answer_list


def answer_question_as_list(question, input_prefix, ordered=False, cap=None):
    if cap:
        answer_list = _answer_as_list(question, ordered, cap)
    else:
        print(question)
        answer_list = _answer_as_list(input_prefix, ordered, cap)
    return answer_list


def _answer_as_text():
    answer_list = []
    while True:
        answer = input('')
        answer = '\n' if not answer else answer
        if answer == '.':
            break
        answer_list.append()
    text_answer = '\n'.join(answer_list)
    return text_answer


def answer_question_as_text(question):
    print(question)
    answer = _answer_as_text()
    return answer


def _validate_required_choice_answer(answer: str, choices: list):
    valid_answers = map(str.casefold, choices)
    help_text = _create_choice_help_text(choices)

    if not answer:
        raise ValueError(f'Answer must not be left blank. {help_text}.')

    elif answer.casefold not in valid_answers:
        raise ValueError(f'Invalid answer. {help_text} or left blank.')


def _validate_required_answer(answer: str):
    if not answer:
        raise ValueError(f'Answer must not be left blank.')


def answer_question(question, answer_type, **kwargs):
    if answer_type == 'oneoff':
        answer = answer_question_as_inline(question, kwargs.get('yesno'))
    elif answer_type == 'text':
        answer = answer_question_as_text(question)
    elif answer_type == 'list':
        answer = answer_question_as_list(question, '• ', kwargs.get('ordered'), kwargs.get('cap'))
    return answer


def _create_question_index_suffix(question, question_list):
    question_index_suffix = f' ({question.index(question_list + 1)} out of {len(question_list)})'
    return question_index_suffix


def answer_question_list(question_list, answer_type='text', show_question_index=False, **kwargs):
    all_answer_list = []
    for question in question_list:
        if kwargs.get('question_index'):
            question += _create_question_index_suffix(question, question_list)
        answer = answer_question(question, answer_type, kwargs)
        all_answer_list.append(answer)
    return all_answer_list