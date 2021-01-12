import re
from pathlib import Path
from .answer import answer_question, answer_questions, answer_question_dict
from .export import export_to_csv, export_to_txt
from .utils import casefold_all
from config import settings


def validate_arg(arg_name, arg_options, arg):
    arg_name, arg_options = casefold_all(arg_name, arg_options)
    appropriate_response = f'either {", ".join(arg_options[:-1])} or {arg_options[-1]}'
    error = f'Arguemnt "{arg_name}" must equal {appropriate_response}.'
    help_text = 'Please check your spelling and try again.'
    error_message = f'{error} {help_text}'
    if arg not in arg_options:
        raise Exception(error_message)


def add_frequency(question_list, frequency):
    '''Add frequency to a question or series of question_list'''
    frequency_set = {'daliy', 'weekly', 'monthly', 'yearly', 'tomorrow'}
    validate_arg('frequency', frequency_set, frequency.casefold())
    frequency_dict = {
        'daily': 'the day',
        'weekly': 'the week',
        'monthly': 'the month',
        'yearly': 'the year',
        'tomrrow': 'tomrrow',
    }
    time = frequency_dict.get(frequency)
    updated_question_list = [f'{question[:-1]} for {time}?' for question in question_list]
    return updated_question_list


def get_text_from_txt_file(file_path):
    with open(file_path) as file:
        file_text = file.read()
    return file_text


def print_file_text(file_path):
    print(get_text_from_txt_file(file_path))


def get_txt_file_title_from_file_text(file_text):
    txt_file_title = re.compile('(.+)\:').search(file_text).group(1)
    return txt_file_title


def get_list_items_from_file_text(file_text):
    list_items = re.compile('\d+\. (.+)').findall(file_text)
    return list_items


def get_txt_file_data(file_path):
    file_text = get_text_from_txt_file(file_path)
    txt_file_title = get_txt_file_title_from_file_text(file_text)
    txt_file_list_items = get_list_items_from_file_text(file_text)
    file_data_list = [file_text, txt_file_title, txt_file_list_items]
    return file_data_list


def remove_items_from_list(list_) -> list:
    question = 'Enter the number of {topic} you\'d like to remove'
    while True:
        list_item_to_remove_index = answer_question(question, 'inline')
        if not list_item_to_remove_index:
            break
        list_item = list_[list_item_to_remove_index]
        list_.remove(list_item)
    return list_


def choose_list_edit_option(topic_plural):
    question = f'How would you like to edit your {topic_plural}?'
    choice_list = ['add', 'rewrite', 'remove', 'no']
    answer = answer_question(question, 'inline', choice_list=choice_list)
    return answer


def add_or_rewrite_txt_file_list(file, question, edit_option):
    new_list_items = answer_question(question, 'list', ordered=True)
    if edit_option == 'add':
        export_to_txt(new_list_items, file.name)
    elif edit_option == 'rewrite':
        export_to_txt(new_list_items, file.name, overwrite=True)


def remove_items_from_txt_file_list(file):
    _, _, list_items = get_txt_file_data(file)
    print()
    list_items = remove_items_from_list(list_items)
    export_to_txt(list_items, file.name, overwrite=True)




def edit_txt_file_list(file_name, topic_plural, question):
    file = settings.STORAGE_DIRECTORY / file_name
    print_file_text(file)
    edit_option = choose_list_edit_option(topic_plural)
    if file.exists():
        if edit_option in {'add', 'rewrite'}:
            add_or_rewrite_txt_file_list(file.name, question, edit_option)
        elif edit_option == 'remove':
            remove_items_from_txt_file_list(file)

    else:
        topic_items = answer_question(question, type='list', ordered=True)
        export_to_txt(topic_items, file.name)
        return topic_items


def activity(file_name, questions, **kwargs):
    answer = ''
    if type(questions) is str:
        answer = answer_question(questions, **kwargs)
    elif type(questions) is list:
        answer = answer_questions(questions, **kwargs)
    elif type(questions) is dict:
        answer = answer_question_dict(questions)
        questions = list(questions.keys())
    export_to_csv(answer, questions, file_name)
    return answer
