from reflector.activities import Activity, SuperActivity
from reflector.questions import ListQuestion, InlineQuestion, TextQuestion, YesNoQuestion, OrderedListQuestion

reflect = TextQuestion('Take some time to reflect on your day.', name='Reflection')
gratitude = OrderedListQuestion('What are you grateful for?')

morning_reflection = Activity('Morning Reflection', [
    gratitude,
    reflect,
], intro_text='Good morning handsome ;)')
gratitude_list = Activity('Gratitude List', [gratitude])