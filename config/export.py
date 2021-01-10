import csv
import re
from datetime import datetime
from pathlib import Path
import os

from . import settings
from .utils import get_datetime_now_vars, debug


def clean_data_for_export(*args):
    return ([arg] if type(arg) is str else arg for arg in args)


def determine_file_mode(file_path, overwrite=False):
    mode = 'w+' if not file_path.exists() or overwrite else 'a+'
    return mode


def create_file_path(file_name, suffix):
    file_path = Path(f'{settings.STORAGE_DIRECTORY}/{file_name}').with_suffix(suffix)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def create_file(file_name, suffix, overwrite=False):
    file = create_file_path(file_name, suffix)
    file_mode = determine_file_mode(file)
    return file, file_mode


def add_time_headers_to_header_row(column_list):
    time_column_list = ['Date', 'Day', 'Time']
    column_list = time_column_list + column_list
    return column_list


def add_time_data_to_data_row(data_list):
    time_data_list = list(get_datetime_now_vars())
    data_list = time_data_list + data_list
    return data_list


def create_csv_rows(answer_data, column_header_list, file_mode):
    rows = []
    if file_mode in {'w+', 'w'}:
        column_header_row = add_time_headers_to_header_row(column_header_list)
        rows.append(column_header_row)
    data_row = add_time_data_to_data_row(answer_data)
    rows.append(data_row)
    return rows


def write_rows_to_csv(file, file_mode, rows):
    with open(file, file_mode, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)


def export_to_csv(answer_data, column_header_list, file_name, overwrite=False):
    answer_data, column_header_list = clean_data_for_export(answer_data, column_header_list)
    file, file_mode = create_file(file_name, '.csv', overwrite)
    rows = create_csv_rows(answer_data, column_header_list, file_mode)
    write_rows_to_csv(file, file_mode, rows)


def write_txt_file_title(file_name, open_txt_file):
    file_title = print(f'{file_name}:\n\n')
    open_txt_file.write(file_title)


def get_list_index(open_txt_file):
    open_txt_file.seek(0)
    try:
        last_line_of_file = open_txt_file.readlines()[-1]
        pattern = '(\d+).'
        regex = re.compile(pattern)
        match = regex.search(last_line_of_file)
        list_index = int(match.group(1)) + 1
    except:
        list_index = 1
    return list_index

def write_data_in_q_and_a_format(answer_data, question_list, open_txt_file):
    for answer, question in zip(answer_data, question_list):
        question_index = question_list.index(question) + 1
        open_txt_file.write(f'Question {question_index}: {question}\n\nAnswer: {answer}')


def add_todays_date(open_txt_file):
    date, _, _ = get_datetime_now_vars()
    open_txt_file.seek(0)
    file_text = open_txt_file.read()
    try:
        re.compile(date).search(file_text).group()
    except:
        open_txt_file.write(f'\n{date}\n')

def write_data_in_text_list_format(answer_data, open_txt_file):
    add_todays_date(open_txt_file)
    list_index = get_list_index(open_txt_file)
    for item in answer_data:
        if item:
            open_txt_file.write(f'{list_index}. {item}\n')
            list_index += 1

# export_to_txt argument mapping doesn't match export_to_csv, but
# question_list is optional because the intention was to have a Q&A style
# test file option. This is the best I knew how to do for now (even though its
# a bit mess)
def export_to_txt(answer_data, file_name, question_list=None,  overwrite=False):
    answer_data = clean_data_for_export(answer_data)
    file, file_mode = create_file(file_name, '.txt', overwrite)
    with open(file, file_mode) as file:
        if file.mode == 'w+':
            write_txt_file_title(file_name, file)
        if question_list:
            write_data_in_q_and_a_format(answer_data, question_list, file)
        else:
            write_data_in_text_list_format(answer_data, file)
