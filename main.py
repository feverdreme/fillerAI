from multiprocessing.spawn import freeze_support
from src.Board import Board, FillOptions
from src.Bot import Bot
import colorama
from src.Game import Game
from src.color import Color
from src.fitness import NaivePlayerScore, SmartPlayerFallen
from src.turn import Turn

colorama.init()

# b = Board(fill_type=FillOptions.FILE, filename="example.txt")
# h = NaivePlayerScore()
# print(h.calculate(b))
# print(str(b))
# exit()
# prev op move
# opmove = Color[str(input())]
# b = Board(fill_type=FillOptions.FILE, filename="example.txt")
# h = NaivePlayerScore()
# bot = Bot(b, h, useDP = True)
# simulated = bot.simulate_move(b, opmove, Turn.P2)
# simulated.dump_file("example.txt", pretty = False)

# # my move
# b = Board(fill_type=FillOptions.FILE, filename="example.txt")
# h = NaivePlayerScore()
# bot = Bot(b, h, useDP = True)
# res = bot.search(7)
# print(res)
# simulated = bot.simulate_move(b, res, Turn.P1)
# simulated.dump_file("example.txt", pretty = False)
# # for i in range(1, 15):
# #     bot.search(i)

b = Board(fill_type=FillOptions.FILE, filename="gianna.txt")
game = Game(b, NaivePlayerScore, useDP = True)
game.shell()
# game.read_board_states('log.txt')