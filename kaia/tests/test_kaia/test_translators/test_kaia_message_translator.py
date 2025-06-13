import pandas as pd
from kaia.kaia import Message
from eaglesong import Listen, Scenario, Automaton, IAsserter
from unittest import TestCase
from kaia.kaia.translators import KaiaMessageTranslator
from avatar import AvatarApi, AvatarSettings
from avatar import WorldFields
from eaglesong.templates import Template


class FakeGuiApi:
    def __init__(self):
        self.buffer = []

    def add_message(self, item):
        self.buffer.append(item)

def echo():
    while True:
        input = yield
        print(f'>> {input}')
        yield input
        yield Listen()

class Adder(IAsserter):
    def __init__(self, api: FakeGuiApi):
        self.api = api
    def assertion(self, actual, test_case: TestCase):
        test_case.assertIsInstance(actual, Message)
        self.api.add_message(actual)

class KaiaMessageTranslatorTestCase(TestCase):
    def test_kaia_message_translator(self):
        with AvatarApi.Test(AvatarSettings()) as api:
            fake_kaia_api = FakeGuiApi()
            adder = Adder(fake_kaia_api)
            skill = KaiaMessageTranslator(echo, fake_kaia_api, api, lambda z:z+'.png')
            template = Template("Test template")
            S = Scenario(lambda: Automaton(skill, None))
            (
                S
                .send(template())
                .check(adder)
                .act(lambda: api.state_change({WorldFields.character:'character_1'}))
                .send("Test string")
                .check(adder)
                .act(lambda: api.state_change({WorldFields.user:'user'}))
                .send("Test2")
                .check(adder)
                .validate()
            )
            df = pd.DataFrame([z.__dict__ for z in fake_kaia_api.buffer])
            self.assertListEqual([None, 'character_0', None, 'character_1', 'user', 'character_1'], list(df.sender))
            self.assertListEqual([None, 'character_0.png', None, 'character_1.png','user.png','character_1.png'], list(df.avatar))


