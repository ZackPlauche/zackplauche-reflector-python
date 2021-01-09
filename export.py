import csv
from datetime import datetime
from pathlib import Path
from utils import get_datetime_now_vars


def format_string_for_export(string):
    return [string]


def determine_file_mode(file_path, overwrite=False):
    mode = 'w+' if not file_path.exists() or overwrite else 'a+'
    return mode


def add_time_headers_to_header_row(column_list):
    time_column_list = ['Date', 'Day', 'Time']
    column_list = time_column_list + column_list
    return column_list


def add_time_data_to_data_row(data_list):
    time_data_list = list(get_datetime_now_vars())
    data_list = time_data_list + data_list
    return data_list


def export_to_csv(answer_data, column_header_list, file_name, overwrite=False):
    if type(answer_data) is str:
        answer_data = format_string_for_export(answer_data)
    file = Path(f'Data Storage/{file_name}').with_suffix('.csv')
    file.parent.mkdir(exist_ok=True)  # Needed to create or else you can't make the file
    mode = determine_file_mode(file, overwrite)
    rows = []
    if mode in {'w+', 'w'}:
        column_header_row = add_time_headers_to_header_row(column_header_list)
        rows.append(column_header_row)
    data_row = add_time_data_to_data_row(answer_data)
    rows.append(data_row)
    with open(file, mode, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)
