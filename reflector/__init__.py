import time
import os
from .answer import answer_question


def run_reflector(activity_dict):
    print_reflector_intro()
    while True:
        activity = select_activity(activity_dict)
        run_activity(activity)
        if not play_again():
            break


def print_reflector_intro():
    print('\nWelcome to Reflector!')
    print('\nPlease choose an activity.\n')


def select_activity(activity_dict):
    activity_choice = smart_choice(list(activity_dict.keys()))
    activity = activity_dict[activity_choice]
    return activity


def smart_choice(choice_list):
    print_choice_list(choice_list)
    while True:
        choice_number = input(f'\nActivity number {get_choice_range(choice_list)}: ')
        if validate_choice_number(choice_number, choice_list):
            choice_number = int(choice_number) - 1
            choice = choice_list[choice_number]
            return choice


def print_choice_list(choice_list):
    for choice in choice_list:
        choice_index = choice_list.index(choice) + 1
        print(f'{choice_index}. {choice}')


def get_choice_range(choice_list):
    choice_range = f'(from 1 to {len(choice_list)})'
    return choice_range


def validate_choice_number(choice_number, choice_list):
    choice_is_valid = True
    if not choice_number:
        error = '\nAnswer cannot be left blank.'
        print(error)
        time.sleep(1)
        choice_is_valid = False
    elif not check_if_int(choice_number):
        error = '\nAnswer must be an integer (whole number).'
        print(error)
        time.sleep(1)
        choice_is_valid = False
    elif check_if_int(choice_number) and not int(choice_number) in range(1, len(choice_list) + 1):
        error = 'Answer out of range.'
        help_text = f'Please enter a number between 1 and {len(choice_list)}.'
        print(f'\n{error} {help_text}')
        time.sleep(1)
        choice_is_valid = False
    return choice_is_valid


def check_if_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def reflection_timer(func):
    def wrapper(arg):
        start_time = time.time()
        func(arg)
        end_time = time.time()
        total_time = create_total_time_string(end_time - start_time)
        print(f'Your reflection took {total_time}.')
        os.system('pause')
    return wrapper


def create_total_time_string(seconds):
    hours, minutes = convert_seconds_to_hours_minutes(seconds)
    minute_suffix = 'minutes' if minutes != 1 else 'minute'
    hour_suffix = 'hours' if hours != 1 else 'hour'
    total_time = f'{minutes} {minute_suffix}'
    if hours:
        total_time = f'{hours} {hour_suffix} ' + total_time 
    return total_time


def convert_seconds_to_hours_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours = int(hours)
    minutes = int(minutes)
    return hours, minutes


@reflection_timer
def run_activity(activity):
    activity()


def play_again():
    question = '\nWould you like to do something else?'
    answer = answer_question(question, 'inline', yesno=True)
    return True if answer in {'y', 'yes', ''} else False
