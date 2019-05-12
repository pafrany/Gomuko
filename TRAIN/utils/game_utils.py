# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:15:06 2019

@author: KemyPeti
"""

import numpy as np

class position():
    
    @staticmethod
    def IDX_to_position(height, width, IDX):
        """
        Ex:
        IDX_to_position(10,10,11) -> [1,1]
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
        probs = np.exp(x - np.max(x))
        probs /= np.sum(probs)
        return probs
    
    @staticmethod
    def relu(X):
        out = np.maximum(X, 0)
        return out
    
    @staticmethod
    def dense(X, W, b):
        out = np.dot(X, W) + b
        return out
    
    @staticmethod
    def conv2D(X, W, b, stride=1, padding=1):
        n_filters, d_filter, h_filter, w_filter = W.shape
        
        W = W[:, :, ::-1, ::-1] #x(t)*h(t-theta) 
        
        n_x, d_x, h_x, w_x = X.shape
        h_out = (h_x - h_filter + 2 * padding) / stride + 1
        w_out = (w_x - w_filter + 2 * padding) / stride + 1
        h_out, w_out = int(h_out), int(w_out)
        X_col = math.im2col_indices(X, h_filter, w_filter,
                               padding=padding, stride=stride)
        W_col = W.reshape(n_filters, -1)
        out = (np.dot(W_col, X_col).T + b).T
        out = out.reshape(n_filters, h_out, w_out, n_x)
        out = out.transpose(3, 0, 1, 2)
        return math.relu(out)
    
    @staticmethod
    def get_im2col_indices(x_shape, field_height,
                           field_width, padding=1, stride=1):
        # First figure out what the size of the output should be
        N, C, H, W = x_shape
        assert (H + 2 * padding - field_height) % stride == 0
        assert (W + 2 * padding - field_height) % stride == 0
        out_height = int((H + 2 * padding - field_height) / stride + 1)
        out_width = int((W + 2 * padding - field_width) / stride + 1)
    
        i0 = np.repeat(np.arange(field_height), field_width)
        i0 = np.tile(i0, C)
        i1 = stride * np.repeat(np.arange(out_height), out_width)
        j0 = np.tile(np.arange(field_width), field_height * C)
        j1 = stride * np.tile(np.arange(out_width), out_height)
        i = i0.reshape(-1, 1) + i1.reshape(1, -1)
        j = j0.reshape(-1, 1) + j1.reshape(1, -1)
    
        k = np.repeat(np.arange(C), field_height * field_width).reshape(-1, 1)
    
        return (k.astype(int), i.astype(int), j.astype(int))

    @staticmethod
    def im2col_indices(x, field_height, field_width, padding=1, stride=1):
        p = padding
        x_padded = np.pad(x, ((0, 0), (0, 0), (p, p), (p, p)), mode='constant')
    
        k, i, j = math.get_im2col_indices(x.shape, field_height,
                                     field_width, padding, stride)
    
        cols = x_padded[:, k, i, j]
        C = x.shape[1]
        cols = cols.transpose(1, 2, 0).reshape(field_height * field_width * C, -1)
        return cols
        