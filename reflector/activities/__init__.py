import itertools

from reflector.answer import answer_question, answer_questions, answer_questions_dict
from reflector.export import export_to_csv, export_to_txt
from reflector.activity import activity
from .utils import get_integrity_status, add_frequency_to_question


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
    self_love()
    easier_life()
    ten_ideas()
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
    ten_ideas()
    goals()
    priorities(frequency='tomorrow')
    reflect()


def weekly_reflection():
    print('I hope you had a nice week sir! :)\n')

    reflect()
    wins('weekly')
    improvements()
    priorities('weekly')
    ten_ideas('crush it this week.')
    perfect_day('weekly')
    reflect()


def monthly_reflection():
    print('Wow, a whole month. I hope you had a nice month sir! :)\n')

    reflect()
    wins('monthly')
    improvements()
    priorities('monthly')
    ten_ideas('crush it this month.')
    perfect_day('monthly')


def birthday_reflection():
    '''Reflection to be done on your birthday.'''
    print('Happy birthday! :)\n')
    wins('yearly')
    improvements()
    priorities('yearly')
    ten_ideas('make this year your most amazing year so far.')


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

    print('Physiology:\n'.upper())
    psychology_answers = answer_questions(physiology_questions, 'inline', yesno=True)
    print()
    print('Security:\n'.upper())
    security_answers = answer_questions(security_questions, 'inline', yesno=True)
    print()
    print('Love & Belonging:\n'.upper())
    love_and_belonging_answers = answer_questions(love_and_belonging_questions, 'inline', yesno=True)
    print()
    print('Self-Esteem:\n'.upper())
    self_esteem_answers = answer_questions(self_esteem_questions, 'list', cap='auto')
    print('Self Actualtization:\n'.upper())
    self_actualization_answers = answer_questions_dict(self_actualization_questions_dict)

    acclaim_system_answers = [
        psychology_answers,
        security_answers,
        love_and_belonging_answers,
        self_esteem_answers,
        self_actualization_answers
    ]

    answers = list(itertools.chain.from_iterable(acclaim_system_answers))
    questions = list(itertools.chain.from_iterable(acclaim_system_questions))

    export_to_csv('acclaim_system', answers, questions)


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
    export_to_txt('Easier Life', easier_life_ideas)
    return easier_life_ideas


def goals():
    '''Displays a previous list of goals, and either ads or sets new ones.'''
    # TODO: Build goal reflector functionality
    question = 'What are your goals?'
    file_name = 'My Goals'
    goals = answer_question(question, 'list')
    export_to_csv(file_name, goals, question)
    return goals


def gratitude():
    '''This function takes in a list of things you appreciate.'''
    file_name = 'Gratitude List'
    question = 'What are you grateful for?'
    gratitude_list = answer_question(question, 'list', ordered=True, input_suffix='I\'m grateful for ')
    export_to_csv(file_name, gratitude_list, column_headers='What are you grateful for?')
    print()

    return gratitude_list


def self_love():
    file_name = 'Self Love'
    question = 'What are 10 Reasons you love yourself?'
    answer = answer_question(question, 'list', ordered=True, cap='auto', input_suffix="I love myself because ")
    column_header = '10 Reasons I Love Myself'
    export_to_csv(file_name, answer, column_header)
    return answer


def improvements():
    question = 'What can you do to improve?'
    improvements = answer_question(question, 'list')
    export_to_txt('Improvements', improvements)
    return improvements


def intentions():
    file_name = 'Intentions'
    question = 'What are your intentions for the day?'
    intentions = answer_question(question, 'list', input_suffix='My intention is to ')
    export_to_csv(file_name, intentions, question)
    return intentions


def lessons():
    question = 'What lessons did you learn or relearn today?'
    lessons = answer_question(question, 'list')
    file_name = 'Daily Lessons'
    export_to_csv(file_name, lessons, question)
    return lessons


def meaningful_experience():
    question = 'What was one meaningful experience you had today?'
    meaningful_experience = answer_question(question, 'text')
    export_to_csv('Meaningful Experiences', meaningful_experience, question)
    return meaningful_experience


def operation_self():
    """This program is for when you're feeling low self esteem / fear that might be fucking up your life at the moment."""
    print('\nThe SELF in this activity is an acronym, that stands for "Self Esteem Low / Fear" and was made to be a guide out of your temporary darkness and move you to a more empowered state.')

    questions_dict = {
        "Did you poop today?": {'answer_type': 'inline', 'yesno': True},
        "Did you tell your significant other that you're experiencing this?": {'answer_type': 'inline', 'yesno': True, 'linebreak': True},
        "Go ahead and reflect for a minute to try to clear your brain.": {'answer_type': 'text'},
        "What can you do to turn this around?": {'answer_type': 'list'}
    }
    answers = answer_questions_dict(questions_dict)
    export_to_csv('Operation Self', answers, list(questions_dict.keys()))


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


def perfect_day(frequency=None):
    print('Forget everything you just typed. Now,...\n')
    question = 'What does your perfect day look like?'
    if frequency:
        question = add_frequency_to_question(question, frequency)
    answer = answer_question(question, 'list', ordered=True)
    file_name = 'perfect_day'
    export_to_csv(file_name, answer, question)
    return perfect_day


def reflect():
    question = 'Take a minute to write a written reflection.'
    reflection = answer_question(question, 'text')
    export_to_csv('Refections', reflection, 'Reflection')
    return reflection


def physiology_check():
    '''Checks up on health stats for the day.'''
    file_name = 'Health Stats'
    questions = [
        'Do you feel well rested?',
        'Are you hydrated?',
        'Are you well fed?',
        'Did you (or are you going to) exercise today?',
        'Is the temperature fine for you?',
        'Is your environment clean and organized?',
        'Do you feel complete wellness?'
    ]
    answers = answer_questions(questions, 'inline', yesno=True)
    score = get_integrity_status(questions, answers)
    print(f'\nYour physiology is at {get_integrity_status(questions, answers)}.\n')
    column_names = [
        'Score',
        'Well Rested',
        'Hydrated',
        'Well Fed',
        'Movement',
        'Temperature',
        'Clean Environment',
        'Full of Health'
    ]
    answers = [score] + answers
    export_to_csv(file_name, answers, column_names)
    return answers


def priorities(frequency=None, write_checklist=False):
    questions = [
        'What are your top 3 personal priorities (starting with The ONE Thing)?',
        'What are your top 3 professional priorities (starting with The ONE Thing)?'
    ]
    priorities = answer_questions(questions, 'list', ordered=True, cap='auto')
    personal_priorities, work_priorities = priorities
    column_names = ['ONE Thing', 'Priority #2', 'Priority #3']
    export_to_csv('Personal Priorities', personal_priorities, column_names)
    export_to_csv('Work Priorities', work_priorities, column_names)
    return priorities


def prismatic_system():
    '''Walks user through Ryan Donaldson's PRISMATIC Goal Setting System.'''
    prismatic_questions_dict = {
        'What is your goal?': {'answer_type': 'inline'},
        'P: What People will you utilize to achieve your goal?': {'answer_type': 'list'},
        'R: What Resources will you utilzie to achieve your goal?': {'answer_type': 'list'},
        'I: What Identities will you embody to achieve your goal?': {'answer_type': 'list'},
        'S: What are the Specifics of your goal?': {'answer_type': 'list'},
        'M: What Metrics will you use to track progress towards goal?': {'answer_type': 'list'},
        'A: What Actions will you take to achieve your goal?': {'answer_type': 'list', 'ordered': True},
        'T: What are the Timelines for each action?': {'answer_type': 'list'},
        'I: What Information will you utilize to achieve your goal?': {'answer_type': 'list'},
        'C: What are your Criteria for Success to achieve this goal?': {'answer_type': 'list'},
    }
    column_names = [
        'Goal',
        'People',
        'Resources',
        'Identity',
        'Specifics',
        'Metrics',
        'Actions',
        'Information',
        'Criteria for Success'
    ]
    file_name = 'prismatic_goals'
    answers = answer_questions_dict(prismatic_questions_dict)
    export_to_csv(answers, column_names, file_name)
    return answers


def ten_ideas(set_topic=False, frequency=None):

    topic = check_for_topic() if set_topic else 'to improve your life'
    question = f'Name an idea to {topic}'
    answer = answer_question(question, 'list', cap=10)
    file_name = 'ideas'
    if frequency:
        file_name = f'{frequency} {file_name}'.title()
    export_to_csv(file_name, answer, question)
    return answer


def check_for_topic():
    print('Anything specific you want to accomplish?\n\n')
    topic = answer_question('I\'d like to', 'inline')
    if not topic:
        topic = 'improve your life'
    print()
    return topic


def type_of_person(pronoun='person'):
    question = f'What type of {pronoun} do you choose to be today?'
    type_of_person = answer_question(question, 'list', input_suffix=f'I choose to be the type of {pronoun} who ')
    export_to_csv('Type of Person', type_of_person, question)
    return type_of_person


def wins(frequency=None):
    question = 'What are your wins?'
    if frequency:
        question = add_frequency_to_question(question, frequency)
    wins = answer_question(question, 'list', ordered=True)
    print(f'Total Wins: {len(wins)}\n')
    export_to_csv('Wins', wins, 'Wins')
    return wins
