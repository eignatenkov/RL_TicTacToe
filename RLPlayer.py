from tictactoe import TicTacToe
from position_generator import generate_positions
import random
import numpy as np


class RLPlayer:
    def __init__(self, who=1, exploration_rate=0.1):
        self.who = who
        self.exploration_rate = exploration_rate
        all_positions = generate_positions()
        # we only need positions after our turn and losing ones. And maybe the starting one, just for completeness
        self.probs = {'.........': 0.5}
        for position in all_positions:
            key = position.tostring()
            if position.who_won() == self.who:
                self.probs[key] = 1
            elif position.who_won() is not None:
                self.probs[key] = 0
            elif ((position.board != 0).sum() % 2 == 1 and self.who == 1) or ((position.board != 0).sum() % 2 == 0 and self.who == -1):
                self.probs[key] = 0.5
        self.last = '.........'
        self.is_last_explorational = False
        return

    def update_last_prob(self, new_prob, learning_rate):
        self.probs[self.last] += learning_rate * (new_prob - self.probs[self.last])

    def make_turn(self, state: TicTacToe, learning_rate=0.1, log=False):
        options = state.make_all_next_moves()
        explore = random.random() < self.exploration_rate
        if explore:
            if log:
                print("exploration move")
            next_move = random.choice(options)
            self.is_last_explorational = True
        else:
            max_prob = max(self.probs[x.tostring()] for x in options)
            max_options = [x for x in options if self.probs[x.tostring()] == max_prob]
            next_move = random.choice(max_options)
            # next_move = max(options, key=lambda x: self.probs[x.tostring()])
            # if log:
                # print(f"updating prob {self.last} from {self.probs[self.last]}")
            self.update_last_prob(self.probs[next_move.tostring()], learning_rate)
            # if log:
            #     print(f"to {self.probs[self.last]}")
            self.is_last_explorational = False
        self.last = next_move.tostring()
        return next_move


def play_game(cross: RLPlayer, naught: RLPlayer, learning_rate=0.1, log=False):
    nb = TicTacToe()
    cross.last = '.........'
    naught.last = '.........'
    cross_turn = True
    next_moves = nb.make_all_next_moves()
    while len(next_moves) > 0:
        if cross_turn:
            nb = cross.make_turn(nb, learning_rate=learning_rate, log=log)
            cross_turn = False
        else:
            nb = naught.make_turn(nb, learning_rate=learning_rate, log=log)
            cross_turn = True
        if log:
            nb.print()
        next_moves = nb.make_all_next_moves()
    if nb.who_won() == -1 and not cross.is_last_explorational:
        if log:
            print(f"updating cross prob {cross.last}")
            print(f"from {cross.probs[cross.last]}")
        cross.update_last_prob(0, learning_rate)
        if log:
            print(f"to {cross.probs[cross.last]}")
    elif nb.who_won() == 1 and not naught.is_last_explorational:
        if log:
            print(f"updating naught prob {naught.last}")
            print(f"from {naught.probs[naught.last]}")
        naught.update_last_prob(0, learning_rate)
        if log:
            print(f"to {naught.probs[naught.last]}")
    else:
        if not cross.is_last_explorational:
            cross.update_last_prob(0.5, learning_rate)
        if not naught.is_last_explorational:
            naught.update_last_prob(0.5, learning_rate)


if __name__ == "__main__":
    cross = RLPlayer(1)
    naught = RLPlayer(-1)
    for i in range(20000):
        play_game(cross, naught, log=False, learning_rate=0.1)

    test_state = TicTacToe(np.array([[1,0,0], [0,0,1], [-1,-1,0]]))
    # test_state = TicTacToe()
    next_states = test_state.make_all_next_moves()
    for sss in next_states:
        print(sss.tostring(), cross.probs[sss.tostring()])
    # print(cross.probs['X..XX.OO.'])
    # print(naught.probs['X...O....'])
    play_game(cross, naught, log=True)
