from __future__ import absolute_import, division, print_function
import sys
import os
try:
    sys.path.append(os.getcwd() + '\\utils\\')
    import game_utils as GU
except:
    import utils.game_utils as GU
import numpy as np
import tensorflow as tf


class PolicyValueNetPlay():
    
    def __init__(self, board_width, board_height, net_params):
        self.width = board_width
        self.height = board_height
        self.params = net_params

    def policy_value_fn(self, availables, current_state):
        
        AVAIL = availables
        CURSTATE = current_state
        
        X = CURSTATE.reshape(-1, 4, self.width, self.height)
        
        X = GU.math.conv2D(X = X,
                               W = self.params[0],
                               b = self.params[1])
        X = GU.math.conv2D(X = X,
                               W = self.params[2],
                               b = self.params[3])
        X = GU.math.conv2D(X = X,
                               W = self.params[4],
                               b = self.params[5])
        
        X_p = GU.math.conv2D(X = X,
                             W = self.params[6], 
                             b = self.params[7],
                             padding = 0)
        X_p = GU.math.dense(X = X_p.flatten(), 
                            W = self.params[8],
                            b = self.params[9])
        act_probs = GU.math.softmax(X_p)
        
        X_v = GU.math.conv2D(X = X,
                             W = self.params[10],
                             b = self.params[11],
                             padding = 0)
        
        X_v = GU.math.relu((GU.math.dense(X = X_v.flatten(),
                                         W = self.params[12],
                                         b = self.params[13])))
        value = np.tanh(GU.math.dense(X = X_v, 
                                      W = self.params[14],
                                      b = self.params[15]))[0]
        act_probs = zip(AVAIL, act_probs.flatten()[AVAIL])
        return act_probs, value
