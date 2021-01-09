from answer import answer, answer_list
from export import export_to_csv


questions = [
    'What did you do today?',
    'What are you grateful for?',
    'What are you going to do tomorrow?',
]

one_answer = answer('Who are you?', 'inline')

export_to_csv(one_answer, ['Q'], 'test', overwrite=True)
