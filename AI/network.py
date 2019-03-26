# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:37:57 2019

@author: KemyPeti
"""
import tensorflow as tf
import numpy as np

def __init_variables__():
    session = tf.Session()
    init = tf.global_variables_initializer()
    session.run(init)

def nnet(board_size, model_file=None):
    board_size = board_size    #list
    regularization_parameter = 0.0001
    learning_rate = 0.0001

    #placeholders for input data
    input_ = tf.placeholder(dtype = tf.float32,
                                shape=[None,
                                       board_size[0],
                                       board_size[1],
                                       4],
                                name = "Layer_0_INPUT")
    
    labels = tf.placeholder(dtype = tf.float32,
                                 shape=[None,
                                        1],
                                 name = "Layer_0_labels") #containing if the game wins or not for each state
    
    mcts_probs = tf.placeholder(dtype = tf.float32,
                                     shape=[None,
                                            board_size[0],
                                            board_size[1]],
                                     name = "Layer_0_AIPlayerProbs")
    
    
    with tf.variable_scope("Common_CONV_Layers", reuse=tf.AUTO_REUSE):
        conv1 = tf.layers.conv2d(inputs=input_,
                                      filters=32,
                                      kernel_size=[3, 3],
                                      padding="same",
                                      activation=tf.nn.leaky_relu,
                                      name = "Layer_1_Convolution")
        conv2 = tf.layers.conv2d(inputs=conv1,
                                      filters=64,
                                      kernel_size=[3, 3],
                                      padding="same",
                                      activation=tf.nn.leaky_relu,
                                      name = "Layer_2_Convolution")
        conv3 = tf.layers.conv2d(inputs=conv2,
                                      filters=128,
                                      kernel_size=[3, 3],
                                      padding="same",
                                      activation=tf.nn.leaky_relu,
                                      name = "Layer_3_Convolution")
        
    with tf.variable_scope("Action_Layers", reuse=tf.AUTO_REUSE):
        action_conv1 = tf.layers.conv2d(inputs=conv3,
                                            filters=4,
                                            kernel_size=[1, 1],
                                            padding="same",
                                            activation=tf.nn.leaky_relu,
                                            name = "Layer_4_Action_Convolution")
        action_conv2 = tf.layers.conv2d(inputs=action_conv1,
                                            filters=1,
                                            kernel_size=[1, 1],
                                            padding="same",
                                            activation=tf.nn.log_softmax,
                                            name = "Layer_5_Action_Convolution") #log probability of moves
        
    with tf.variable_scope("Eval_Layers", reuse=tf.AUTO_REUSE):
        eval_conv = tf.layers.conv2d(inputs=conv3,
                                            filters=2,
                                            kernel_size=[1, 1],
                                            padding="same",
                                            activation=tf.nn.leaky_relu,
                                            name = "Layer_4_Eval_Convolution")
        eval_flatten = tf.flatten(inputs = eval_conv,
                                         name = "Layer_5_Eval_Flatten")
        eval_dense1 = tf.layers.dense(inputs=eval_flatten,
                                           units=board_size[0]*board_size[1],
                                           activation=tf.nn.leaky_relu,
                                           name = "Layer_6_Eval_Dense")
        eval_dense2 = tf.layers.dense(inputs=eval_dense1,
                                           units=1,
                                           activation=tf.nn.tanh,
                                           name = "Layer_7_Eval_Dense") #the evaluation score of each state
        
    with tf.name_scope("Losses"):
        eval_loss = tf.losses.mean_squared_error(labels,
                                                      eval_dense2)
        action_loss = tf.negative(tf.reduce_mean(tf.reduce_sum(tf.math.multiply(mcts_probs,
                                                                                     action_conv2)))) #policy loss
        l2_regularization = regularization_parameter * tf.add_n([tf.nn.l2_loss(ts) for ts in
                                                                           tf.trainable_variables()])
        
        loss = eval_loss + action_loss + l2_regularization
        
        
    with tf.name_scope("Optimization"):
        optimizer = tf.train.AdamOptimizer(
                learning_rate=learning_rate).minimize(loss)
    
    return loss, optimizer
        

