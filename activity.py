import re
from datetime import datetime
from pathlib import Path

from utils import casefold_all

def validate_arg(arg_name, arg_options, arg):
    arg_name, arg_options = casefold_all(arg_name, arg_options)
    appropriate_response = f'either {", ".join(arg_options[:-1])} or {arg_options[-1]}'
    error_text = f'Arguemnt "{arg_name}" must equal {appropriate_response}.'
    help_text = 'Please check your spelling and try again.'
    error_message = f'{error_text} {help_text}'
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

    return question_list


def display(file_name, directory_name='Data Storage', keep='text'):
    """Print previously imported data in a list format in command line / terminal."""
    base_dir = Path('.')
    directory = base_dir / directory_name
    file_path = directory / file_name

    # Print/Display items first if they exist already.
    if file_path.exists():
        file = open(file_path)
        file_text = file.read()

        # Sort all items into individual list
        title = re.compile('(.+)\:').search(file_text).group(1)
        items = re.compile('\d+\. (.+)').findall(file_text)
        print(file_text)
        file.close()

        file_data_list = []
        if keep == 'file_text':
            file_data_list.append(file_text)
        elif keep == 'title':
            file_data_list.append(title)
        elif keep == 'items':
            file_data_list.append(title)

        return tuple(file_data_list)

def export(answer_data, file_name: str, directory_name='Data Storage', overwrite=False, **kwargs):
    '''Exports data into a file for storage.

    :param report: add a list of column names for your report.
    :param overwrite: write over a file that already exists **Warning: this will erase any data previously a file there.**'''

    directory = Path('.') / directory_name
    directory.mkdir(exist_ok=True)
    file_path = directory / file_name


    # Determine the type of file.
    def determine_file_type_to_export(data, file_path, report=False):
        file_suffix = 'csv' if report else 'txt'
        return file_suffix
    
    new_file_type = determine_file_type_to_export(answer_data, file_path, kwargs.get('report'))

    def format_data_for_export(data):
        formatted_data = tuple([data]) if type(data) is str else tuple(data)
        return formatted_data
        
    formatted_ansewr_data = format_data_for_export(answer_data)

    # See if file is a txt or a csv, and if so perform the following actions.
    if new_file_type in {'txt', 'csv'}:

        def determine_file_mode(file_path, overwrite=False):
            mode = 'w+' if not file_path.exists() or overwrite else 'a+'
            return mode
        
        mode = determine_file_mode(file_path, overwrite)

        

        file = open(file_path, mode, newline='')

        # If a file doesn't exist, or is being overwritten, write it.
        mode = 'w+' if not file_path.exists() or overwrite else 'a+'
        if not file_path.exists() or overwrite:
            if new_file_type == 'csv':
                file = open(file_path, 'w+', newline='')
            elif new_file_type == 'txt':
                file = open(file_path, 'w+')

        # If a file does exist, append to it.
        else:
            if new_file_type == 'csv':
                file = open(file_path, 'a+', newline='')
            elif new_file_type == 'txt':
                file = open(file_path, 'a+')

        # Create time variables for csv reports and text files that add dates to their entry.
        now = datetime.now()
        todays_date = f'{now.month}/{now.day}/{now.year}'
        time = datetime.now().strftime('%#m/%#d/%Y')
        today = now.strftime('%A')
        time = now.strftime("%I:%M %p").lstrip('0')

        # Write report/csv if new_file_type is csv.
        if new_file_type == 'csv':

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

        elif new_file_type == 'txt':

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
                new_items = answer(question, answer_type='list', ordered=True)
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
        topic_items = answer(question, type='list', ordered=True)
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


def activity(activity_name, question_list, frequency=None, **kwargs):
    '''Shorter format for added funcionality for each reflector activity.'''

    if frequency:
        question_list = add_frequency(question_list, frequency)

        # Add the frequency to the activities name
        activity_name = f'{activity_name} ({frequency})'

    # Walk through question_list and collect answer data
    activity_data = answer_question_list(question_list, answer_type='list', ordered=ordered, cap=cap)

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


def test():
    question_list = [
        'What are your priorities?',
        'What are your wins?'
    ]
    activity('test', question_list, export_data=False, frequency='daily', ordered=True, cap=3)


if __name__ == '__main__':
    test()