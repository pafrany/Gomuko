# -*- coding: utf-8 -*-
"""
@author: KemyPeti, pafrany
"""

from __future__ import print_function
import sys
import os
import tkinter

sys.path.append(os.getcwd() + '\\utils\\')

# import game_utils as GU
import numpy as np
from tkinter import *

BOARD_SIZE=15
MARKS={1:'X', 2:'O'}
COLORS={1: 'red', 2: 'blue'}


class Game(object):
    class Board(object):
        def __init__(self, parent, mode):
            self.parent=parent
            self.field_buttons = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
            self.other_buttons=[]
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    self.field_buttons[i][j] = Button(parent.window, font=('Arial', 20), width=4, bg='powder blue',
                             command=lambda r=i, c=j: self.parent.callback(r, c))
                    self.field_buttons[i][j].grid(row=i, column=j)
            if mode==0: #játékmódtól függően a különböző GUI elemek
                self.other_buttons.append(None) #így

        def clear(self):
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    self.buttons[i][j].configure(text='', bg='powder blue', state='normal')
        def step(self, r, c, player):
            self.field_buttons[r][c].configure(text=MARKS[self.parent.player], disabledforeground=COLORS[self.parent.player], bg='white', state=DISABLED)
        def draw_win(self, r, c, dir):
            self.field_buttons[r][c].configure(bg='red4')
            i, j=r, c
            while True:
                i, j=i+dir[0], j+dir[1]
                if any(x in set([i, j]) for x in [-1, BOARD_SIZE]):
                    break
                if self.parent.states[i][j]!=self.parent.states[r][c]:
                    break
                self.field_buttons[i][j].configure(bg='DarkOrange3')
            i, j=r,c
            while True:
                i, j=i-dir[0], j-dir[1]
                if any(x in set([i, j]) for x in [-1, BOARD_SIZE]):
                    break
                if self.parent.states[i][j]!=self.parent.states[r][c]:
                    break
                self.field_buttons[i][j].configure(bg='DarkOrange3')

    def __init__(self, window, mode):     
        self.stop_game=True
        self.player=1
        self.mode=mode
        self.window=window
        self.states=[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.board=self.Board(self, mode)
        if mode==1:
        	self.callback=self.callback_1v1
    def callback_1v1(self, r, c):
        if self.states[r][c] != 0 or self.stop_game:
            return
        self.board.step(r, c, self.player)
        self.states[r][c] = self.player
        self.player = (self.player % 2) +1
        dir, self.stop_game=self.check_for_winner(r, c)
        if self.stop_game:
            self.board.draw_win(r, c, dir)
    def callback_vscomp(self, r, c):
    	print('blee')
    def start_play(self):
        self.stop_game=False
    def check_for_winner(self, r, c):
        for dir in [[0, 1], [1, 0], [1, 1], [1, -1]]:
            num=1
            for sign in [1, -1]:
                i, j=r, c
                while True:
                    i, j=i+sign*dir[0], j+sign*dir[1]
                    if any(x in set([i, j]) for x in [-1, BOARD_SIZE]):
                        break
                    if self.states[i][j]==self.states[r][c]:
                        num+=1
                        if num==5:
                            return dir, True
                    else:
                        break
        return None, False
        





"""
def jatek():
    window = Toplevel(root)
    def callback(r, c):
        global player
        print(r)
        print(c)
        if states[r][c] == 0:
            b[r][c].configure(text=MARKS[player], fg=COLORS[player], bg='white')
            states[r][c] = player
            player = (player % 2) +1
            print(player)
        stop_game=check_for_winner(r, c)
        print(stop_game)




    states = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    b = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            b[i][j] = Button(window, font=('Arial', 20), width=4, bg='powder blue',
                             command=lambda r=i, c=j: callback(r, c))
            b[i][j].grid(row=i, column=j)
    player = 1
    stop_game = False
"""
