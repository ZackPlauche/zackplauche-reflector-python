from config.answer import answer_question, answer_questions, answer_question_dict
from config.export import export_to_csv


question_dict = {
    'How was your day on a scale from one to 10?': {'answer_type': 'list', 'cap': 'auto'}
}
answer = answer_question_dict(question_dict)

export_to_csv(answer, list(question_dict.keys()), 'test', overwrite=True)
