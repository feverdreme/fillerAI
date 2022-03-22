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

def run_depth(times: int, depth: int, useDP: bool, useMP = False):
    for i in range(times):
        b = Board()
        b.random_floodfill()

        h = NaivePlayerScore()
        bot = Bot(b, h, useDP)

        if useMP:
            bot.mp_search(depth)
        else:
            bot.search(depth)

class TestEfficiency(unittest.TestCase):
    def test_1t_2d(self):
        self.assertTrue(timefunc(run_depth, 1, 2, True) <= timefunc(run_depth, 1, 2, False))

    def test_1t_3d(self):
        self.assertTrue(timefunc(run_depth, 1, 3, True) < timefunc(run_depth, 1, 3, False))
    
    def test_1t_5d(self):
        self.assertTrue(timefunc(run_depth, 1, 5, True) < timefunc(run_depth, 1, 5, False))
    
    def test_3t_3d(self):
        self.assertTrue(timefunc(run_depth, 3, 3, True) < timefunc(run_depth, 3, 3, False))
    
    # ---------------------------------------------------------------------------------------------------------
    # FIXME: https://docs.python.org/dev/library/unittest.mock.html, https://stackoverflow.com/a/33129114/14000710
    # def test_1t_9d_nodp(self):
    #     self.assertTrue(timefunc(run_depth, 1, 7, False, True) <= timefunc(run_depth, 1, 7, False, False))

    # def test_1t_9d_dp(self):
    #     self.assertTrue(timefunc(run_depth, 1, 7, True, True) <= timefunc(run_depth, 1, 7, True, False))
    

unittest.main()