import random
from src.Board import Board
from queue import Queue

from src.turn import Turn

# INTERFACE ONLY
class Heuristic():
    def __init__(self):
        pass

    def calculate(self, board_state: Board, turn: Turn) -> int:
        ...

class NaivePlayerScore(Heuristic):
    def calculate(self, board_state: Board, turn) -> int:
        ret = Board.player_score(board_state) 
        board_state.flip()

        ret -= Board.player_score(board_state)

        return ret

class SmartPlayerFallen(Heuristic):
    @staticmethod
    def get_player_area(board_state: Board, flip: bool = False) -> set[tuple[int, int]]:
        q: Queue = Queue()
        p_set: set[tuple[int, int]] = set()
        seen: set[tuple[int, int]] = set()
        q.put((0, 0))
        p_set.add((0, 0))

        p_color = board_state.access(0, 0)

        while not q.empty():
            curr = c_i, c_j = q.get()
            n_i, n_j = c_i + 1, c_j + 1
            
            if curr in seen:
                continue

            if board_state.access(*curr) is p_color:
                p_set.add(curr)
                seen.add(curr)
            else:
                continue

            if n_j < board_state.cols:
                q.put((c_i, n_j))
            
            if n_i < board_state.rows:
                q.put((n_i, c_j))

        return p_set

    def calculate(self, board_state: Board, turn: Turn) -> int:
        not_seen: set[tuple[int, int]] = set()
        p1_area: set[tuple[int, int]] = set()
        p2_area: set[tuple[int, int]] = set()
        areas: list[tuple[bool, bool, int]] = list()

        for i in range(board_state.rows):
            for j in range(board_state.cols):
                not_seen.add((i, j))
    
        p1_area = SmartPlayerFallen.get_player_area(board_state)
        board_state.flip()
        p2_area = SmartPlayerFallen.get_player_area(board_state)
        board_state.flip()

        not_seen = not_seen.difference(p1_area, p2_area)

        while len(not_seen) != 0:
            info: list[bool | int] = [False, False, 0]
            seen: set[tuple[int, int]] = set()

            q: Queue = Queue()
            elem, = random.sample(not_seen, 1)
            q.put(elem)

            while not q.empty():
                curr = c_i, c_j = q.get()
                n_i, n_j = c_i + 1, c_j + 1

                if curr in seen:
                    continue

                if curr in p1_area:
                    info[0] = True
                
                elif curr in p2_area:
                    info[1] = True
                
                else:
                    info[2] += 1
                    seen.add(curr)
                    not_seen.discard(curr)

                    if n_j < board_state.cols:
                        q.put((c_i, n_j))
            
                    if n_i < board_state.rows:
                        q.put((n_i, c_j))

            areas.append(tuple(info)) # type: ignore
        
        p1_score = len(p1_area)
        p2_score = len(p2_area)

        for chunk in areas:
            match chunk: # type: ignore
                case (True, False, _):
                    p1_score += chunk[2]
                
                case (False, True, _):
                    p2_score += chunk[2]
        
        print(p1_score, p2_score)
        
        return p1_score - p2_score