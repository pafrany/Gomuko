# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:55:37 2019

@author: KemyPeti
"""

import numpy as np
import tensorflow as tf

class NeuralNetwork():
    def __init__(self, board_size, model_file=None):
        self.board_size = board_size    #list
        self.regularization_parameter = 0.0001
        self.learning_rate = 0.0001
    
        #placeholders for input data
        self.input = tf.placeholder(dtype = tf.float32,
                                    shape=[None,
                                           self.board_size[0],
                                           self.board_size[1],
                                           4],
                                    name = "Layer_0_INPUT")
        
        self.labels = tf.placeholder(dtype = tf.float32,
                                     shape=[None,
                                            1],
                                     name = "Layer_0_labels") #containing if the game wins or not for each state
        
        self.mcts_probs = tf.placeholder(dtype = tf.float32,
                                         shape=[None,
                                                self.board_size[0],
                                                self.board_size[1]],
                                         name = "Layer_0_AIPlayerProbs")
        
        
        with tf.variable_scope("Common_CONV_Layers", reuse=tf.AUTO_REUSE):
            self.conv1 = tf.layers.conv2d(inputs=self.input,
                                          filters=32,
                                          kernel_size=[3, 3],
                                          padding="same",
                                          activation=tf.nn.leaky_relu,
                                          name = "Layer_1_Convolution")
            self.conv2 = tf.layers.conv2d(inputs=self.conv1,
                                          filters=64,
                                          kernel_size=[3, 3],
                                          padding="same",
                                          activation=tf.nn.leaky_relu,
                                          name = "Layer_2_Convolution")
            self.conv3 = tf.layers.conv2d(inputs=self.conv2,
                                          filters=128,
                                          kernel_size=[3, 3],
                                          padding="same",
                                          activation=tf.nn.leaky_relu,
                                          name = "Layer_3_Convolution")
            
        with tf.variable_scope("Action_Layers", reuse=tf.AUTO_REUSE):
            self.action_conv1 = tf.layers.conv2d(inputs=self.conv3,
                                                filters=4,
                                                kernel_size=[1, 1],
                                                padding="same",
                                                activation=tf.nn.leaky_relu,
                                                name = "Layer_4_Action_Convolution")
            self.action_conv2 = tf.layers.conv2d(inputs=self.action_conv1,
                                                filters=1,
                                                kernel_size=[1, 1],
                                                padding="same",
                                                activation=tf.nn.log_softmax,
                                                name = "Layer_5_Action_Convolution") #log probability of moves
            
        with tf.variable_scope("Eval_Layers", reuse=tf.AUTO_REUSE):
            self.eval_conv = tf.layers.conv2d(inputs=self.conv3,
                                                filters=2,
                                                kernel_size=[1, 1],
                                                padding="same",
                                                activation=tf.nn.leaky_relu,
                                                name = "Layer_4_Eval_Convolution")
            self.eval_flatten = tf.flatten(inputs = self.eval_conv,
                                             name = "Layer_5_Eval_Flatten")
            self.eval_dense1 = tf.layers.dense(inputs=self.eval_flatten,
                                               units=self.board_size[0]*self.board_size[1],
                                               activation=tf.nn.leaky_relu,
                                               name = "Layer_6_Eval_Dense")
            self.eval_dense2 = tf.layers.dense(inputs=self.eval_dense1,
                                               units=1,
                                               activation=tf.nn.tanh,
                                               name = "Layer_7_Eval_Dense") #the evaluation score of each state
            
        with tf.name_scope("Losses"):
            self.eval_loss = tf.losses.mean_squared_error(self.labels,
                                                          self.eval_dense2)
            self.action_loss = tf.negative(tf.reduce_mean(tf.reduce_sum(tf.math.multiply(self.mcts_probs,
                                                                                         self.action_conv2)))) #policy loss
            self.l2_regularization = self.regularization_parameter * tf.add_n([tf.nn.l2_loss(ts) for ts in
                                                                               tf.trainable_variables()])
            
            self.loss = self.eval_loss + self.action_loss + self.l2_regularization
            
            
        with tf.name_scope("Optimization"):
            self.optimizer = tf.train.AdamOptimizer(
                    learning_rate=self.learning_rate).minimize(self.loss)
    
        self.__init_variables()
        
        self.saver = tf.train.Saver()
        if model_file is not None:
            self.restore_model(model_file)
            
    def __init_variables(self):
        self.session = tf.Session()
        init = tf.global_variables_initializer()
        self.session.run(init)

    def save_model(self, model_path):
        self.saver.save(self.session, model_path)

    def restore_model(self, model_path):
        self.saver.restore(self.session, model_path)
        
        
    '''
    def policy_value_fn(self, Party):
        """
        input: board
        output: a list of (action, probability) tuples for each available
        action and the score of the board state
        """
        legal_positions = Party.possible_steps
        current_state = np.ascontiguousarray(board.current_state().reshape(
                -1, 4, self.board_width, self.board_height))
        act_probs, value = self.policy_value(current_state)
        act_probs = zip(legal_positions, act_probs[0][legal_positions])
        return act_probs, value
    '''