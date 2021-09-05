from datetime import datetime

import pandas as pd

from reflector.questions import YesNoQuestion, YES_ANSWERS
from reflector.utils import listify
from reflector.settings import STORAGE_DIRECTORY


class Activity:

    def __init__(self, name, questions, intro_text=''):
        self.name = name
        if not questions:
            raise ValueError('Argument "questions" list cannot be empty.')
        self.questions = list(questions)
        self.columns = [question.name for question in self.questions]
        self.intro_text = intro_text

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.__str__()}>'

    def run(self) -> list:
        self._print_intro_text()
        self._ask_questions()
        self._export()
        return self.answers

    def _print_intro_text(self):
        if self.intro_text:
            print(self.intro_text, end='\n\n')

    def _ask_questions(self) -> list:
        self.answers = []
        for question in self.questions:
            answer = question.ask()
            if isinstance(answer, list):
                answer = listify(answer)
            self.answers.append(answer)
        return self.answers

    def _export(self):
        if not self.answers:
            raise AttributeError('Cannot export Activity without answer data.')
        file_path = STORAGE_DIRECTORY / f'{self.name}.csv'
        df = pd.DataFrame(data=[[str(datetime.now())] + self.answers], columns=['DateTime'] + self.columns)
        if file_path.exists():
            previous_df = pd.read_csv(file_path)
            df = previous_df.append(df)
        df.to_csv(file_path, index=False)


class IntegrityActivity(Activity):

    def __init__(self, name, yes_no_questions, category, intro_text: str = ''):
        if not all(isinstance(question, YesNoQuestion) for question in yes_no_questions):
            raise ValueError('questions in IntegrityActivity must be type "YesNoQuestion".')
        self.name = name
        self.questions = yes_no_questions
        self.intro_text = intro_text
        self.category = f'{category} '

    def run(self):
        self._print_intro_text()
        self._ask_questions()
        self._get_integrity()
        print('\n', f'Your {self.category}integrity is at {self.integrity}%!')
        self._export()
        return self.answers

    def _get_integrity(self):
        integrity_piece = 100 / len(self.questions)
        integrity = 0
        for answer in self.answers:
            if answer.casefold() in YES_ANSWERS:
                integrity += integrity_piece
        self.integrity = round(integrity, 1)
        return self.integrity

    def _export(self):
        if not self.answers:
            raise AttributeError('Cannot export Activity without answer data.')
        file_path = STORAGE_DIRECTORY / f'{self.name}.csv'
        columns = ['DateTime', 'Integrity'] + self.columns
        data = [[str(datetime.now()), self.integrity] + self.answers]
        df = pd.DataFrame(data=data, columns=columns)
        if file_path.exists():
            previous_df = pd.read_csv(file_path)
            df = previous_df.append(df)
        df.to_csv(file_path, index=False)


class SuperActivity(Activity):

    def __init__(self, name: str, activities: list, intro_text: str = ''):
        self.name = str(name)
        if not activities:
            raise ValueError('Argument "activities" list cannot be empty.')
        self.activities = list(activities)
        self.columns = [column for activity in self.activities for column in activity.columns]
        self.intro_text = str(intro_text)

    def run(self) -> list:
        self._print_intro_text()
        self._run_activities()
        self._export()
        return self.answers

    def _run_activities(self) -> list:
        self.answers = []
        for activity in self.activities:
            activity_answers = activity.run()
            self.answers += activity_answers
        return self.answers
