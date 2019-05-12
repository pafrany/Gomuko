# -*- coding: utf-8 -*-
"""
@author: KemyPeti
"""

from __future__ import print_function
import sys
import pickle
from game import Board, Game
sys.path.append('.\\TRAIN\\')
from mcts_alphaZero import MCTSPlayer
from policy_value_net_play import PolicyValueNetPlay


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move
    
    def set_action(self, board, location):
        try:
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run(width = 8,
        height = 8,
        num_in_row = 5,
        model_file = 'best_policy_8_8_5.model'):
    
    try:
        board = Board(n_in_row=num_in_row)
        
        game = Game(board)
        
        policy_param = pickle.load(open(model_file, 'rb'),
                                   encoding='bytes')
        
        best_policy = PolicyValueNetPlay(width, height, policy_param)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)

        # set start_player=0 for human first
        game.start_play(Human(), mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run(width = 8,
        height = 8,
        num_in_row = 5,
        model_file = 'best_policy_8_8_5.model')
