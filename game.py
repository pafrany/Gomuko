# -*- coding: utf-8 -*-
"""
@author: KemyPeti, pafrany
"""

from __future__ import print_function
import sys
import os
import tkinter as tk
from tkinter import font  as tkfont
from AI import AI

sys.path.append(os.getcwd() + '\\utils\\')

# import game_utils as GU
import numpy as np
from tkinter import *

BOARD_SIZE=15
MARKS={1:'X', 2:'O'}
COLORS={1: 'red', 2: 'blue'}


class Game_offline(tk.Tk):

    def __init__(self, mode): 
        tk.Tk.__init__(self)    
        self.stop_game=False
        self.player=1
        self.mode=mode
        self.states=[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.board=Board(self, self, mode)
        self.board.pack()
        self.board.tkraise()

        if mode==1: #1v1
        	self.callback=self.callback_1v1
        if mode==2: #AI
            self.callback=self.callback_AI
            self.history=[]
            self.AI=AI()
    def callback_AI(self, r, c):
        if self.states[r][c] != 0 or self.stop_game:
            return
        self.AI.capture_location((r, c))
        self.history.append([r, c])
        self.board.step(r, c, self.player)
        self.states[r][c] = self.player
        self.player = (self.player % 2) +1
        dir, self.stop_game=self.check_for_winner(r, c)
        if self.stop_game:
            self.board.draw_win(r, c, dir)
            return
        step=self.AI.get_AI_move(self.states)
        r, c=step[0], step[1]
        self.history.append([r, c])
        if self.states[r][c] != 0 or self.stop_game:
            return
        self.AI.capture_location((r, c))
        self.board.step(r, c, self.player)
        self.states[r][c] = self.player
        self.player = (self.player % 2) +1
        dir, self.stop_game=self.check_for_winner(r, c)
        if self.stop_game:
            self.board.draw_win(r, c, dir)
            return
    def callback_1v1(self, r, c):
        if self.states[r][c] != 0 or self.stop_game:
            return
        self.board.step(r, c, self.player)
        self.states[r][c] = self.player
        self.player = (self.player % 2) +1
        dir, self.stop_game=self.check_for_winner(r, c)
        if self.stop_game:
            self.board.draw_win(r, c, dir)
    def start_play(self):
        self.stop_game=False
    def undo(self):
        if len(self.history)<2:
            return
        field=self.history[-1]
        self.board.undo(field[0], field[1])
        self.AI.free_location(field)
        del self.history[-1]
        field=self.history[-1]
        self.board.undo(field[0], field[1])
        self.AI.free_location(field)
        del self.history[-1]

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
        

class Game_online(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Login, Register, Room):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")
        frame=Board(container, self, 0)
        frame.grid(row=1, column=0, sticky="nsew")
        self.frames['Board']=frame
        self.show_frame("Login")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Board(tk.Frame):
    def __init__(self, parent, game, mode):
        tk.Frame.__init__(self, parent, width=1000, height=700)
        self.parent=parent
        self.game=game
        self.field_buttons = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.other_buttons=[]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.field_buttons[i][j] = Button(self, font=('Arial', 20), width='1', height='1', bg='powder blue',
                         command=lambda r=i, c=j: self.game.callback(r, c))
                #self.field_buttons[i][j].grid(row=i, column=j)
                self.field_buttons[i][j].place(x=200+40*i, y=40+40*j)
        if mode==2:
            self.other_buttons.append(Button(self, font=('Arial', 20), width=4, text='Undo',
                         command=lambda: self.game.undo()))
            self.other_buttons[0].place(x=900, y=100)

    def clear(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].configure(text='', bg='powder blue', state='normal')
    def step(self, r, c, player):
        self.field_buttons[r][c].configure(text=MARKS[self.game.player], disabledforeground=COLORS[self.game.player], bg='white', state=DISABLED)
    def undo(self, r, c):
        self.field_buttons[r][c].configure(text='', disabledforeground=COLORS[self.game.player], bg='powder blue', state='normal')
    def draw_win(self, r, c, dir):
        self.field_buttons[r][c].configure(bg='red4')
        i, j=r, c
        while True:
            i, j=i+dir[0], j+dir[1]
            if any(x in set([i, j]) for x in [-1, BOARD_SIZE]):
                break
            if self.game.states[i][j]!=self.game.states[r][c]:
                break
            self.field_buttons[i][j].configure(bg='DarkOrange3')
        i, j=r,c
        while True:
            i, j=i-dir[0], j-dir[1]
            if any(x in set([i, j]) for x in [-1, BOARD_SIZE]):
                break
            if self.gamestates[i][j]!=self.game.states[r][c]:
                break
            self.field_buttons[i][j].configure(bg='DarkOrange3')

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=1000, height=700)
        #self.controller = controller
        usrnm=Entry(self, width=20)
        usrnm.place(x=400, y=250)
        psswrd=Entry(self, width=20)
        psswrd.place(x=400, y=350)

        button1 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame("Room"))
        button2 = tk.Button(self, text="Register",
                            command=lambda: controller.show_frame("Register"))
        button1.place(x=400, y=400)
        button2.place(x=500, y=400)
        label1=Label(self, text='Username')
        label1.place(x=400, y=200)
        label2=Label(self, text='Password')
        label2.place(x=400, y=300)
class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        usrnm=Entry(self, width=20)
        usrnm.place(x=400, y=250)
        psswrd=Entry(self, width=20)
        psswrd.place(x=400, y=350)
        psswrd2=Entry(self, width=20)
        psswrd2.place(x=400, y=450)
        button1 = tk.Button(self, text="Cancel",
                            command=lambda: controller.show_frame("Login"))
        button2 = tk.Button(self, text="Create account",
                            command=lambda: controller.show_frame("Login"))
        button1.place(x=400, y=500)
        button2.place(x=500, y=500)
        label1=Label(self, text='Username')
        label1.place(x=400, y=200)
        label2=Label(self, text='Password')
        label2.place(x=400, y=300)
        label2=Label(self, text='Password one more time')
        label2.place(x=400, y=400)


class Room(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.controller = controller
        scrollview=Frame(self, width=20, height=10)
        scrollview.place(x=10, y=200)
        listNodes = Listbox(scrollview, font=("Helvetica", 12))
        listNodes.grid(row=0, column=0)
        for i in range(20):
            listNodes.insert(END, str(i))
        scrollbar = Scrollbar(scrollview, orient="vertical")
        scrollbar.config(command=listNodes.yview)
        scrollbar.grid(row=0, column=1)

        listNodes.config(yscrollcommand=scrollbar.set)
        button = tk.Button(self, text="Log out", width=1, height=1,
                           command=lambda: controller.show_frame("Login"))
        button.place(x=30, y=50)
class Communicator(object):
    def __init__(self, socket):
        self.socket=socket
    def print(self, message):
        self.socket.send(message.encode())
    def read_line(self):
        return self.socket.makefile().readline()

