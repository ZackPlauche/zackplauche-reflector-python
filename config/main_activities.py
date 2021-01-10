from .activities import *

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
    # self_love()  # TODO: Accidentally deleted, need to restore to activities.py
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
    # self_love()  # TODO: Accidentally deleted, need to restore to activities.py
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