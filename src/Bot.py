from typing import Callable, Type, TypeVar
from src.Board import Board, ColorTuple
from src.color import COLORS, Color
from queue import Queue
from src.fitness import Heuristic
from src.turn import Turn

from multiprocessing import Pool

class Bot:
    def __init__(self, initial_board_state: Board, heuristic, useDP: bool = False):
        self.initial_board_state = initial_board_state
        self.heuristic = heuristic

        if useDP:
            self.DPEngine = BotEngineDP()
            self.engine = self.DPEngine.useEngineDP(self.engine) # type: ignore

    def simulate_move(self, board_state: Board, move: Color, turn: Turn) -> Board:
        if turn is Turn.P2:
            board_state.flip()

        p_color = board_state.access(0, 0)

        q: Queue = Queue()
        q.put((0, 0))

        while not q.empty():
            c_i, c_j = q.get()
            n_i, n_j = c_i + 1, c_j + 1

            if board_state.access(c_i, c_j) == p_color:
                board_state.setv(c_i, c_j, move)

            else:
                continue

            if n_j < board_state.cols:
                q.put((c_i, n_j))

            if c_j == 0 and n_i < board_state.rows:
                q.put((n_i, c_j))

        if turn is Turn.P2:
            board_state.flip()

        return board_state

    # def minmax(self, scores: list[int], turn: Turn) -> int:
    #     if turn is Turn.P1:
    #         return max(scores)

    #     else:
    #         return min(scores)

    # returns the max score you can get from some board state
    def engine(self, board_state: Board, depth: int, turn: Turn) -> int:
        # terminal case
        if depth == 0 or board_state.is_finished():
            return self.heuristic.calculate(board_state, turn)

        # inducted case
        scores = []
        for move in board_state.possible_moves():
            scores.append(
                self.engine(
                    board_state=self.simulate_move(board_state.copy(), move, turn),
                    depth=depth - 1,
                    turn=Turn(-turn.value),
                )
            )

        return max(scores)

    def best_move(self, outcomes: dict[Color, int]) -> Color:
        return max(outcomes, key=lambda move: outcomes[move])

    # main function that evaluates the next moves
    def search(self, depth: int, return_outcomes: bool = False) -> Color | tuple[Color, dict[Color, int]]:
        outcomes = dict()
        for move in self.initial_board_state.possible_moves():
            outcomes[move] = self.engine(
                board_state = self.simulate_move(
                    self.initial_board_state.copy(), move, Turn.P1
                ),
                depth = depth,
                turn = Turn.P2,
            )

        if return_outcomes:
            return (self.best_move(outcomes), outcomes)
        
        else:
            return self.best_move(outcomes)
    
    def mp_search(self, depth: int) -> Color:
        # T = TypeVar('T')
        # def mypyengine(t: Type[T]) -> Callable[[T], T]:
        #     return self.engine

        possible_moves = self.initial_board_state.possible_moves()

        with Pool(len(possible_moves)) as p:
            args = list(map(
                lambda move: (
                    self.simulate_move(self.initial_board_state.copy(), move, Turn.P1), 
                    depth, 
                    Turn.P2
                ), possible_moves
            ))
            # FIXME: mypy typing generics see https://stackoverflow.com/a/68147205/14000710
            outcomes: dict[Color, int] = dict(zip(possible_moves, p.map(self.engine, args))) # type: ignore
        
        # print(outcomes)

        return self.best_move(outcomes)

#############################################################################

EngineType = Callable[[Board, int, Turn], int]

class BotEngineDP:
    """
    This is meant to preserve computational time
    
    Stores a DP dict of hashed tuple of board to a struct of depth, score.
    When accessing, if the asked depth is <= historical depth, then returns value
    If depth is > hisorical depth, then recalcuate all over again
    """
    def __init__(self):
        self.dp_dict: dict[ColorTuple, tuple[int, int]] = {}
        self.EngineType: Type = Callable[[Bot, Board, int, Turn], int]

    # decorator
    def useEngineDP(self, inner: EngineType) -> EngineType:
        def wrapper(board_state: Board, depth: int, turn: Turn) -> int:
            if board_state.to_tuple() in self.dp_dict:
                dp_depth, dp_score = self.dp_dict[board_state.to_tuple()]

                if depth > dp_depth:
                    res_score = inner(board_state, depth, turn)
                    self.dp_dict[board_state.to_tuple()] = (depth, res_score)
                    return res_score

                else:
                    return dp_score

            else:
                res_score = inner(board_state, depth, turn)
                self.dp_dict[board_state.to_tuple()] = (depth, res_score)
                return res_score
        
        return wrapper