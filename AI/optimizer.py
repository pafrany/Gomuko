# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:34:41 2019

@author: KemyPeti
"""

class train():
    def __init__(self,
                 Network_fn,
                 init_model, 
                 Party,
                 MCTS_PLAYER,
                 learning_rate,
                 learning_rate_adjust,
                 batch_size,
                 game_batch_num,
                 n_playout):
        '''
        Input:\n
        \n\t Network_fn: neural network function
        \n\t init_model: 1 or the data_dir for model
        \n\t Party: Party from General_Class
        \n\t learning_rate: learning_rate
        
                 
        
        '''
        # params of the board and the game
        self.board_width = Party.Table.width
        self.board_height = Party.Table.height
        self.n_in_row = Party.num_in_row
        
        #training
        self.learn_rate = learning_rate
        self.lr_multiplier = learning_rate_adjust #exponential decay?
        self.batch_size = batch_size
        self.game_batch_num = game_batch_num
        self.n_playout = n_playout  # num of simulations for each move
        
        
        #network
        if init_model == 1:
            self.NN = Network_fn(board_size = [self.board_width, self.board_height])
        else:
            self.NN = Network_fn(board_size = [self.board_width, self.board_height],
                                 model_file = init_model)
            
        #MONTE_CARLO player
        self.mcts_player = MCTS_PLAYER(self.policy_value_net.policy_value_fn,
                                       c_puct=self.c_puct,
                                       n_playout=self.n_playout,
                                       is_selfplay=1)
            
            
            
        '''
        self.board = Board(width=self.board_width,
                           height=self.board_height,
                           n_in_row=self.n_in_row)
        self.game = Game(self.board)
        
        # training params
        
        self.temp = 1.0  # the temperature param
        
        self.c_puct = 5
        self.buffer_size = 10000
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.play_batch_size = 1
        self.epochs = 5  # num of train_steps for each update
        self.kl_targ = 0.02
        self.check_freq = 50
        self.best_win_ratio = 0.0
        # num of simulations used for the pure mcts, which is used as
        # the opponent to evaluate the trained policy
        self.pure_mcts_playout_num = 1000

        '''