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
#import TensorFlow_net

#%%
Party = GC.GameParty(9)# 5 in row
Party.start_game()
#%%
