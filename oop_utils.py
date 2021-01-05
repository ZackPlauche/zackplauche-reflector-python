class Question:
    answers = []

    def __init__(self, question: str = None, question_type: str = "oneoff"):
        if question and type(question) != str:
            raise TypeError('"question" argument must be a string.')
        self.question = question
        self.question_type = question_type

    def _question_validator(func):
        def wrapper(self):
            if type(self.question) != str:
                raise TypeError('The set question needs to be a string')
            func(self)
        return wrapper

    @_question_validator
    def listed_answer(self, question=None, ordered=False):

        if not question:
            question = self.question

        # Define list style
        if ordered:
            counter = 1
            list_style = f'{counter}. '
        else:
            list_style = '• '

        # Ask question
        print(question)
        while True:
            answer = input(list_style)
            if answer == '':
                print()
                break
            self.answers.append(answer)
            if ordered: 
                counter += 1
            
    def list_answers(self):
        for i, answer in enumerate(self.answers):
            print(f'{i + 1}. {answer}')


def main():
    favorite_shows = Question('What are your favorite shows?')
    favorite_shows.listed_answer()
    favorite_shows.list_answers()


if __name__ == '__main__':
    main()
    
