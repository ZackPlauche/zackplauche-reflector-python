#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
from .answer import answer_question


def print_reflector_intro():
    print('\nWelcome to Reflector!')
    print('\nPlease choose an activity.\n')


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
        error = 'Answer cannot be left blank.\n'
        print(error)
        time.sleep(1)
        choice_is_valid = False
    elif not check_if_int(choice_number):
        error = '\nAnswer must be a whole number\n'
        print(error)
        time.sleep(1)
        choice_is_valid = False
    elif check_if_int(choice_number) and not int(choice_number) in range(len(choice_list)):
        error = 'Answer out of range.'
        help_text = f'Please enter a number between 1 and {len(choice_list)}.'
        print(f'\n{error} {help_text}\n')
        time.sleep(1)
        choice_is_valid = False
    return choice_is_valid


def smart_choice(choice_list):
    print_choice_list(choice_list)
    while True:
        choice_number = input(f'\nActivity number {get_choice_range(choice_list)}: ')
        if validate_choice_number(choice_number, choice_list):
            choice_number = int(choice_number) - 1
            choice = choice_list[choice_number]
            return choice


def select_activity(activity_dict):
    activity_choice = smart_choice(list(activity_dict.keys()))
    activity = activity_dict[activity_choice]
    return activity


def reflection_timer(func):
    def wrapper(arg):
        start_time = time.time()
        func(arg)
        end_time = round(time.time())
        total_time = end_time - start_time
        print(f'Your reflection took {total_time // 60 } minutes.')
        os.system('pause')
    return wrapper


@reflection_timer
def run_activity(activity):
    activity()


def play_again():
    question = '\n Would you like to do something else?'
    answer = answer_question(question, 'inline', yesno=True)
    return True if answer in {'y', 'yes', ''} else False


def run_reflector(activity_dict):
    print_reflector_intro()
    while True:
        activity = select_activity(activity_dict)
        run_activity(activity)
        if not play_again():
            break
