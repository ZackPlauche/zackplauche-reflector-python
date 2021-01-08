# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
import re
from datetime import datetime
from pathlib import Path


def activity(activity_name, question_list, frequency=None, ordered=False, cap=None, **kwargs):
    '''Shorter format for added funcionality for each reflector activity.'''

    # Add frequency if frequency is defined
    if frequency:
        question_list = add_frequency(question_list, frequency)

        # Add the frequency to the activities name
        activity_name = f'{activity_name} ({frequency})'

    # Walk through question_list and collect answer data
    activity_data = answer(question_list, answer_type='listed', ordered=ordered, cap=cap)

    # If kwarg "export" exists, export data as it should be exported.
    if kwargs.get('export'):
        if kwargs.get('export') == 'report':
            try:
                export(activity_name.title(), activity_data, report=kwargs.get('columns'))
            except:
                raise Exception('Must include the keyword argument of "columns" which must equal a list of columns.')
        elif kwargs.get('export') == 'date':
            export(activity_name.title(), activity_data, date=True)
        else:
            export(activity_name.title(), activity_data)

    # Return activity data
    return activity_data


def arg_check(arg_name, response_list, arg):
    if type(response_list) == str:
        appropriate_response = response_list
    else:
        appropriate_response = f'either {", ".join(response_list[:-1])} or {response_list[-1]}'

    if arg not in response_list:
        raise Exception(
            f'Arugument "{arg_name}" must equal {appropriate_response}. Please check your spelling and try again.')


def add_frequency(question_list, frequency):
    '''Add frequency to a question or series of question_list'''
    # Lowercase frequency to ensure proper string format is standard from the beginning
    frequency = frequency.lower()
    arg_check('frequency', ['daily', 'weekly', 'monthly', 'yearly', 'tomorrow'], frequency)

    # Add a time to add to the question_list
    if frequency == 'daily':
        time = 'the day'
    elif frequency == 'weekly':
        time = 'the week'
    elif frequency == 'monthly':
        time = 'the month'
    elif frequency == 'yearly':
        time = 'the year'
    elif frequency == 'tomorrow':
        time = 'tomorrow'

    # Add time to each question
    question_list = [f'{question[:-1]} for {time}?' for question in question_list]

    return question_list


def display(filename, keep='text', directory='Data Storage'):
    '''display(title, *list_to_display, ordered=False)

    Displays items in a basic list format.

    To display an entire list, you'll need to add a * in front of the list name.
    For example: *mylist
    Otherwise it will print the whole list.
    '''

    # Print/Display itmes first if they exist already.
    if os.path.exists(f'.\\{directory}\\{filename}'):
        file = open(f'.\\{directory}\\{filename}')
        file_text = file.read()

        # Sort all items into individual list
        title = re.compile('(.+)\:').search(file_text).group(1)
        items = re.compile('\d+\. (.+)').findall(file_text)
        print(file_text)
        file.close()

        if keep == 'file_text':
            return file_text
        if keep == 'title':
            return title
        if keep == 'items':
            return items
        if keep == 'all':
            return file_text, title, items

# TODO: Fix export not adding the title to files.


def export(filename, data, directory='Data Storage', **kwargs):
    '''Exports data into a file for storage.

    :param report: add a list of column names for your report.
    :param overwrite: write over a file that already exists **Warning: this will erase any data previously a file there.**'''

    # Skip the whole function if data = None
    if not data or not data[0]:
        pass

    else:

        # Remove file_type from filename
        if filename[:-4] in {'.txt', '.csv'}:
            filename = filename[:-4]

        # Create the directory to store your data if it doesn't already exist.
        os.makedirs(directory, exist_ok=True)

        # Determine the type of file.
        data_type = type(data)
        if data_type == list or data_type == str:
            if data_type == str:
                data = tuple([data])
            if kwargs.get('report'):
                filetype = 'csv'
            else:
                data = tuple(data)
                filetype = 'txt'
        elif data_type == pd.DataFrame:
            filetype = 'xlsx'

        filepath = f'.\\{directory}\\{filename}.{filetype}'

        # See if file is a txt or a csv, and if so perform the following actions.
        if filetype in {'txt', 'csv'}:

            # If a file doesn't exist, or is being overwritten, write it.
            if not os.path.isfile(filepath) or kwargs.get('overwrite'):  # If overwrite=True, overwrite the a file.
                if filetype == 'csv':
                    file = open(filepath, 'w+', newline='')
                elif filetype == 'txt':
                    file = open(filepath, 'w+')

            # If a file does exist, append to it.
            else:
                if filetype == 'csv':
                    file = open(filepath, 'a+', newline='')
                elif filetype == 'txt':
                    file = open(filepath, 'a+')

            # Create time variables for csv reports and text files that add dates to their entry.
            now = datetime.now()
            todays_date = f'{now.month}/{now.day}/{now.year}'
            today = now.strftime('%A')
            time = now.strftime("%I:%M %p").lstrip('0')

            # Write report/csv if filetype is csv.
            if filetype == 'csv':

                # Define csv writer
                writer = csv.writer(file)

                # Add time tracking columns to csv reports.
                if kwargs.get('report'):
                    time_column_headers = ['Date', 'Day']
                    time_column_data = [todays_date, today]
                if kwargs.get("time") == 'full':
                    time_column_headers.append('Time')
                    time_column_data.append(time)

                # If file is in write mode, add a header row
                print(file.mode)
                if file.mode == 'w+':
                    writer.writerow(time_column_headers + kwargs.get('report'))

                # If the data contains a nested list, join each list of answers into a single answer and put it into a list
                if type(data[0]) is list:
                    writer.writerow(time_column_data + [', '.join(answer) for answer in data])

                # Otherwise, join the data and add it to the report.
                else:
                    if len(', '.join(data)) is len(kwargs.get('report')):
                        writer.writerow(time_column_data + [', '.join(data)])
                    else:
                        writer.writerow(time_column_data + data)

            elif filetype == 'txt':

                # Write title of text file if file is in write mode.
                if file.mode == 'w+':
                    file.write(f'{filename}:\n\n')

                try:
                    file.seek(0)
                    last_line = file.readlines()[-1]
                    last_index_regex = re.compile('(\d+).')
                    last_index_match = last_index_regex.search(last_line)
                    index = int(last_index_match.group(1)) + 1
                except:
                    index = 1

                # Text report template
                if kwargs.get('report'):
                    question_list = kwargs.get('report')
                    for answer, question in zip(data, question_list):
                        file.write(f'Question {kwargs.get("report").index(question) + 1}: {question}\n\nAnswer: {answer}')

                # List Template
                else:
                    # Write date if date is not in file text
                    if kwargs.get('date'):
                        file.seek(0)
                        try:
                            filetext = file.read()
                            date_match = re.compile(todays_date).search(filetext).group()
                        except:

                            date_match = None
                        if date_match == todays_date:
                            print('Skipping Date...\n')
                        else:
                            print('Adding Date...\n')
                            file.write(f'\n{todays_date}\n')

                    for item in data:
                        if item:
                            file.write(f'{index}. {item}\n')
                            index += 1
                file.close()


def integrity(yorn_question_list_list, yorn_answers, dependency=None):
    '''
    Takes in a list of yes or no answers and their resopnses and converts them to a total percentage value
    based on a y to n ratio.
    '''

    # Integrity starts at 100%
    integrity = 100

    # Each piece of the integrity is made up of the maximum integrity divided by the number of yes or no question_list
    piece = 100 / len(yorn_question_list_list)

    # Subtract a piece from the maximum integrity for each "no" answer
    for answer in yorn_answers:
        if answer == 'n' or answer == 'no':
            integrity -= piece

    # Put the integrity in an integer format for better readability (no messy decimals)
    integrity = f'{int(integrity)}%'

    return integrity


def list_reflector(filename, topic, question, directory='Data Storage', **kwargs):
    '''full_answer(filename, topic, question_list, **kwargs)

    :param filename:
    :param topic:
    :param question:
    :param kwargs:
    :return:
    '''

    # Pulls title from filename
    title = re.compile('(.+)\.').search(filename).group(1)

    # Print/Display goals first if they exist already.
    if os.path.exists(f'.\\{directory}\\{filename}'):
        display_text, filetitle, items = display(filename, 'all')

        # Add or Rewrite new items.
        choice = pick_option(f'Would you like to add to or rewrite your {topic}?', ['add', 'rewrite', 'remove', 'no'])
        if not choice in {'no', 'n', ''}:
            if choice != 'remove':
                new_items = answer(question, answer_type='listed', ordered=True)
                if choice == 'add':
                    print(f'Exporting {topic[0].upper() + topic[1:]}...\n')
                    export(title, new_items)
                    print(f'{topic[0].upper() + topic[1:]} exported...')
                elif choice == 'rewrite':
                    export(title, new_items, overwrite=True)
            elif choice == 'remove':
                print()
                # Rewrite file without the removed number items
                item_numbers = []
                while True:
                    item_number = input(f'Enter the number of {topic} you\'d like to remove (or press "enter" with nothing to end): ')
                    if item_number == '':
                        break
                    item_numbers.append(int(item_number))
                remove_items = []
                for number in item_numbers:
                    remove_items.append(items[number - 1])
                for item in remove_items:
                    items.remove(item)
                export(title, items, overwrite=True)
                return items

            # Put current topic_items in a list
        else:
            regex = re.compile('.+\. (.+)')
            topic_items = regex.findall(display_text)

    # Write goals for the first time.
    else:
        topic_items = answer(question, type='listed', ordered=True)
        export(title, topic_items)

        return topic_items


def pick_option(question, acceptable_answers):

    choice = input(f'{question} ({"/".join(acceptable_answers)}): ').lower()
    print()

    # Answer validation
    if choice:
        while choice not in [answer.lower() for answer in acceptable_answers]:
            print('ERROR: That is not a valid answer.\n')
            print('Please select a valid answer from this list:\n')

            for answer in acceptable_answers:
                print(f'{acceptable_answers.index(answer) + 1}. {answer}')
            print()

            choice = input('Enter the number of the option you\'d like to pick: ')
            print()
            try:
                choice = acceptable_answers[(int(choice) - 1)].lower()
            except:
                pass

            if choice in [answer.lower() for answer in acceptable_answers]:
                break

    return choice


def smart_choice(menu_items):
    '''
    :param menu_items: Allows user to input list of activities to do to return a choice.
    :returns : Exact item chosen through the items index.
    '''

    choice_range = f'(from {menu_items.index(menu_items[0]) + 1} to {menu_items.index(menu_items[-1]) + 1})'

    for item in menu_items:
        print(f'{menu_items.index(item) + 1}) {item}')

    choice = input(f'\nActivity number {choice_range}: ')
    print()
    if choice != '':
        try:
            if int(choice) in range(len(menu_items) + 1):
                pass
            else:
                while True:
                    print("ERROR: Given Response outside the number range.\n")
                    choice = input("Please enter activity number next to corresponding acivity: ")

                    if int(choice) in range(len(menu_items + 1)):
                        break
            choice = menu_items[int(choice) - 1]

            print('\n')
        except:
            while True:
                print("ERROR: Given response was not a number.\n")
                choice = input("Please enter activity number next to corresponding acivity: ")
                print()

                try:
                    if int(choice) in range(len(menu_items)):
                        pass
                    else:
                        while True:
                            print("ERROR: Given Response outside the number range.\n")
                            choice = input("Please enter activity number next to corresponding acivity: ")
                            print()

                            if int(choice) in range(len(menu_items)):
                                break
                    choice = menu_items[int(choice) - 1]
                    break
                except:
                    continue

                try:
                    if choice in [str(menu_items.index(item) + 1) for item in menu_items]:
                        choice = menu_items[int(choice) - 1]
                        print()
                        break
                except:
                    continue
    return choice


def test():
    question_list = [
        'What are your priorities?',
        'What are your wins?'
    ]
    activity('test', question_list, export_data=False, frequency='daily', ordered=True, cap=3)


if __name__ == '__main__':
    test()
