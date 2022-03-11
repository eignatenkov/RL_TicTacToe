import numpy as np
import random
from copy import copy


class FieldBusy(Exception):
    """Raise when the field is busy"""


class GameOver(Exception):
    """Raise when game is over, can't make next move"""


class TicTacToe:
    def __init__(self, board=np.zeros((3, 3), dtype=int), string_board=''):
        if string_board != '':
            self.board = TicTacToe.board_from_string(string_board)
        else:
            self.board = board

    @classmethod
    def board_from_string(cls, string_board):
        assert len(string_board) == 9
        board = np.zeros((3,3), dtype=int)
        for i, symb in enumerate(string_board):
            x = i // 3
            y = i % 3
            if symb in {'X', 'O'}:
                mark = 1 if symb == 'X' else -1
                board[x, y] = mark
        return board

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        return hash(self.board.tostring())

    def who_won(self):
        hor = self.board.sum(axis=0)
        if 3 in hor:
            return 1
        if -3 in hor:
            return -1
        vert = self.board.sum(axis=1)
        if 3 in vert:
            return 1
        if -3 in vert:
            return -1
        d = [self.board.diagonal().sum(), np.flipud(self.board).diagonal().sum()]
        if 3 in d:
            return 1
        if -3 in d:
            return -1
        return None

    def add_cross(self, x, y):
        if self.board[x, y] == 0:
            self.board[x, y] = 1
        else:
            raise FieldBusy

    def add_nought(self, x, y):
        if self.board[x, y] == 0:
            self.board[x, y] = -1
        else:
            raise FieldBusy

    def make_all_next_moves(self):
        """
        returns all possible next states from the given one
        :param board: np.array, current state
        :return: list of all possible next states
        """
        if self.who_won() is not None:
            return []
        x_turn = (self.board == 1).sum() == (self.board == -1).sum()
        empty_spots = np.argwhere(self.board == 0)
        if len(empty_spots) > 0:
            new_states = []
            for spot in empty_spots:
                new_board = TicTacToe(copy(self.board))
                if x_turn:
                    new_board.add_cross(*spot)
                else:
                    new_board.add_nought(*spot)
                new_states.append(new_board)
            return new_states
        else:
            return []

    def make_random_move(self):
        if self.who_won() is not None:
            raise GameOver
        x_turn = (self.board == 1).sum() == (self.board == -1).sum()
        empty_spots = np.argwhere(self.board == 0)
        new_move = random.choice(empty_spots)
        if x_turn:
            self.add_cross(*new_move)
        else:
            self.add_nought(*new_move)

    def print(self):
        for i in range(3):
            line = []
            for j in range(3):
                cell = self.board[i, j]
                if cell == 1:
                    line.append('X')
                elif cell == -1:
                    line.append('O')
                else:
                    line.append('.')
            print(''.join(line))
        print('')

    def tostring(self):
        line = ''
        for i in range(3):
            for j in range(3):
                cell = self.board[i, j]
                if cell == 1:
                    line += 'X'
                elif cell == -1:
                    line += 'O'
                else:
                    line += '.'
        return line


if __name__ == "__main__":
    game = TicTacToe()
    for i in range(5):
        game.make_random_move()
        game.print()

    for a in game.make_all_next_moves():
        a.print()
