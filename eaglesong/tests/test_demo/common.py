from eaglesong.core import *
from eaglesong.drivers.telegram.primitives import *
from unittest import TestCase
import pandas as pd


def S(bot, proc = None) -> Scenario:
    bot.processor = proc
    return Scenario(lambda: bot.create_generic_automaton(BotContext(123)))


