from eaglesong.tests.test_demo.common import *
from eaglesong.demo.example_02_questionnaire import bot


class Demo0TestCase(TestCase):
    def test_questionnairs_1(self):
        (
            S(bot)
            .send('/start')
            .check('What is your name?')
            .send('A')
            .check('Where are you from, A?')
            .send('B')
            .check(lambda z: z.startswith('Nice to meet you, A from B! By the way'), Return)
            .validate()
        )







