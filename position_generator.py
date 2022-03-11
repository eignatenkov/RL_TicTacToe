from tictactoe import TicTacToe


def generate_positions():
    all_boards = set()
    current_boards = {TicTacToe()}
    while current_boards:
        new_boards = set()
        for cb in current_boards:
            new_boards |= set(cb.make_all_next_moves())
        all_boards |= current_boards
        current_boards = new_boards
    return all_boards
