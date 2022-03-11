import numpy as np
from tictactoe import TicTacToe


def test_board_from_string():
    test_string = 'XO..XO..X'
    assert np.array_equal(TicTacToe.board_from_string(test_string), np.array([[1,-1,0], [0,1,-1], [0,0,1]]))


def test_who_won():
    board = TicTacToe(string_board='XXOXO.O..')
    assert board.who_won() == -1