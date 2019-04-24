import game
from mcts_alphaZero_play import MCTSPlayer
from policy_value_net_play import PolicyValueNetPlay
from random import randint
import utils.game_utils as GU
import pickle
import numpy as np
import tensorflow as tf
bsize = 15#game.BOARD_SIZE


class BState():
    def __init__(self):
        self.current_player = 2
        self.availables = list(range(bsize * bsize))
        self.states = dict()
        self.n_in_row = 5
        
    def current_state(self):
        last_move = list(self.states.keys())[-1]
        current_player = len(self.states) % 2 + 1
        square_state = np.zeros((4, bsize, bsize))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == current_player]
            move_oppo = moves[players != current_player]
            square_state[0][move_curr // bsize,
                            move_curr % bsize] = 1.0
            square_state[1][move_oppo // bsize,
                            move_oppo % bsize] = 1.0
            # indicate the last move location
            square_state[2][last_move // bsize,
                            last_move % bsize] = 1.0
        if current_player == 1:
            square_state[3][:, :] = 1.0  # indicate the colour to play
        return square_state[:, ::-1, :]
    
    def has_a_winner(self):
        states = self.states
        n = self.n_in_row

        moved = list(set(range(bsize * bsize)) - set(self.availables))
        if len(moved) < self.n_in_row * 2 - 1:
            return False, -1

        for m in moved:
            h = m // bsize
            w = m % bsize
            player = states[m]

            if (w in range(bsize - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(bsize - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * bsize, bsize))) == 1):
                return True, player

            if (w in range(bsize - n + 1) and h in range(bsize - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (bsize + 1), bsize + 1))) == 1):
                return True, player

            if (w in range(n - 1, bsize) and h in range(bsize - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (bsize - 1), bsize - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):
            return True, -1
        return False, -1
    

class AI:
    def __init__(self):
        
        self.BoardState = BState()
        
        self.model_file = './AI_model/9_9_5_best_policy.model.meta'
        
        sess=tf.Session()    
        #First let's load meta graph and restore weights
        saver = tf.train.import_meta_graph(self.model_file)
        saver.restore(sess,tf.train.latest_checkpoint('./AI_model/'))
        graph = tf.get_default_graph()
        
        variables = [n.name for n in tf.get_default_graph().as_graph_def().node if "Variable" in n.op]
        self.policy_param = []
        for idx in range(16):
            self.policy_param.append(graph.get_tensor_by_name(variables[idx] + ':0').eval(session=sess))

        self.best_policy = PolicyValueNetPlay(bsize,
                                              bsize,
                                              self.policy_param)
        self.mcts_player = MCTSPlayer(self.best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)
        
    def move_to_location(self, move):
    	return GU.position.IDX_to_position(height=bsize, width=bsize, IDX=move)

    def location_to_move(self, location):
        return GU.position.position_to_IDX(height=bsize, width=bsize, position=location)
	
    def get_AI_move(self, states):
        
        move = self.mcts_player.set_action(self.BoardState, bsize)
        return self.move_to_location(move)

    def capture_location(self, location, player):
        IDX = self.location_to_move(location)
        self.BoardState.availables.remove(IDX)
        self.BoardState.states[IDX] = player

    def free_location(self, location): #undo esetére
        IDX = self.location_to_move(location)
        self.BoardState.availables.append(IDX)
        self.BoardState.availables=sorted(self.availables)
        self.BoardState.states.pop(IDX);


