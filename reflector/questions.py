import copy

YES_ANSWERS = ['y', 'yes', 'yep', 'yessir', 'yeezer', 'yerp']
NO_ANSWERS = ['n', 'no', 'nope', 'nada']


class Question:

    def __init__(self, question, name=''):
        self.question = str(question)
        self.name = str(name) if name else self.question
        self.ending = ''

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.__str__()}>'

    def ask(self):
        answer = self.ask_question()
        if self.ending:
            print(end=self.ending)
        return answer

    def ask_question(self):
        answer = input(self.question)
        return answer

    def rename(self, name):
        new_question = copy.copy(self)
        new_question.name = name
        return new_question

    def endwith(self, ending):
        self.ending = ending
        return self


class TextQuestion(Question):
    help_text = '\n(linebreaks are enabled. To finish answering, press "." on a new line and press enter)'

    def ask_question(self):
        print(self.question, self.help_text, end="\n\n")
        answer_line_list = []
        while True:
            answer_line = input()
            if answer_line == '.':
                break
            answer_line_list.append(answer_line)
        return '\n'.join(answer_line_list)


class InlineQuestion(Question):

    def __init__(self, question, valid_answers=None, display_answers='default', name=''):
        if not valid_answers:
            valid_answers = []
        elif isinstance(valid_answers, range):
            valid_answers = map(str, list(valid_answers))
        self.question = str(question)
        self.name = name if name else self.question
        self.valid_answers = list(valid_answers)
        self.display_answers = display_answers if not display_answers == 'default' else self.valid_answers
        self.ending = ''

    def ask_question(self) -> str:
        prompt = f'{self.question}: ' if not self.display_answers else f'{self.question} ({"/".join(self.display_answers)}): '
        while True:
            answer = input(prompt)
            if self.valid_answers and answer.casefold() not in self.valid_answers:
                feedback = 'Answer Invalid.'
                feedforward = f'Please choose either {", ".join(self.valid_answers[:-1])} or {self.valid_answers[-1]}.'
                print(f'\n{feedback} {feedforward}', end='\n\n')
                continue
            return answer


class YesNoQuestion(InlineQuestion):
    valid_answers = YES_ANSWERS + NO_ANSWERS
    display_answers = ['y', 'n']

    def __init__(self, question, name=''):
        self.question = str(question)
        self.name = str(name) if name else self.question


class ListQuestion(Question):

    def __init__(self,
                 question: str,
                 list_style: str = '• ',
                 name: str = ''
                 ):
        self.question = str(question)
        self.name = str(name) if name else self.question
        self.list_style = str(list_style)
        self.ending = '\n'

    def ask_question(self) -> list:
        self.answer_list = []
        print(self.question)
        answer = self._get_list_answer()
        return answer

    def _get_list_answer(self):
        while answer := input(self.list_style):
            self.answer_list.append(answer)
        return self.answer_list


class OrderedListQuestion(ListQuestion):

    def __init__(self,
                 question,
                 limit: int = 0,
                 list_style: str = '',
                 name: str = '',
                 ):
        self.question = str(question)
        self.limit = int(limit)
        self.list_style = str(list_style)
        self.name = str(name) if name else self.question
        self.ending = '\n'

    def _get_list_answer(self):
        count = 1
        while answer := input(self._build_prompt(count)):
            if not answer:
                break
            self.answer_list.append(answer)
            if self.limit and len(self.answer_list) == self.limit:
                break
            count += 1
        return self.answer_list

    def _build_prompt(self, count):
        if self.limit and self.list_style:
            return f'{self.list_style} ({count} of {self.limit}): '
        elif self.limit:
            return f'{count} of {self.limit}. '
        return f'{count}. '