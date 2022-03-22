from __future__ import annotations

import copy
from enum import Enum, auto
from queue import Queue
from random import choice
from typing import Callable, Literal

from colorama import Back, Style

from src.color import COLORS, Color, aliases
from src.turn import Turn

SQUARE = "  "

ColorArray = list[list[Color]]
ColorTuple = tuple[tuple[Color]]

class FillOptions(Enum):
    RANDOM = auto()
    FILE = auto()
    STR = auto()

class Board:
    def __init__(self, shape: tuple[int, int] = (7, 8), fill_type: FillOptions = FillOptions.RANDOM, **kwargs):
        self.rows, self.cols = shape
        self.access: Callable[[int, int], Color] = self.default_access
        self.setv: Callable[[int, int, Color], None] = self.default_setv
        self.board = Board.get_shape_template(shape)

        if fill_type == FillOptions.RANDOM:
            self.random_floodfill
        
        elif fill_type == FillOptions.FILE:
            self.read_file(kwargs['filename'])
        
        elif fill_type == FillOptions.STR:
            with open('/tmp/boardstr', 'w+') as f:
                f.write(kwargs['data'])
            
            self.read_file('/tmp/boardstr')
    
    def is_finished(self):
        rawscores = Board.player_score(self)
        bcopy = self.copy()
        bcopy.flip()
        rawscores += Board.player_score(bcopy)

        return rawscores == self.rows * self.cols

    def flip(self):
        self.access = (
            self.flipped_access
            if self.access == self.default_access
            else self.default_access
        )
        self.setv = (
            self.flipped_setv
            if self.setv == self.default_setv
            else self.default_setv
        )

    def default_access(self, i: int, j: int) -> Color:
        return self.board[i][j]

    def flipped_access(self, i: int, j: int) -> Color:
        return self.board[self.rows - i - 1][self.cols - j - 1]

    def default_setv(self, i: int, j: int, value: Color):
        self.board[i][j] = value

    def flipped_setv(self, i: int, j: int, value: Color):
        self.board[self.rows - i - 1][self.cols - j - 1] = value

    def players(self) -> set[Color]:
        return set([self.access(0, 0), self.flipped_access(0, 0)])

    def possible_moves(self) -> set[Color]:
        return COLORS.difference(self.players())

    def copy(self) -> Board:
        copy_board = Board((self.rows, self.cols))
        copy_board.board = copy.deepcopy(self.board)

        return copy_board

    def __str__(self):
        out = []
        for i in self.board:
            s = ""
            for j in i:
                j = str(j).lstrip("Color.")
                if j == "PURPLE":
                    j = "MAGENTA"
                s += eval(f"Back.{j}") + SQUARE + Style.RESET_ALL
            out.append(s + "\n")
        return "".join(out[::-1])[:-1]

    def __repr__(self):
        out = []
        for i in self.board:
            s = ""
            for j in i:
                s += str(j).lstrip("Color.") + "\t"
            out.append(s + "\n")
        return "".join(out[::-1])[:-1]

    @staticmethod
    def get_shape_template(shape: tuple[int, int]) -> ColorArray:
        rows, cols = shape
        return [[Color.BLACK for _ in range(cols)] for _ in range(rows)]

    def random_floodfill(self):
        q: Queue = Queue()
        q.put((0, 0))
        while not q.empty():
            c_i, c_j = q.get()
            p_i, p_j = c_i - 1, c_j - 1
            n_i, n_j = c_i + 1, c_j + 1

            adj = set()
            if p_i >= 0:
                adj.add(self.access(p_i, c_j))
            if p_j >= 0:
                adj.add(self.access(c_i, p_j))

            choices = COLORS.difference(adj)
            self.setv(c_i, c_j, choice(list(choices)))

            if n_j < self.cols:
                q.put((c_i, n_j))

            if c_j == 0 and n_i < self.rows:
                q.put((n_i, c_j))

    def read_file(self, filename: str):
        with open(filename, "r") as f:
            contents = f.read()
        
        split_char = ''
        if ' ' in contents:
            split_char = ' '
        if '\t' in contents:
            if split_char != '':
                raise Exception("Error: more than one type of whitespace in file")
            
            split_char = '\t'

        lines = [
            list(filter(lambda x: not x.isspace() and x != '', line.split(split_char)))
            for line in contents.split("\n")
        ][::-1]
        new_board = Board.get_shape_template((self.rows, self.cols))

        if len(lines) != self.rows or len(lines[0]) != self.cols:
            raise Exception(
                "File read error: board dimensions do not fit size.\nSaw %d rows, expected %d.\nSaw %d cols, expected %d" % (
                    len(lines),
                    self.rows,
                    len(lines[0]),
                    self.cols
                )
            )

        for r, i in enumerate(lines):
            for c, j in enumerate(i):
                s = j.upper()
                if s in aliases:
                    s = aliases[s]
                new_board[r][c] = Color[s]

        self.board = new_board
    
    def dump_file(self, filename: str, pretty: bool = False):
        with open(filename, 'w+') as f:
            if pretty:
                f.write(str(self))
            
            else:
                f.write(repr(self))
    
    def to_tuple(self) -> ColorTuple:
        return tuple(tuple(row) for row in self.board) # type: ignore

    @staticmethod
    def player_score(oriented_board: Board) -> int:
        q: Queue = Queue()
        seen: set[tuple[int, int]] = set()
        q.put((0, 0))

        p_color = oriented_board.access(0, 0)
        p_score = 0

        while not q.empty():
            c_i, c_j = q.get()
            n_i, n_j = c_i + 1, c_j + 1
            
            if (c_i, c_j) in seen:
                continue

            if oriented_board.access(c_i, c_j) is p_color:
                p_score += 1
                seen.add((c_i, c_j))
            else:
                continue

            if n_j < oriented_board.cols:
                q.put((c_i, n_j))
            
            if n_i < oriented_board.rows:
                q.put((n_i, c_j))

        return p_score