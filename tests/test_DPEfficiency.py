import unittest
from time import time

from src.Board import Board
from src.Bot import Bot
from src.fitness import NaivePlayerScore

def timefunc(func, *args):
    start = time()
    func(*args)
    end = time()
    return end - start

def run_depth(times: int, depth: int, useDP: bool):
    for i in range(times):
        b = Board()
        b.random_floodfill()

        h = NaivePlayerScore()
        bot = Bot(b, h, useDP)

        bot.search(depth)

class TestDPEfficiency(unittest.TestCase):
    def test_5t_3d(self):
        assert timefunc(run_depth, 5, 3, True) - timefunc(run_depth, 5, 3, False) >= 0

unittest.main()