import re


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
    question = f'{question} (y/n)' if yesno else question
    answer = input(f'{question}: ')
    if yesno:
        _validate_choice_answer(answer, ['yes', 'y', 'no', 'n'])
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
        print('Auto')
        cap = _get_cap_in_answer_prefix(input_prefix)
        print(cap)

    while len(answer_list) != cap if cap else True:
        i = len(answer_list) + 1
        answer_prefix = _create_list_answer_prefix(input_prefix, i, ordered, cap, input_suffix)
        answer = input(answer_prefix)
        if not answer:
            break
        answer_list.append(answer)
    return answer_list


def answer_question_as_list(question, input_prefix='• ', ordered=False, cap=None, input_suffix=''):
    if cap == 'auto':
        cap = _get_cap_in_answer_prefix(question)
        print(cap)
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
        answer_list.append()
    text_answer = '\n'.join(answer_list)
    return text_answer


def answer_question_as_text(question):
    print(question)
    help_text = '(linebreaks are enabled. To end reflection, press "." on a new line and press enter)'
    print(help_text)
    answer = _answer_as_text()
    return answer


def answer(question, answer_type, **kwargs):
    if answer_type == 'inline':
        answer = answer_question_as_inline(question, kwargs.get('yesno'))
    elif answer_type == 'text':
        answer = answer_question_as_text(question)
    elif answer_type == 'list':
        answer = answer_question_as_list(question, '• ', kwargs.get('ordered'), kwargs.get('cap'), kwargs.get('input_suffix'))
    return answer


def _create_question_index_suffix(question, question_list):
    question_index_suffix = f' ({question_list.index(question) + 1} out of {len(question_list)})'
    return question_index_suffix


def answer_list(question_list, answer_type, show_question_index=False, **kwargs):
    all_answer_list = []
    for question in question_list:
        if show_question_index:
            question += _create_question_index_suffix(question, question_list)
        question_answer = answer(question, answer_type, **kwargs)
        all_answer_list.append(question_answer)
    return all_answer_list


def test():
    # x = answer_question_as_list('What did you do today?')
    # x = answer_question_as_list('What did you do today?', ordered=True)
    # x = answer_question_as_list('What did you do today?', cap=5)
    # x = answer_question_as_list('What did you do today?', input_suffix='Boiiiiii ')
    # x = answer_question_as_list('What did you do today?', ordered=True, cap=5)
    # x = answer_question_as_list('What did you do today?', cap='auto')
    # x = answer_question_as_list('What are your top 3 priorities?', cap='auto')
    # x = answer_question_as_list('What did you do today?', ordered=True, cap='auto')
    # x = answer_question_as_list('Top 3 priorities', ordered=True, cap='auto')
    # x = answer('What did you do today?', answer_type='list')
    # x = answer('What did you do today?', answer_type='list', ordered=True)
    # x = answer('What did you do today?', answer_type='list', cap=5)
    # x = answer('What did you do today?', answer_type='list', input_suffix='Boiiiiii ')
    # x = answer('What did you do today?', answer_type='list', ordered=True, cap=5)
    # x = answer('What did you do today?', answer_type='list', cap='auto')
    # x = answer('What are your top 3 priorities?', answer_type='list', cap='auto')
    # x = answer('What did you do today?', answer_type='list', ordered=True, cap='auto')
    # x = answer('Top 3 priorities', answer_type='list', ordered=True, cap='auto')
    x = answer_list(['What are your top 3 priorities?', 'How are you?', 'How many is 5?'], answer_type='list', show_question_index=True, ordered=True, cap='auto', input_suffix='I want to ')

    print(x)
    pass


if __name__ == '__main__':
    test()
