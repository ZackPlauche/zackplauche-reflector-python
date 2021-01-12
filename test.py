from reflector.answer import answer_question

answer = answer_question(
    'What?',
    'inline',
    yesno=True
)

print(answer)