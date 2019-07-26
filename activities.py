#! Python3.7
# Reflector\activities.py

# -*- coding in: utf-8 -*-
from answerlogic import answer, display, export, pick_option, list_reflector, activity
from evernoteautogui import tasklist
import pandas as pd
import time
import os

class Activities():

    def acclaim_system(self):
        '''
        Walks through the acclaim System Created by Ryan Donaldson.
        '''

        # Acclaim System Questions

        physiology_questions = [
            'Did you sleep well today?',
            'Are you hydrated?',
            'Are you well fed?',
            'Are you in a clean, nice temperature environment?',
            'Are you feeling well (No sickness)?'
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
            'State 10 reasons why you love yourself.',
            'List 5 things you feel you are most competent at.'
        ]

        self_actualization_questions = [
            'List the 1 project that User is Most Excited to work on.',
            'List what skills that the User is going to use from the self esteem list',
            'List the actions that can be done to secure the success of that project',
            'List the criteria that will guage the success of that project.',
            'Express completion of this Board to Accountability Partners'
        ]

        acclaim_system_questions = [
            physiology_questions,
            security_questions,
            love_and_belonging_questions,
            self_esteem_questions,
            self_actualization_questions
        ]

        hierarchy_counter = 0

        maslows_hierarchy = ('physiology', 'security', 'love & belonging', 'self esteem', 'self actualization')

        self.acclaim_system_status = {
            'Physiology': None,
            'Security': None,
            'Love & Belonging': None,
            'Self-Esteem': None,
            'Self-Actualization': None
        }

        # Ask all yes or no questions (1st - 3rd section of the hierarchy)
        for question_list in acclaim_system_questions[:3]:
            print(f"{maslows_hierarchy[hierarchy_counter]}: \n".upper())
            responses = answer(question_list, answer_type='oneoff', yorn=True)
            if hierarchy_counter == 0:
                physiology_status = responses['Answers'].tolist()
                self.acclaim_system_status['Physiology'] = physiology_status
            elif hierarchy_counter == 1:
                security_status = responses['Answers'].tolist()
                self.acclaim_system_status['Security'] = security_status
            elif hierarchy_counter == 2:
                love_and_belonging_status = responses['Answers'].tolist()
                self.acclaim_system_status['Love & Belonging'] = love_and_belonging_status
            hierarchy_counter += 1

        # Ask all list questions
        for question_list in acclaim_system_questions[3:]:
            print(f"{maslows_hierarchy[hierarchy_counter]}:\n".upper())
            response = answer(question_list, answer_type='listed', ordered=True, cap=True, question_index=True)
            if hierarchy_counter == 3:
                self_esteem_status = response['Answers'].tolist()
                self.acclaim_system_status['Self-Esteem'] = self_esteem_status
            elif hierarchy_counter == 4:
                self_actualization_status = response['Answers'].tolist()
                self.acclaim_system_status['Self-Actualization'] = self_actualization_status
            hierarchy_counter += 1

        return self.acclaim_system_status

    def life_addition(self):

        addition = answer('What can you bring into your day to upgrade your performance?', answer_type='listed', ordered=True, cap=1)

        export('Life Additions', addition, report=['Additions'])

        return addition

    def breather(self):

        realization_questions = [
            'Do you realize life is meaningless?',
            'Do you realilze life only has the meaning you give it?',
            'Do you realize everything that exists can be either a truth or a lie based on perception?',
            'Do you realize that choosing is the only thing requierd?'
        ]

        print("Take a deep breath...\n")
        breath = answer(realization_questions, answer_type='yorn')
        print("Take another deep breath...\n")

    def delegation(self, frequency=None):
        '''Walks through process for where energy was spent and what can be done to become more efficient.'''

        delegation_quesitons = [
            'What took your energy?',
            'What non-ceo activities did you do?',
            'To Do\'s - What Can be delegated?',
            'What systems do we need?',
            'What can I stop doing?'
        ]

        columns = ['Energy Investments', 'Non CEO activities', 'Tasks to Delegate', 'Systems Needed', 'Stop List']

        delegation_report = activity('Delegation Report', delegation_quesitons, frequency=frequency, export='report', columns=columns)

        return delegation_report

    def upgrades(self, frequency=None):

        question = 'What can you bring into your life to upgrade your performance?'

        column = 'Upgrade'

        upgrade = activity('Upgrades', question, frequency=frequency, ordered=True, cap=1, export='report', columns=column)

        return improvements

    def priorities(self, frequency=None, write_checklist=False):

        questions = [
            f'What are your top 3 personal priorities (starting with the most important)?',
            f'What are your top 3 professional priorities (starting with the most important)?'
        ]

        priorities = activity('Priorities', questions, frequency=frequency, ordered=True, cap='auto')

        columns = ['ONE Thing', 'Priority #2', 'Priority #3']

        export("Personal Priorities", priorities[0], report=columns)
        export("Work Priorities", priorities[1], report=columns)

        if write_checklist == True:
            title = f'{frequency} Priorities'.title()
            tasklist(title, priorities, title, headings=['Personal', 'Work'])

        return priorities

    def wins(self, frequency=None):

        wins = activity('Wins', 'What are your wins?', frequency=frequency, export='Date')

        print(f'\nTotal Wins: {len(wins)}\n')

        return wins

    def dave_asprey(self):

        dave_asprey_questions = [
            'What am I grateful for?',
            'What can I do to make today great?',
            'What kind of person do I want to be today?'
        ]

        answer(dave_asprey_questions[0], answer_type='listed', ordered=True)
        answer(dave_asprey_questions[1:])

    def important_metrics(self):  # TODO: Complete this.

        metrics = [
            'Times Olga came: ',
            'Overall Happiness: ',
        ]

        pass

    def goals(self):
        '''Displays a previous list of goals, and either ads or sets new ones.'''

        goals = list_reflector('My Goals.txt', 'goals', 'What are your goals?')

        return goals

    def goal_stats(self): pass

    def gratitude(self):
        '''This function takes in a list of things you appreciate.'''

        # Make a list of things you appreciate
        gratitude = answer('Name as many things you appreciate as you\'d like.', answer_type='listed', ordered=True)

        # Add them to a list that builds overtime
        export('Gratitude List', gratitude, date=True)

        # Linebreak
        print()

        return gratitude

    def health_analysis(self):
        '''Collects a list of health information at the end of everday.'''
        health_analysis_questions = [
            'Did you brush your teeth today?',
            'Did you consume any added sugar today?',
            'Did you consume any bread today?',
            'Did you consume any dairy today?',
            'Did you consume any trans fats today?',
            'Did you consume any probiotics today?',
            'Did you consume any omega 3s today?',
            'Did you consume a multivitamin today?',
            'Did you exercise today?',
            'Did you stretch today?',
            'Did you meditate today?',
            'Did you do kegals today?',
            'Did you have sex today?',
            'Did you ejaculate today?',
            'Did you take a cold shower today?',
            'Did you get at least 30 minutes of sunlight today?',
            'Did you intentionally relax today?',
            'Did you take actions to create wealth today?',
            'Did you talk to your significant other today?',
            'Did you talk to any friends today?',
            'Did you tell yourself you love, accept, trust, and believe in yourself today?'
        ]

        # Collect answers from Health input & return a score
        health_results = answer(health_analysis_questions, answer_type='oneoff', yorn=True)
        print()  # Linebreak

        # Send data to a spreadsheet to keep track of progress overtime.

        return health_results

    def lessons(self):
        '''Allows user to share what lessons they've learned this day.'''

        lessons = answer("What lessons did you learn or relearn today?", answer_type="listed")

        export('Daily Lessons', lessons, date=True)

        return lessons

    def life_givers(self):

        life_givers = answer('What life-giving situations did you experience today?', answer_type='listed')

        export('Life Givers', life_givers)

    def meaningful_experience(self):

        meaningful_experience = answer('What was one meaningful experience you had today?')

        export('Meaningful Experiences', meaningful_experience, date=True)

        return meaningful_experience

    def nutrition_analysis(self, meal='breakfast'):
        '''Let's User Input what time they're eating lunch'''

        # Collect a list of ingredients the user is going to eat for breakfast
        ingredients = answer(f'What healthy {meal} ingredients are you going to eat today?', answer_type='listed')

        # Check if this compination ingredients is a new recipe
        # recipe_check = input('Is this a new recipe? (y/n): ')
        # if recipe_check == 'y':
        # 	recipe = input('What is the name of this recipe: ')
        #
        # 	# Add recipe to a recipe list
        # 	pass
        # 	print(f'{recipe} has been added to Recipe List!')

        supplements = answer('What supplements are you going to take with your meal?', answer_type='listed')

        # Linebreak
        print()

    def physiology_check(self):
        '''Checks up on health stats for the day.'''

        physiology_questions = [
            'Do you feel well rested?',
            'Are you hydrated?',
            'Are you well fed?',
            'Did you (or are you going to) exercise today?',
            'Is the temperature fine for you?',
            'Is your environment clean and organized?',
            'Do you feel complete wellness?'
        ]

        physiology_stats = answer(physiology_questions, answer_type='oneoff', yorn=True)

        health = 100
        health_key = 100 / 7

        for stat in physiology_stats:
            if stat == 'n':
                health -= health_key

        health_score = f'{int(health)}%'

        print(f'\nYour physiology is at {health_score}.\n')

        health_columns = ['Score', 'Well Rested', 'Hydrated', 'Well Fed', 'Movement', 'Temperature', 'Clean Environment', 'Full of Health' ]

        export('Health Stats', [health_score] + physiology_stats, report=health_columns)


        return physiology_stats

    def power_questions(self):

        tony_robbins_power_questions = [
            'What am I happy about in my life right now?',
            'What am I excited about in my life right now?',
            'What am I proud about in my life right now?',
            'What am I grateful about in my life right now?',
            'What am I enjoying in my life right now?',
            'What am I committed to in my life right now?',
            'Who do I love? Who loves me?'
        ]

        # Answers each question in a listed answer format.
        answer(tony_robbins_power_questions, answer_type='listed', ordered=True, question_index=True)

    def prismatic_system(self):
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

        prismatic_questions = [
            'What is your goal: ',
            'What people will you utilize to achieve your goal?',
            'What resources will you utilzie to achieve your goal?',
            'What identities will you embody to achieve your goal?',
            'What are the specifics of your goal?',
            'What metrics will you use to track progress towards goal?',
            'What actions will you take to achieve your goal?',
            'What are the timelines for each action?',
            'What information will you utilize to achieve your goal?'
            'What are your Criteria for success to achieve this goal?'
        ]

        goal = input(prismatic_questions[0])
        print()
        resources = answer(prismatic_questions[1:6], answer_type='listed')
        action_plan = answer(prismatic_questions[6:8], answer_type='listed', ordered=True)
        resources.append(answer(prismatic_questions[8:]), answer_type='listed')

        return resources, action_plan

    def review(self, filename, subject):
        '''Opens a txt file and shows user what ideas they wrote down.'''

        print(f'Take a moment to review your {subject} you made and see what might be useful...')
        time.sleep(1.5)
        os.startfile(f'.\\Data Storage\\{filename}')
        os.system('pause')

    def self_love(self):
        '''Gives the user an opportunity to share some love to themselves.'''

        # Asks 10 reasons why the user loves themself.
        self_love_reasons = answer('List 10 reasons why you love yourself.', answer_type='listed', ordered=True,
                                   cap='auto')

        export('Self-Love List', self_love_reasons)

        return self_love_reasons

    def stressors(self):

        stressors = answer('What stressors (if any) did you experience today and how can you resolve them?', answer_type='listed')

        export('Stressors', stressors)

        return stressors

    def success_metrics(self):

        success_questions = [

        ]

    def tasks(self):

        tasks = list_reflector('My Tasks.txt', 'tasks', 'What tasks do you have (if any) floating around in your mind?')

        return tasks

    def ten_ideas(self, topic=None, frequency=None, write_checklist=False):
        ''' This function takes in 10 ideas you come up with to improve
        your life. '''

        # Add topic if there was no topic given
        if topic == None:
            # Set the topic for your ideas
            topic = input('Anything specific you want to accomplish?\n\nI\'d like to: ')
            if topic == '':
                topic = 'improve your life'
        else:
            pass

        # Collect 10 ideas in a list
        ideas = answer(f'Name an idea to {topic}', answer_type='oneoff', loop=10)
        print()  # Linebreak

        # Send ideas to an ideas list
        filename = 'Ideas'
        if frequency:
            filename = f'{frequency} {filename}'.title()
        export(f'{filename} List', ideas, date=True)

        if write_checklist == True:
            tasklist(filename, ideas, 'Idea Lists')

        return ideas

    def the_one_thing(self):
        '''Asks the focus question from the book "The One Thing".'''

        one_thing_question = "What is the one project you can work on so that all of the others become either easier or unnecessary?\n"

        one_thing = input(one_thing_question)

        export('The One Thing', one_thing, overwrite=True)

        # Linebreak
        print()


class MainActivities(Activities):

    def morning_reflection(self):
        '''Reflection to get the day started in a positive, epic mindset.'''

        print('Good morning handsome ;) \n')

        self.physiology_check()
        self.goals()
        self.gratitude()
        self.life_addition()
        priorities = self.priorities('daily')
        self.self_love()
        self.ten_ideas()

        tasklist('Priorities', priorities, 'Daily Priorities', headings=['Personal', 'Work'])

    def end_of_day_reflection(self):


        print('Good evening sir ;) \n')

        wins = self.wins()
        lessons = self.lessons()
        appreciation_list = self.gratitude()
        meaningful_experience = self.meaningful_experience()
        self_love = self.self_love()
        improvements = self.ten_ideas()
        goals = self.goals()
        tasks = self.tasks()

    def weekly_reflection(self):
        print('I hope you had a nice week sir! :)\n')

        self.wins('weekly')
        self.review('Ideas List.txt','ideas')
        priorities = self.priorities('weekly')
        ideas = self.ten_ideas('crush it this week.')

        tasklist('Weekly Priorities', priorities, 'Weekly Priorities', headings=['Personal', 'Work'])
        tasklist('Weekly Ideas', ideas, 'Idea Lists')



    def birthday_reflection(self):
        '''Reflection to be done on your birthday.'''
        print('Happy birthday! :)\n')

        self.wins('yearly')
        # self.review('Ideas List.txt', 'ideas')
        priorities = self.priorities('yearly')
        ideas = self.ten_ideas('make this year your most amazing year so far.')

        tasklist('Yearly Priorities', priorities, 'Yearly Priorities', headings=['Personal', 'Work'])
        tasklist('Yearly Ideas', ideas, 'Idea Lists')


activities = Activities()

main_activities = MainActivities()

def main():
    activities.physiology_check()

if __name__ == '__main__':
    main()