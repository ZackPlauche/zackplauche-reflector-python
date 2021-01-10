import time
import os
import itertools

from .utils import get_integrity_status
from .answer import answer_question, answer_questions, answer_question_dict
from .export import export_to_csv


def acclaim_system():
    '''
    Walks through the acclaim System Created by Ryan Donaldson, with some added parts.
    '''
    physiology_questions = [
        'Do you feel well rested?',
        'Are you hydrated?',
        'Are you well fed?',
        'Did you (or are you going to) exercise today?',
        'Is the temperature fine for you?',
        'Is your environment clean and organized?',
        'Do you feel complete wellness?'
    ]

    security_questions = [
        'Are you financially well off or have a financial plan?',
        'Are you physically safe?'
    ]

    love_and_belonging_questions = [
        'Have you messaged 5 of your friends saying "I appreciate you & you matter to me"?',
        'Have you talked to your favorite person or Significant Other?'
    ]

    self_esteem_questions = [
        'State 10 reasons why you love your',
        'List 5 things you feel you are most competent at.'
    ]

    self_actualization_questions_dict = {
        'List the 1 project that you\'re Most Excited to work on': {'answer_type': 'list', 'cap': 'auto'},
        'List what skills that you\'re going to use from the self esteem list': {'answer_type': 'list'},
        'List the actions that can be done to secure the success of that project': {'answer_type': 'list', 'ordered': True},
        'List the criteria that will guage the success of that project.': {'answer_type': 'list'},
        'Did you express completion of this board to your accountability partners?': {'answer_type': 'inline', 'yesno': True}
    }

    acclaim_system_questions = [
        physiology_questions,
        security_questions,
        love_and_belonging_questions,
        self_esteem_questions,
        self_actualization_questions_dict.keys(),
    ]

    acclaim_system_status_list = [
        'Physiology',
        'Security',
        'Love & Belonging',
        'Self-Esteem',
        'Self-Actualization',
    ]

    # TODO: Make this a loop
    print('Physiology:\n'.upper())
    psychology_answers = answer_questions(physiology_questions, 'inline', yesno=True)
    print('Security:\n'.upper())
    security_answers = answer_questions(security_questions, 'inline', yesno=True)
    print('Love & Belonging:\n'.upper())
    love_and_belonging_answers = answer_questions(love_and_belonging_questions, 'inline', yesno=True)
    print('Self-Esteem:\n'.upper())
    self_esteem_answers = answer_questions(self_esteem_questions, 'list', cap='auto')
    print('Self Actualtization:\n'.upper())
    self_actualization_answers = answer_question_dict(self_actualization_questions_dict)

    acclaim_system_answers = [
        psychology_answers,
        security_answers,
        love_and_belonging_answers,
        self_esteem_answers,
        self_actualization_answers
    ]

    answers = list(itertools.chain.from_iterable(acclaim_system_answers))
    questions = list(itertools.chain.from_iterable(acclaim_system_questions))

    export_to_csv(answers, questions, 'acclaim_system')


def delegation(frequency=None):
    '''Walks through process for where energy was spent and what can be done to become more efficient.'''

    quesitons = [
        'What took your energy?',
        'What non-ceo activities did you do?',
        'To Do\'s - What Can be delegated?',
        'What systems do we need?',
        'What can I stop doing?'
    ]

    columns = ['Energy Investments', 'Non CEO activities',
               'Tasks to Delegate', 'Systems Needed', 'Stop List']

    delegation_report = activity(
        'Delegation Report', quesitons, frequency=frequency, export='report', columns=columns)

    return delegation_report


def easier_life():
    question = 'Name an idea to make your life easeir'
    easier_life_ideas = answer_question(question, 'list', cap=5)
    print()
    # TODO: Build export to text list
    export_to_csv(easier_life_ideas, question, 'Easier Life')
    return easier_life_ideas


def goals():
    '''Displays a previous list of goals, and either ads or sets new ones.'''
    # TODO: Build goal reflector functionality
    question = 'What are your goals?'
    file_name = 'My Goals.txt'
    goals = answer_question(question, 'list')
    export_to_csv(goals, question, file_name)
    return goals


def gratitude():
    '''This function takes in a list of things you appreciate.'''
    question = 'What are you grateful for?'
    gratitude_list = answer_question(question, 'list', ordered=True)
    file_name = 'Gratitude List'
    # TODO: Build export to text list
    export_to_csv(gratitude_list, question, file_name,)
    print()

    return gratitude_list


def improvements():
    question = ['What can you do to improve?']
    improvements = answer_question(question, 'list')
    # TODO: Build export to text list
    export_to_csv(improvements, ['Improvements'], improvements)
    return improvements


def intentions():
    question = 'What are your intentions for the day?'
    intentions = answer_question("What are your intentions for the day?", 'list')
    file_name = 'Intentions'
    export_to_csv(intentions, question, file_name)
    return intentions


def lessons():
    question = 'What lessons did you learn or relearn today?'
    lessons = answer_question(question, "list")
    file_name = 'Daily Lessons'
    export_to_csv(lessons, question, file_name)

    return lessons


def meaningful_experience():
    question = 'What was one meaningful experience you had today?'
    meaningful_experience = answer_question(question, 'text')
    export_to_csv(meaningful_experience, question, 'Meaningful Experiences')
    return meaningful_experience


def operation_self():
    """This program is for when you're feeling low self esteem / fear that might be fucking up your life at the moment."""
    print('\nThe SELF in this activity is an acronym, that stands for "Self Esteem Low / Fear"\nand was made to be a guide out of your temporary darkness and move you to a more empowered state.')

    questions_dict = {
        "Did you poop today?": {'answer_type': 'inline', 'yesno': True},
        "Did you tell your significant other that you're experiencing this?": {'answer_type': 'inline', 'yesno': True},
        "Go ahead and reflect for a minute to try to clear your brain.": {'answer_type': 'text'},
        "What can you do to turn this around?": {'answer_type': 'list'}
    }
    answers = answer_question_dict(questions_dict)


def operation_red_dragon():
    "For when she's on her period."
    print("\nSo, your women is on her period huh? Perfect. That's what this program is designed for.\n")

    print("""Here's what you should probably look at doing.

    1. Breathe, everything is going to be ok. And you have to be strong here, so start with this one.
    2. Whether you like it or not, you'll need to do more chores. Take care of something she normally does (like laundry, feeding the animals, etc.)
    3. Make sure to have some kind of sugars or chocolate in the house. Her body is going through a transformation that requires a lot of pain and her ovaries are committing sapuku.
    4. Flowers and some other type of girly gift.
    5. Be a bit more attentive and make sure to not make any mistakes for the most part in general. In fact, I'd do one of two things: stay out all day or make an in day the most amazing in day possible. Try having a movie day or something like this.
    6. Finally, this is her time to shine, so let her.
    7. Also, if she's down, have sex and make her cum.""")
    print('\nThat\'s all for now.')


def perfect_day(frequency):
    print('Forget everything you just typed. Now,...\n')
    question = 'What does your perfect day look like?'
    answer = answer_question(question, 'list', ordered=True)
    file_name = 'perfect_day'
    export_to_csv(answer, question, file_name)
    return perfect_day


def reflect():

    reflection = answer_question(
        'Take a minute to write a written reflection.\n''(linebreaks are enabled. To end reflection, press "." on a new line and press enter)')

    return reflection


def physiology_check():
    '''Checks up on health stats for the day.'''

    questions = [
        'Do you feel well rested?',
        'Are you hydrated?',
        'Are you well fed?',
        'Did you (or are you going to) exercise today?',
        'Is the temperature fine for you?',
        'Is your environment clean and organized?',
        'Do you feel complete wellness?'
    ]

    answers = answer_question(questions, 'inline', yesno=True)
    file_name = 'health_stats'
    physiology_score = get_integrity_status(questions, answers)
    print(f'\nYour physiology is at {get_integrity_status(questions, answers)}.\n')

    physiology_columns = ['Score', 'Well Rested', 'Hydrated', 'Well Fed',
                          'Movement', 'Temperature', 'Clean Environment', 'Full of Health']

    export_to_csv('Health Stats', [physiology_score] +
                  physiology_stats, report=physiology_columns)

    return physiology_stats


def security_check():
    '''Checks up on security stats for the day.'''

    security_questions = [
        'Are you financially well off or have a financial plan?',
        'Are you physically safe?'
    ]

    security_stats = answer_question(
        security_questions, 'inline', yesno=True)

    security_score = integrity(security_questions, security_stats)

    print(f'\nYour security is at {security_score}.\n')

    security_columns = ['Score', 'Financially Sound', 'Physically Safe']

    export('Security Stats', [security_score] +
           security_stats, report=security_columns)

    return security_stats


def love_and_belonging_check():
    '''Checks up on health stats for the day.'''

    love_and_belonging_questions = [
        'Have you messaged 5 of your friends saying "I appreciate you & you matter to me"?',
        'Have you talked to your favorite person or Significant Other?'
    ]

    love_and_belonging_stats = answer_question(
        love_and_belonging_questions, 'inline', yesno=True)

    love_and_belonging_score = integrity(
        love_and_belonging_questions, love_and_belonging_stats)

    print(f'\nYour love and belonging is at {love_and_belonging_score}.\n')

    love_and_belonging_columns = [
        'Score', 'Friend Appreciation', 'Significant Other Communication']

    export('Love and Belonging Stats', [
        love_and_belonging_score] + love_and_belonging_stats, report=love_and_belonging_columns)

    return love_and_belonging_stats


def priorities(frequency=None, write_checklist=False):

    questions = [
        f'What are your top 3 personal priorities (starting with The ONE Thing)?',
        f'What are your top 3 professional priorities (starting with The ONE Thing)?'
    ]

    priorities = activity('Priorities', questions,
                          frequency=frequency, ordered=True, cap='auto')

    columns = ['ONE Thing', 'Priority #2', 'Priority #3']

    export("Personal Priorities", priorities[0], report=columns)
    export("Work Priorities", priorities[1], report=columns)

    if write_checklist == True:
        title = f'{frequency} Priorities'.title()
        tasklist(title, priorities, title, headings=['Personal', 'Work'])

    return priorities


def prismatic_system():
    '''Walks user through Ryan Donaldson's PRISMATIC Goal Setting System.'''
    prismatic_list = [
        'People',
        'Resources',
        'Identity',
        'Specifics',
        'Metrics',
        'Actions',
        'Information',
        'Criteria for Success'
    ]
    prismatic_questions_dict = {
        'What is your goal?': {'answer_type': 'inline'},
        'What people will you utilize to achieve your goal?': {'answer_type': 'list'},
        'What resources will you utilzie to achieve your goal?': {'answer_type': 'list'},
        'What identities will you embody to achieve your goal?': {'answer_type': 'list'},
        'What are the specifics of your goal?': {'answer_type': 'list'},
        'What metrics will you use to track progress towards goal?': {'answer_type': 'list'},
        'What actions will you take to achieve your goal?': {'answer_type': 'list', 'ordered': True},
        'What are the timelines for each action?': {'answer_type': 'list'},
        'What information will you utilize to achieve your goal?': {'answer_type': 'list'},
        'What are your Criteria for success to achieve this goal?': {'answer_type': 'list'},
    }
    file_name = 'prismatic_goals'
    answers = answer_question_dict(prismatic_questions_dict)
    export_to_csv(answers, list(prismatic_questions_dict.keys()), file_name)
    return answers

def check_for_topic():
        print('Anything specific you want to accomplish?\n\n')
        topic = answer_question('I\'d like to', 'inline')
        if not topic:
            topic = 'improve your life'
        print()
        return topic

def ten_ideas(set_topic=False, frequency=None):
    
    topic = check_for_topic() if set_topic else 'to improve your life'
    question = f'Name an idea to {topic}'
    answer = answer_question(question, 'list', cap=10)
    file_name = 'ideas'
    if frequency:
        filename = f'{frequency} {file_name}'.title()
    export_to_csv(answer, question, file_name)
    return answer

def type_of_person():
    question = 'What type of person do you choose to be today?'
    type_of_person = answer_question(question, 'list')
    print()
    return type_of_person


def wins(frequency=None):
    question = 'What are your wins?'
    wins = answer_question(question, 'list', orderd=True)
    print(f'\nTotal Wins: {len(wins)}\n')
    return wins


def morning_reflection():
    '''Reflection to get the day started in a positive, epic mindset.'''

    print('Good morning handsome ;) \n')

    reflect()
    physiology_check()
    goals()
    type_of_person()
    intentions()
    gratitude()
    priorities('daily')
    self_love()  # TODO: Fix woopsie
    easier_life()
    ten_ideas_to_improve_your_life()
    reflect()


def end_of_day_reflection():

    print('Good evening sir! :) \n')
    reflect()
    wins()
    improvements()
    lessons()
    gratitude()
    meaningful_experience()
    self_love()
    ten_ideas_to_improve_your_life()
    goals()
    priorities = priorities(frequency='tomorrow')
    reflect()


def weekly_reflection():
    print('I hope you had a nice week sir! :)\n')

    reflect()
    wins('weekly')
    improvements()
    priorities = priorities('weekly')
    ideas = ten_ideas('crush it this week.')
    perfect_day = perfect_day('weekly')
    reflect()


def monthly_reflection():
    print('Wow, a whole month. I hope you had a nice month sir! :)\n')

    reflect()
    wins('monthly')
    improvements()
    priorities = priorities('monthly')
    ideas = ten_ideas('crush it this month.')
    perfect_day = perfect_day('monthly')

def birthday_reflection():
    '''Reflection to be done on your birthday.'''
    print('Happy birthday! :)\n')

    wins('yearly')
    improvements()
    priorities = priorities('yearly')
    ideas = ten_ideas('make this year your most amazing year so far.')


def off_the_wagon():
    reflect()
    not_doing()
    turn_around()
