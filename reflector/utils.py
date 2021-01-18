from reflector.answer import validate_choice


def get_and_print_integrity_status(yesno_questions: list, yesno_answers: list, topic: str):
    integrity_status = get_integrity_status(yesno_questions, yesno_answers)
    print(f'\nYour {topic} is at {integrity_status}.\n')
    return integrity_status


def get_integrity_status(yesno_questions: list, yesno_answers: list):
    integrity_slice = 100 / len(yesno_questions)
    integrity: int = sum([integrity_slice for answer in yesno_answers if answer in {'y', 'yes'}]).__int__()
    integrity_status = f'{integrity}%'
    return integrity_status


def add_frequency_to_question(question: str, frequency: str) -> str:
    frequency_dict = {
        'daily': 'the day',
        'weekly': 'the week',
        'monthly': 'the month',
        'yearly': 'the year',
        'tomrrow': 'tomrrow',
    }
    validate_choice(frequency, list(frequency_dict.keys()))
    frequency = frequency_dict.get(frequency)
    updated_question = f'{question[:-1]} for {frequency}?'
    return updated_question
