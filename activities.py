#! Python3.7
# Reflector\activities.py

# -*- coding in: utf-8 -*-
from utils import *
from evernoteautogui import tasklist
import pandas as pd
import time
import os

from answer import answer, answer_list


class Activities():

    # TODO: Save information somewhere somehow
    def acclaim_system(self):
        '''
        Walks through the acclaim System Created by Ryan Donaldson, with some added parts.
        '''

        # Acclaim System Questions

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
            'State 10 reasons why you love yourself.',
            'List 5 things you feel you are most competent at.'
        ]

        self_actualization_questions = [
            'List the 1 project that you\'re Most Excited to work on',
            'List what skills that you\'re going to use from the self esteem list',
            'List the actions that can be done to secure the success of that project',
            'List the criteria that will guage the success of that project.',
            # TODO: Make the program automatically share on Facebook/send to fb group
            'Express completion of this board to your accountability partners'
        ]

        acclaim_system_questions = [
            physiology_questions,
            security_questions,
            love_and_belonging_questions,
            self_esteem_questions,
            self_actualization_questions
        ]

        acclaim_system_status = {
            'Physiology': None,
            'Security': None,
            'Love & Belonging': None,
            'Self-Esteem': None,
            'Self-Actualization': None
        }

        # Run through each stage of the acclaim system showing what stage the user is in and asking the questions
        for hierarchy_stage, stage_questions in zip(acclaim_system_status.keys(), acclaim_system_questions):

            # Print what part of the hierarchy the user is answering in:
            print(f'{hierarchy_stage.upper()}:\n')

            if stage_questions in acclaim_system_questions[:3]:
                # Ask questions for user to answer
                status = answer_list(stage_questions,
                                     answer_type='inline', yesno=True)

                # Populate hierarchy stage integrity
                stage_integrity = integrity(stage_questions, status)

                # Print the hierarchy stage's integrity in an easy to read format
                print(
                    f'\nYour {hierarchy_stage.lower()} is at {stage_integrity}!\n')

            # Self-esteem questions
            elif stage_questions is acclaim_system_questions[3]:
                self_esteem = answer_list(
                    stage_questions, answer_type='list', ordered=True, cap='auto')

            # Self-actualization questions
            elif stage_questions is acclaim_system_questions[4]:
                favorite_project = answer_list(
                    stage_questions[0], answer_type='inline')
                print()
                action_lists = answer_list(
                    stage_questions[1:4], answer_type='list', ordered=True)
                share = answer_list(
                    stage_questions[4], answer_type='inline', yesno=True)

    def life_addition(self):

        addition = answer('What can you bring into your day to upgrade your performance?',
                          answer_type='list', ordered=True, cap=1)

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
        breath = answer_list(realization_questions, answer_type='inline', yesno=True)
        print("Take another deep breath...\n")

    def start_stop_keep(self):

        questions = [
            "What should you start doing?",
            "What should you stop doing?",
            "What should you keep doing?"
        ]

        columns = ['Start', 'Stop', 'Keep']

        report = activity('Start Stop Keep', questions,
                          export='report', columns=columns)

        return report

    def delegation(self, frequency=None):
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

    def upgrades(self, frequency=None):

        question = 'What can you bring into your life to upgrade your performance?'

        column = 'Upgrade'

        upgrade = activity('Upgrades', question, frequency=frequency,
                           ordered=True, cap=1, export='report', columns=column)

        return improvements

    def dave_asprey(self):

        dave_asprey_questions = [
            'What am I grateful for?',
            'What can I do to make today great?',
            'What kind of person do I want to be today?'
        ]

        answer(dave_asprey_questions[0], answer_type='list', ordered=True)
        answer_list(dave_asprey_questions[1:])

    def easier_life(self):

        easier_ideas = answer(
            'Name an idea to make your life easier', answer_type='list', cap=5)
        print()

        export('Easy Ideas', easier_ideas)

        return easier_ideas

    def goals(self):
        '''Displays a previous list of goals, and either ads or sets new ones.'''

        goals = list_reflector('My Goals.txt', 'goals', 'What are your goals?')

        return goals

    def goal_stats(self): pass

    def gratitude(self):
        '''This function takes in a list of things you appreciate.'''

        # Make a list of things you appreciate
        gratitude = answer(
            'What are you grateful for?', answer_type='list', ordered=True)

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
        health_results = answer_list(health_analysis_questions,
                                answer_type='inline', yesno=True)
        print()  # Linebreak

        # Send data to a spreadsheet to keep track of progress overtime.

        return health_results

    def improvements(self):

        improvements = answer('What can you do to improve?', answer_type='list')

        export('Improvements', improvements)

        return improvements

    def intentions(self):

        intentions = answer("What are your intentions for the day?", answer_type='list')

        export('Intentions', intentions)

        return intentions

    def lessons(self):
        '''Allows user to share what lessons they've learned this day.'''

        lessons = answer(
            "What lessons did you learn or relearn today?", answer_type="list")

        export('Daily Lessons', lessons, date=True)

        return lessons

    def life_givers(self):

        life_givers = answer(
            'What life-giving situations did you experience today?', answer_type='list')

        export('Life Givers', life_givers)

    def meaningful_experience(self):

        meaningful_experience = answer(
            'What was one meaningful experience you had today?', answer_type='text')

        print(meaningful_experience)

        export('Meaningful Experiences', meaningful_experience, date=True)

        return meaningful_experience

    def not_doing(self):

        not_doing = answer('What are you not doing?', answer_type='list')

        return not_doing

    def nutrition_analysis(self, meal='breakfast'):
        '''Let's User Input what time they're eating lunch'''

        # Collect a list of ingredients the user is going to eat for breakfast
        ingredients = answer(
            f'What healthy {meal} ingredients are you going to eat today?', answer_type='list')

        # Check if this compination ingredients is a new recipe
        # recipe_check = input('Is this a new recipe? (y/n): ')
        # if recipe_check == 'y':
        # 	recipe = input('What is the name of this recipe: ')
        #
        # 	# Add recipe to a recipe list
        # 	pass
        # 	print(f'{recipe} has been added to Recipe List!')

        supplements = answer(
            'What supplements are you going to take with your meal?', answer_type='list')

        # Linebreak
        print()

    def operation_self(self):
        """This program is for when you're feeling low self esteem / fear that might be fucking up your life at the moment."""

        print("\nThe SELF in this activity is an acronym, that stands for \"Self Esteem Low / Fear\"\nand was made to be a guide out of your temporary darkness and move you to a more empowered state.")

        questions = [
            "Did you poop today?",
            "Did you tell your significant other that you're experiencing this?",
            "Go ahead and reflect for a minute to try to clear your brain.",
            "What can you do to turn this around?"
        ]

        status_list = answer_list(questions[:2], answer_type="inline", yesno=True)
        reflection = answer(questions[2])
        actions = answer(questions[3], answer_type="list")

    def operation_red_dragon(self):
        "For when she's on her period."
        print("\nSo, you're women is on her period huh? Perfect. That's what this program is designed for.\n")

        print("""Here's what you should probably look at doing.

        1. Breathe, everything is going to be ok. And you have to be strong here, so start with this one.
        2. Whether you like it or not, you'll need to do more chores. Take care of something she normally does (like laundry, feeding the animals, etc.)
        3. Make sure to have some kind of sugars or chocolate in the house. Her body is going through a transformation that requires a lot of pain and her ovaries are committing sapuku.
        4. Flowers and some other type of girly gift.
        5. Be a bit more attentive and make sure to not make any mistakes for the most part in general. In fact, I'd do one of two things: stay out all day or make an in day the most amazing in day possible. Try having a movie day or something like this.
        6. Finally, this is her time to shine, so let her.
        7. Also, if she's down, have sex and make her cum.""")

        print('\nThat\'s all for now.')

    def perfect_day(self, frequency):

        print('Forget everything you just typed. Now,...\n')

        perfect_day = activity('Perfect Day', 'What does your perfect day look like?',
                               frequency=frequency, ordered=True, export='date')

        return perfect_day

    def reflect(self):

        reflection = answer(
            'Take a minute to write a written reflection.\n(linebreaks are enabled. To end reflection, press "." on a new line and press enter)')

        return reflection

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

        physiology_stats = answer(
            physiology_questions, answer_type='inline', yesno=True)

        physiology_score = integrity(physiology_questions, physiology_stats)

        print(f'\nYour physiology is at {physiology_score}.\n')

        physiology_columns = ['Score', 'Well Rested', 'Hydrated', 'Well Fed',
                              'Movement', 'Temperature', 'Clean Environment', 'Full of Health']

        export('Health Stats', [physiology_score] +
               physiology_stats, report=physiology_columns)

        return physiology_stats

    def security_check(self):
        '''Checks up on security stats for the day.'''

        security_questions = [
            'Are you financially well off or have a financial plan?',
            'Are you physically safe?'
        ]

        security_stats = answer(
            security_questions, answer_type='inline', yesno=True)

        security_score = integrity(security_questions, security_stats)

        print(f'\nYour security is at {security_score}.\n')

        security_columns = ['Score', 'Financially Sound', 'Physically Safe']

        export('Security Stats', [security_score] +
               security_stats, report=security_columns)

        return security_stats

    def love_and_belonging_check(self):
        '''Checks up on health stats for the day.'''

        love_and_belonging_questions = [
            'Have you messaged 5 of your friends saying "I appreciate you & you matter to me"?',
            'Have you talked to your favorite person or Significant Other?'
        ]

        love_and_belonging_stats = answer(
            love_and_belonging_questions, answer_type='inline', yesno=True)

        love_and_belonging_score = integrity(
            love_and_belonging_questions, love_and_belonging_stats)

        print(f'\nYour love and belonging is at {love_and_belonging_score}.\n')

        love_and_belonging_columns = [
            'Score', 'Friend Appreciation', 'Significant Other Communication']

        export('Love and Belonging Stats', [
               love_and_belonging_score] + love_and_belonging_stats, report=love_and_belonging_columns)

        return love_and_belonging_stats

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

        # Answers each question in a list answer format.
        answer(tony_robbins_power_questions, answer_type='list',
               ordered=True, question_index=True)

    def priorities(self, frequency=None, write_checklist=False):

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
        resources = answer(prismatic_questions[1:6], answer_type='list')
        action_plan = answer(
            prismatic_questions[6:8], answer_type='list', ordered=True)
        resources.append(answer(prismatic_questions[8:]), answer_type='list')

        return resources, action_plan

    def review(self, filename, subject):
        '''Opens a txt file and shows user what ideas they wrote down.'''

        print(
            f'Take a moment to review your {subject} you made and see what might be useful...')
        time.sleep(1.5)
        os.startfile(f'.\\Data Storage\\{filename}')
        os.system('pause')

    def self_love(self):
        '''Gives the user an opportunity to share some love to themselves.'''

        # Asks 10 reasons why the user loves themself.
        self_love_reasons = answer('List 10 reasons why you love yourself.', answer_type='list', ordered=True,
                                   cap='auto')

        export('Self-Love List', self_love_reasons)

        return self_love_reasons

    def stressors(self):

        stressors = answer(
            'What stressors (if any) did you experience today and how can you resolve them?', answer_type='list')

        export('Stressors', stressors)

        return stressors

    def success_metrics(self):

        print('Please report your success metrics for the day (DON\'T LEAVE BLANK): \n')

        dream_metrics = {
            # "Sleep Quality": "How was your sleep overall? (0-5)",
            # "Average Dream Quality": "How were your dreams? (0-5)",
            # "Dreams": "How many dreams did you have?",
            # "Dreams Captured": "How many dreams did you write out?",
            # "Nightmares": "How many of your dreams were nightmares?",
            # "Recurring Dreams": "How many dreams were recurring?",
            # "Lucid Dreams": "How many of your dreams were lucid?",
            # "Reality Checks": "How many times did you reality check?",
            # "Hours Since Last Meal Before Bed": "How many hours before bed did you last eat?",
        }

        efficiency_metrics = {
            # "Shopping Quantity": "How many times did you go shopping today?",
            # "Proactive Shopping": "Did you go shopping for more than 1 day?",
        }

        health_metrics = {
            # "Emotional Level": "How are you feeling emotionally overall? (1-5)",
            # "Relaxed Level": "How relaxed do you feel? (1-5)",
            # "Soreness Level": "How sore are you? (0-5)",
            # "Tightness Level": "How tight are your muscles? (0-5)",
            # "Good Open Posture": "How often were you holding good posture? (0-5)",
            # "Deep Breathing Average": "How often were you breathing deep? (0-5)",
            # "Poop Quantity": "How many times did you poop?",
            # "Poops Without Phone": "How many times did you poop without your phone?",
            # "Head Scratching Quantity": "How many times did you scratch your head?",
            # "Booger Quantity": "How many many times did you pick your nose & eat your booger?",
            # "Nail Biting Quantity": "How many times did you bite your nails?",
            # "Pimples Popped / Picked": "How many pimples did you pop / pick at?",
            # "Moisturize Quantity": "How many times did you moisturize your face?",
            # "Exercise Time": "How long did you exercise today?",
            # "Environment Cleanliness": "How clean was your environment? (0-5)",
            # "Cleaned": "Did you (or are you going to) clean?",
            # "Reflected": "Did you reflect today?",
            # "Videogames": "Did you play videogames?",
            # "Sunlight": "Did you get sunlight?",
            # "Processed Meat": "Did you eat processed meat?",
            # "Potato / Corn Chips": "Did you eat potato/corn chips?",
            # "Eggs": "Did you eat eggs?",
            # "Red Meat (non-processed)": "Did you eat red meat?",
            # "Fish": "Did you eat fish?",
            # "Added Sugar (Bread / Sweets)": "Did you eat sweets or bread (including crackers or crutons)?",
            # "High Glycemic Fruits": "Did you eat high glycemic fruits (bananas, apples)?",
            # "Berries": "Did you eat berries?",
            # "Omega 3s": "Did you eat omega-3s?",
            # "Vegetables": "Did you eat vegetables?",
            # "Nightshades": "Did you eat nightshades?",
            # "Cheese": "Did you eat cheese?",
            # "Milk": "Did you drink dairy milk?",
            # "Alcohol": "Did you drink alcohol?",
            # "High Caffeine Drinks": "Did you drink coffee, energy drinks, or yerba mate?",
            # "Breakfast": "Did you eat breakfast?",
            # "Lunch": "Did you eat lunch?",
            # "Dinner": "Did you eat dinner?",
            # "Snacking": "Did you snack throughout the day?",
            "Flossing": "Did you floss?",
        }

        finance_metrics = {
            "Business Income": "How much money did you earn from business(USD)?",
            "Family Income": "How much money did you earn from family/friends (USD)?",
            # "Saved Income": "How much money did you put to savings (USD)?",
            # "Credit Card Debt Paid": "How much money did you pay off of your credit card?",
            "Business Investments": "How much money did you spend on business stuff (USD)?",
            "Personal Investments": "How much money did you spend on personal stuff (USD)?",
            "Simple Checking Balance": "How much money do you have in your checking account (USD)?",
            "Simple Savings Balance": "How much money do you have in savings (USD)?",
            "Chase Card Balance": "How much money do you have on your credit card (USD)?",
        }

        business_metrics = {
            # "Wyzant Proposals Sent": "How many Wyzant proposals did you send?",
            # "Upwork Proposals Sent": "How many Upwork proposals did you send?",
            # "Processes Built": "How many processes did you build / map out?",
            # "Processes Optimized": "How many processes did you optimize?",
            # "Processes Automated": "How many processes did you automate?",
            # "Processes Delegated": "How many processes did you delegate?",
            # "Facebook Group Value Added": "How many times did you add value to a Facebook group?",
            # "Collaborator Outreach": "How many potential collaborators did you reach out to?",
            "Hours Worked": "How many hours did you spend working today?",
            # "Skill Development Hours": "How many hours did you spend developing a skill today?",
            # "Reading Hours": "How many hours did you spend reading today?",
            # "Russian Lessons": "How many Russian duolingo lessons did you do?",
            # "Times Destracted": "How many times did you get distracted today?",
        }

        relationship_metrics = {
            # "Arguments with Olga": "How many times did you and Olga argue?",
            "Olga Initiated Sex Quantity": "How many times did you and Olga have sex after Olga initiated?",
            "Me Initiated Sex Quantity": "How many times did you and Olga have sex after you initiated?",
            "Olga Initiated Blowjob Quantity": "How many times did Olga blow you with Olga initiating?",
            "Me Initiated Blowjob Quantity": "How many times did Olga blow you with you initiating?",
            "Masterbation Quantity": "How many times did you masterbate?",
            "Olga Initiated Compliment Quantity": "How many times did Olga compliment you without you initiating?",
            # "Toilet Seat Closed": "Did you close the toilet seat after every use?",
            # "Put Down Shower": "Did you put the shower back to faucet mode?",
            # "Tub Area Cleaned": "Did you clean the water from the tub after every use?",
            # "Tub Items Removed": "Did you pick up everything from the tub after every use?",
            # "All Hot Water Without Permission": "Did you use all the hot water without asking Olga?",
            # "Equal Food & Drink Purchase": "Did you get an equal amount of food for both yourself and Olga?",
            # "Olga's Snacks Stolen": "Did you not eat Olga's snacks without asking or buying her a new one?",
            # "Water Poof": "Did you water poof?",
        }

        growth_metrics = {
        }

        metric_dicts = [
            dream_metrics,
            efficiency_metrics,
            health_metrics,
            finance_metrics,
            business_metrics,
            relationship_metrics,
            # growth_metrics
        ]

        metrics = []
        metric_questions = []

        for metric_dict in metric_dicts:
            metrics += metric_dict.keys()
            metric_questions += metric_dict.values()

        success_metrics = answer(metric_questions, answer_type='inline')
        print()

        export('Success Metrics 2020-6-27', success_metrics,
               report=metrics, time='full')

    def ten_ideas(self, topic=None, frequency=None, write_checklist=False):
        ''' This function takes in 10 ideas you come up with to improve
        your life. '''

        # Add topic if there was no topic given
        if topic == None:
            # Set the topic for your ideas
            topic = input(
                'Anything specific you want to accomplish?\n\nI\'d like to: ')
            if topic == '':
                topic = 'improve your life'
        else:
            pass

        # Collect 10 ideas in a list
        ideas = answer(f'Name an idea to {topic}',
                       answer_type='inline', loop=10)
        print()  # Linebreak

        # Send ideas to an ideas list
        filename = 'Ideas'
        if frequency:
            filename = f'{frequency} {filename}'.title()
        export(f'{filename} List', ideas, date=True)

        if write_checklist == True:
            tasklist(filename, ideas, 'Idea Lists')

        return ideas

    def turn_around(self):

        turn_around = answer(
            'What actions can you take to turn this around?', answer_type='list')

        return turn_around

    def type_of_person(self):
        """Allows the user to choose what type of person they're going to be that day."""

        type_of_person = answer(
            "What type of person do you choose to be today?", answer_type="list")
        print()

        return type_of_person

    def wins(self, frequency=None):

        wins = activity('Wins', 'What are your wins?',
                        frequency=frequency, export='Date')

        print(f'\nTotal Wins: {len(wins)}\n')

        return wins


class MainActivities(Activities):

    def morning_reflection(self):
        '''Reflection to get the day started in a positive, epic mindset.'''

        print('Good morning handsome ;) \n')

        self.reflect()
        self.physiology_check()
        self.goals()
        self.type_of_person()
        self.intentions()
        self.gratitude()
        priorities = self.priorities('daily')
        self.self_love()
        self.easier_life()
        # self.ten_ideas()
        self.reflect()

        # tasklist('Priorities', priorities, 'Daily Priorities',
        #          headings=['Personal', 'Work'])

    def end_of_day_reflection(self):

        print('Good evening sir! :) \n')
        self.reflect()
        self.wins()
        self.improvements()
        self.lessons()
        self.gratitude()
        self.meaningful_experience()
        self.self_love()
        self.ten_ideas()
        self.goals()
        priorities = self.priorities(frequency='tomorrow')
        self.reflect()

        # tasklist('Priorities', priorities, 'Daily Priorities',
        #          headings=['Personal', 'Work'])

    def weekly_reflection(self):
        print('I hope you had a nice week sir! :)\n')

        self.reflect()
        self.wins('weekly')
        self.improvements()
        priorities = self.priorities('weekly')
        ideas = self.ten_ideas('crush it this week.')
        perfect_day = self.perfect_day('weekly')
        self.reflect()

        # tasklist('Weekly Priorities', priorities,
        #          'Weekly Priorities', headings=['Personal', 'Work'])
        # tasklist('Weekly Ideas', ideas, 'Idea Lists')

    def monthly_reflection(self):
        print('Wow, a whole month. I hope you had a nice month sir! :)\n')

        self.reflect()
        self.wins('monthly')
        self.improvements()
        priorities = self.priorities('monthly')
        ideas = self.ten_ideas('crush it this month.')
        perfect_day = self.perfect_day('monthly')

        # tasklist('Monthly Priorities', priorities,
        #          'Monthly Priorities', headings=['Personal', 'Work'])
        # tasklist('Monthly Ideas', ideas, 'Idea Lists')

    def birthday_reflection(self):
        '''Reflection to be done on your birthday.'''
        print('Happy birthday! :)\n')

        self.wins('yearly')
        self.improvements()
        priorities = self.priorities('yearly')
        ideas = self.ten_ideas('make this year your most amazing year so far.')

        # tasklist('Yearly Priorities', priorities,
        #          'Yearly Priorities', headings=['Personal', 'Work'])
        # tasklist('Yearly Ideas', ideas, 'Idea Lists')

    def off_the_wagon(self):
        self.reflect()
        self.not_doing()
        self.turn_around()


activities = Activities()
main_activities = MainActivities()


def main():
    activities.goals()


if __name__ == '__main__':
    main()
