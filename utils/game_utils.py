# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:15:06 2019

@author: KemyPeti
"""
from __future__ import absolute_import, division, print_function
import numpy as np


import tensorflow as tf

class position():
    
    @staticmethod
    def IDX_to_position(height, width, IDX):
        """
        Ex:
        IDX_to_position(10,10,11) -> [1,1]
        
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = IDX // width
        w = IDX % width
        return [h, w]
    
    @staticmethod
    def position_to_IDX(height, width, position):
        
        if len(position) != 2:
            return -1
        h = position[0]
        w = position[1]
        IDX = h * width + w
        
        if IDX not in range(width * height):
            return -1
        
        return IDX

class math():
    
    @staticmethod
    def softmax(x):
        return tf.nn.softmax(x).numpy()
    
    @staticmethod
    def dense(X, W, b):
        out = np.dot(X, W) + b 
        return out
    
    @staticmethod
    def conv2D(X, W, b):
        X = np.transpose(X, (0, 2, 3, 1))
        W = np.transpose(W, (2, 3, 1, 0))
        tconv = tf.nn.conv2d(X, W, [1,1,1,1], padding = 'SAME')
        tconv = tf.nn.bias_add(tconv, b)
        return np.transpose(tf.nn.relu(tconv).numpy(),(0,3,1,2))
