from pyautogui import hotkey, typewrite, press
from time import sleep
from datetime import datetime
import subprocess

now = datetime.now()
date = f'{now.month}/{now.day}/{now.year}'
day = now.strftime('%A')
time = now.strftime("%I:%M %p").lstrip('0')


def openevernote():
    subprocess.Popen('C:\\Program Files (x86)\\Evernote\\Evernote\\Evernote.exe')
    sleep(1)


def new_note():
    '''This creates a new note inside of Evernote
    Best placed inside of another function. '''
    hotkey('ctrl', 'n')
    sleep(1)


def fullscreen():
    hotkey('win', 'up')


def checkbox():
    '''Creates a checkbox. '''
    hotkey('ctrl', 'shift', 'c')


def orderedlist():
    '''Creates an ordered list.'''
    hotkey('ctrl', 'shift', 'o')


def title_note(notetitle, name=None):
    notetitle = notetitle.title()
    notetitle = f'{notetitle} {date}'
    if name:
        name = name.title()
        notetitle = f'{name} {notetitle}'
    press('f2')
    typewrite(notetitle)
    sleep(.5)
    press('enter')
    sleep(.5)


def assign_to_notebook(notebook_title):
    hotkey('alt', 'shift', 'b')
    sleep(.5)
    typewrite(notebook_title)
    sleep(.5)
    press('enter')
    sleep(.5)


def create_note(title, notebook_title, name=None):
    '''Create a note inside of evernote.'''

    openevernote()
    new_note()
    assign_to_notebook(notebook_title)
    title_note(title, name)


def notepad():
    ''' This uploads your reflection to a new note, then saves the note in your "Daily Reflections" notebook.'''
    create_note('Notepad', 'Notepad')


def tasklist(title, tasks, notebook_title=None, headings=False):
    '''Creates a list of tasks given a list of information.'''
    create_note('List', notebook_title, title)

    tasks = tuple(tasks)

    def writetasks(tasks):
        orderedlist()
        checkbox()
        for task in tasks:
            typewrite(task)
            press('enter')
        press('enter')
        press('enter')
        press('enter')

    if headings:
        for heading, tasklist in zip(headings, tasks):
            typewrite(f'{heading}:')
            press('enter')
            writetasks(tasklist)
    else:
        writetasks(tasks)


def test():
    '''Put stuff to test here.'''
    tasklist('Test', [['Task 1', 'Task 2'], ['Task 3', 'Task 4']], ['Heading 1', 'Heading 2'])
    pass


if __name__ == '__main__':
    test()
