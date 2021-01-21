import itertools

from reflector.answer import (
    answer_question,
    answer_questions,
    answer_questions_dict
)
from reflector.export import export_to_csv
from reflector.activity import activity
from reflector.utils import (
    get_and_print_integrity_status,
    add_frequency_to_question
)


def morning_reflection():
    print('Good morning handsome ;) \n')
    reflect()
    physiology()
    daily_competency()
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
    print('Happy birthday! :)\n')
    wins('yearly')
    improvements()
    priorities('yearly')
    ten_ideas('make this year your most amazing year so far.')


def acclaim_system(file_name='Accliam System'):
    '''Walks through the acclaim System Created by Ryan Donaldson, with some added parts.'''
    functions = [
        physiology,
        security,
        love_and_belonging,
        self_esteem,
        self_actualization
    ]
    categories = [
        'Physiology',
        'Security',
        'Love & Belonging',
        'Self-Esteem',
        'Self-Actualization',
    ]
    all_answers = []
    all_columns = []
    for category, function in zip(categories, functions):
        print(f'{category}:\n')
        answers, columns = function()
        all_answers.append(answers)
        all_columns.append(columns)
    answers = list(itertools.chain.from_iterable(all_answers))
    columns = list(itertools.chain.from_iterable(all_columns))
    export_to_csv(file_name, answers, columns)


def physiology(file_name='Physiology'):
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
    score = get_and_print_integrity_status(questions, answers, 'phsiology')
    column_names = [
        'Physiology Score',
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
    return answers, column_names


def security(file_name='Security'):
    questions = [
        'Are you financially well off or have a financial plan?',
        'Are you physically safe?'
    ]
    answers = answer_questions(questions, 'inline', yesno=True)
    answers.insert(0, get_and_print_integrity_status(questions, answers, topic='security'))
    column_names = ['Security Score', 'Financially Safe', 'Physically Safe']
    export_to_csv(file_name, answers, column_names)
    return answers, column_names


def love_and_belonging(file_name='Love & Belonging'):
    questions = [
        'Have you messaged 5 of your friends saying "I appreciate you & you matter to me"?',
        'Have you talked to your favorite person or Significant Other?'
    ]
    answers = answer_questions(questions, 'inline', yesno=True)
    answers.insert(0, get_and_print_integrity_status(questions, answers, 'love & belonging'))
    column_names = [
        'Love & Belonging Score', 
        '5 Friends Appreciated', 
        'SO / Favorite Person Talked To'
    ]
    export_to_csv(file_name, answers, column_names)
    return answers, column_names


def self_esteem(file_name='Self Esteem'):
    questions = [
        'What are 10 reasons you love yourself?',
        'What 5 things do you feel most competent at today?',
    ]
    answers = answer_questions(questions, 'list', ordered=True, cap='auto')
    column_names = ['Self Love Reasons', '5 Daily Competencies']
    export_to_csv(file_name, answers, column_names)
    return answers, column_names


def self_actualization(file_name='Self Actualization'):
    questions = {
        'What 1 project are you most excited to work on?': {'answer_type': 'inline', 'linebreak': True},
        'What skills are you going to use from the self esteem list?': {'answer_type': 'list'},
        'What actions (in order) can be done to secure the success of that project?': {'answer_type': 'list', 'ordered': True},
        'What criteria will gauge the success of that project?': {'answer_type': 'list'},
        'Did you express completion of this board to your accountability partners?': {'answer_type': 'inline', 'yesno': True}
    }
    answers = answer_questions_dict(questions)
    column_names = [
        'Project Your Most Excited For',
        'Skills to Apply to Favorite Project',
        'Actions for Project Success',
        'Criteria for Project Success',
        'Shared With Accountability Partners',
    ]
    export_to_csv(file_name, answers, column_names)
    return answers, column_names


def delegation(frequency=None):
    quesitons = [
        'What took your energy?',
        'What non-ceo activities did you do?',
        'To Do\'s - What Can be delegated?',
        'What systems do we need?',
        'What can I stop doing?'
    ]
    columns = [
        'Energy Investments',
        'Non CEO activities',
        'Tasks to Delegate',
        'Systems Needed',
        'Stop List'
    ]
    delegation_report = activity('Delegation Report', quesitons, frequency=frequency, export='report', columns=columns)
    return delegation_report


def easier_life():
    question = 'Name an idea to make your life easeir'
    easier_life_ideas = answer_question(question, 'list', cap=5)
    print()
    export_to_csv('Easier Life', easier_life_ideas)
    return easier_life_ideas


def goals():
    '''Displays a previous list of goals, and either ads or sets new ones.'''
    question = 'What are your goals?'
    file_name = 'My Goals'
    goals = answer_question(question, 'list')
    export_to_csv(file_name, goals, question)
    return goals


def gratitude():
    file_name = 'Gratitude List'
    question = 'What are you grateful for?'
    gratitude_list = answer_question(question, 'list', ordered=True, input_suffix='I\'m grateful for ')
    export_to_csv(file_name, gratitude_list, column_headers='What are you grateful for?')
    return gratitude_list


def self_love():
    file_name = 'Self Love'
    question = 'What are 10 Reasons you love yourself?'
    answer = answer_question(question, 'list', ordered=True, cap='auto', input_suffix="I love myself because ")
    column_name = '10 Reasons I Love Myself'
    export_to_csv(file_name, answer, column_name)
    return answer


def improvements():
    question = 'What can you do to improve?'
    improvements = answer_question(question, 'list')
    export_to_csv('Improvements', improvements, question)
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


def ten_ideas(topic='improve your life', frequency=None):
    question = f'Name an idea to {topic}'
    answer = answer_question(question, 'list', cap=10)
    file_name = 'ideas'
    if frequency:
        file_name = f'{frequency} {file_name}'.title()
    export_to_csv(file_name, answer, question)
    return answer


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

def daily_competency():
    question = 'What 5 things do you feel the most competent at today?'
    answer = answer_question(question, answer_format='list', ordered=True, cap='auto')
    export_to_csv('Daily Competencies', answer, 'Daily Competencies')
    return answer
    