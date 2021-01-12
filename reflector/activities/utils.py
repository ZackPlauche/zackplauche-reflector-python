import re

from config import settings
from reflector.export import export_to_csv, export_to_txt, export, clean_data_for_export
from reflector.answer import answer_question, validate_choice



def get_integrity_status(yesno_question_list, yesno_answer_list):
    integrity_slice = 100 / len(yesno_question_list)
    integrity = sum([integrity_slice for answer in yesno_answer_list if answer in {'y', 'yes'}]).__int__()
    integrity_status = f'{integrity}%'
    return integrity_status

def add_frequency_to_question(question, frequency):
    '''Add frequency to a question or series of question_list'''
    frequency_dict = {
        'daily': 'the day',
        'weekly': 'the week',
        'monthly': 'the month',
        'yearly': 'the year',
        'tomrrow': 'tomrrow',
    }
    validate_choice(frequency, list(frequency_dict.keys()))
    frequency = frequency_dict.get(frequency)
    updated_question = f'{question[:-1]} for {frequency}?'
    return updated_question


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
def debug(*args):
    print('DEBUG: ', *args)
