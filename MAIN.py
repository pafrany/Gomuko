# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:37:39 2019

@author: KemyPeti
"""
import sys
import os

import General_Class as GC

sys.path
sys.path.append(os.getcwd() + '\\AI\\')

import MCTS
import optimizer
import TensorFlow_net

#%%
Party = GC.GameParty(9)# 5 in row
Party.start_game()
#%%
#még nem fog futni
AI_trainer = optimizer.train(Network_fn = TensorFlow_net.NeuralNetwork,
                             init_model = ".\\model_dir\\",
                             Party = Party,
                             MCTS_PLAYER = MCTS.MCTSPlayer,
                             learning_rate = 0.001,
                             learning_rate_adjust = 1,
                             batch_size = 512,
                             game_batch_num = 1024,
                             n_playout = 256)

#%%