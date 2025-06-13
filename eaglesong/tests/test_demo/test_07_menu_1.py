from eaglesong.tests.test_demo.common import *
from eaglesong.demo.example_07_menu_1 import bot
from eaglesong.drivers.telegram.menu import MenuItem

class Menu1TestCase(TestCase):
    def test_menu_happy_path(self):
        (
            S(bot)
            .send('/start')
            .check(Options)
            .send(SelectedOption('Where do you live?'))
            .check(Delete,Options)
            .send(SelectedOption(MenuItem.back_button_text))
            .check(Delete,Options)
            .send(SelectedOption('How old are you?'))
            .check(Delete, Options)
            .send(SelectedOption('18-30'))
            .check(Delete, 'You have selected: 18-30', Return)
            .validate()
        )

    def test_menu_close(self):
        (
            S(bot)
            .send('/start')
            .check(Options)
            .send(SelectedOption('Where do you live?'))
            .check(Delete, Options)
            .send(SelectedOption(MenuItem.close_button_text))
            .check(Delete, 'You have selected: None', Return)
            .validate()
    )

    def test_menu_wrong_input(self):
        (
            S(bot)
            .send('/start')
            .check(Options)
            .send('bla')
            .check(Delete, 'You have selected: None', Return)
            .validate()
         )