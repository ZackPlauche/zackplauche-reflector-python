import re
from time import sleep
from pathlib import Path

from . import settings
from .answer import answer_question, answer_questions, answer_question_dict
from .export import export_to_csv, export_to_txt
from .utils import casefold_all

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

    return updated_question_list


def display(file_name, keep='text'):
    """Print previously imported data in a list format in command line / terminal."""
    path = Path('Data Storage') / file_name

    # Print/Display items first if they exist already.
    if path.exists():
        file = open(path)
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








def list_reflector(file_name, topic, question, directory='Data Storage', **kwargs):
    '''full_answer(file_name, topic, question_list, **kwargs)

    :param file_name:
    :param topic:
    :param question:
    :param kwargs:
    :return:
    '''
    file = Path(settings.STORAGE_DIRECTORY) / file_name
    title = file.name

    # Print/Display goals first if they exist already.
    if file.exists():
        display_text, filetitle, items = display(file_name, 'all')

        # Add or Rewrite new items.
        choice = pick_option(f'Would you like to add to or rewrite your {topic}?', ['add', 'rewrite', 'remove', 'no'])
        if not choice in {'no', 'n', ''}:
            if choice != 'remove':
                new_items = answer_questions(question, answer_type='list', ordered=True)
                if choice == 'add':
                    print(f'Exporting {topic[0].upper() + topic[1:]}...\n')
                    export_to_txt(new_items, title)
                    print(f'{topic[0].upper() + topic[1:]} exported...')
                elif choice == 'rewrite':
                    export_to_txt(new_items, title, overwrite=True)
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
                export_to_txt(title, items, overwrite=True)
                return items

            # Put current topic_items in a list
        else:
            regex = re.compile('.+\. (.+)')
            topic_items = regex.findall(display_text)

    # Write goals for the first time.
    else:
        topic_items = answer_question(question, type='list', ordered=True)
        export_to_txt(title, topic_items)

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

def print_choice_list(choice_list):
        for choice in choice_list:
            choice_index = choice_list.index(choice) + 1
            print(f'{choice_index}. {choice}')

def get_choice_range(choice_list):
    choice_range = f'(from 1 to {len(choice_list)})'
    return choice_range

def check_if_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def validate_choice_number(choice_number, choice_list):
    choice_is_valid = True
    if not choice_number:
        error = '\nAnswer cannot be left blank.\n'
        print(error)
        sleep(1)
        choice_is_valid = False
    elif not check_if_int(choice_number):
        error = '\nAnswer must be a whole number\n'
        print(error)
        sleep(1)
        choice_is_valid = False
    elif check_if_int(choice_number) and not int(choice_number) in range():
        error = 'Answer out of range.'
        help_text = f'Please enter a number between 1 and {len(choice_list)}.'
        print(f'\n{error} {help_text}\n')
        sleep(1)
        choice_is_valid = False
    return choice_is_valid


def smart_choice(choice_list):
    '''
    :param choice_list: Allows user to input list of activities to do to return a choice.
    :returns : Exact item chosen through the items index.
    '''
    print_choice_list(choice_list)
    while True:
        choice_number = input(f'\nActivity number {get_choice_range(choice_list)}: ')
        if validate_choice_number(choice_number, choice_list):
            return choice_number

def activity(questions, file_name, **kwargs):
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


def test():
    question_list = [
        'What are your priorities?',
        'What are your wins?'
    ]
    activity('test', question_list, export_data=False, frequency='daily', ordered=True, cap=3)


if __name__ == '__main__':
    test()