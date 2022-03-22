from typing import Type
from src.Board import Board, FillOptions
from src.color import Color
from src.fitness import Heuristic
from src.Bot import Bot
from src.turn import Turn

class Game:
    def __init__(self, initial_board_state: Board, heuristic: Type[Heuristic], useDP: bool = False):
        heur = heuristic()
        self.bot = Bot(initial_board_state, heur, useDP)
        self.initial_board_state = initial_board_state
        self.current_board_state = initial_board_state
        self.move_history: list[Color] = list()
        self.current_move = Turn.P1

        self.move_logfile: str | None = None
        self.engine_logfile: str | None = None
    
    def useDebug(self, move_logfile: str = None, engine_logfile: str = None):
        self.move_logfile = move_logfile
        self.engine_logfile = engine_logfile
    
    def send_logfile(self, filename: str, data: str):
        f = open(filename, 'a+')
        f.write(data + '\n')
        f.close()
        
    def _make_move(self, move: Color, turn: Turn = None):
        if turn is None:
            turn = self.current_move
        
        new_board_state = self.bot.simulate_move(self.current_board_state, move, turn)
        self.move_history.append(move)
        self.current_move = Turn(-turn.value)

        if self.move_logfile:
            self.send_logfile(self.move_logfile, str(move))
    
    # def play_move(self, depth: int = 7):
    #     res, outcomes = self.bot.search(depth, return_outcomes = True)

    #     if self.move_logfile:
    #         self.send_logfile(self.move_logfile, res)
        
    #     if self.engine_logfile:
    #         self.send_logfile(self.engine_logfile, repr(outcomes))
    
    def dump_board_states(self, filename: str):
        with open(filename, 'a+') as f:
            turn = Turn.P1
            curr_board = self.initial_board_state.copy()

            for move in self.move_history:
                new_board_state = self.bot.simulate_move(curr_board, move, turn)
                f.write(repr(new_board_state) + '\n')
    
    def read_board_states(self, filename: str):
        with open(filename, 'r') as f:
            contents = list(filter(lambda x: x != '', f.readlines()))
        
        boards: list[str] = [''.join(contents[i * 8: i * 8 + 8]).rstrip('\n') for i in range(len(contents) // 8)]
        
        for board in boards:
            # print(repr(board))
            print(str(Board(fill_type = FillOptions.STR, data = board)), '\n')

    def shell(self):
        while True:
            uinput = input('> ').rstrip()
            output: str = ''

            if uinput == 'exit':
                break
            
            elif uinput.startswith('move'):
                if uinput == 'move?':
                    output = repr(self.current_move)
                
                else:
                    _, player, move = uinput.split(' ')
                    player = Turn[player.upper()]
                    move = Color[move.upper()]

                    self._make_move(move, player)
            
            elif uinput.startswith('search'):
                if uinput == 'search':
                    output = self.bot.search(depth = 7)
                
                else:
                    _, depth = uinput.split(' ')
                    output = self.bot.search(depth = int(depth))
            
            elif uinput.startswith('outcomes'):
                uinput = uinput[len('outcomes '): ]

                if uinput == 'search':
                    res, outcomes = self.bot.search(depth = 7, return_outcomes = True)
                    output = f'{res}\n{repr(outcomes)}'
                
                else:
                    _, depth = uinput.split(' ')
                    res, outcomes = self.bot.search(depth = int(depth), return_outcomes = True)
                    output = f'{res}\n{repr(outcomes)}'
            
            elif uinput == 'show':
                output = str(self.current_board_state)
            
            elif uinput.startswith('dump'):
                _, filename = uinput.split(' ')
                with open(filename, 'w+') as f:
                    f.write(repr(self.current_board_state))
            
            else:
                output = 'Invalid input'
        
            print(output)