<<<<<<< HEAD
=======

>>>>>>> 2bd67f714635bf2055426e9097c21cc88039ebb7

from __future__ import print_function
import sys
import os
import tkinter as tk
from tkinter import font  as tkfont
from AI import AI
import hashlib
import numpy as np
from tkinter import *
from tkinter import messagebox
import threading
from threading import Thread
from GUI import *
from communicator import *

BOARD_SIZE=15



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
		self.AI.capture_location((r, c), 1)
		self.history.append([r, c])
		self.board.step(r, c, self.player)
		self.states[r][c] = self.player
		self.player = (self.player % 2) +1
		dir, self.stop_game=self.check_for_winner(r, c)
		if self.stop_game:
			self.board.draw_win(r, c, dir)
			return
		Tk.update_idletasks(self)
		step=self.AI.get_AI_move()
		r, c=step[0], step[1]
		self.history.append([r, c])
		if self.states[r][c] != 0 or self.stop_game:
			return
		self.AI.capture_location((r, c), 2)
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
		self.selfdata=None
		self.playerdata=[]
		self.plist=[]
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		self.myturn=False
		self.myplayerid=1
		self.game_runs=False
		self.opponent=None
		self.on_board=False
		self.communicator=Communicator(self)        
		self.communicator.print('Ping\r\n')
		resp=self.communicator.read_line()

		self.playerbox=None
		self.challenged_popup=None
		self.i_challenge_popup=None
		self.rematch_in_popup=None
		self.rematch_out_popup=None
		self.give_up_popup=None

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.frames = {}
		for F in (Login, Register, Room):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=1, column=0, sticky="nsew")
		frame=Board(container, self, 0)
		frame.grid(row=1, column=0, sticky="nsew")
		self.frames['Board']=frame
		self.show_frame("Login")
		self.protocol("WM_DELETE_WINDOW", self.communicator.close)

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()
	def show_player(self, event):
		self.playerbox=Player(self, self.playerdata[self.frames['Room'].p_listNodes.curselection()[0]], self.communicator)
	

	def login(self, usrnm, psswrd):
		self.frames['Login'].del_error()
		psswrd=hashlib.md5(psswrd.encode()).hexdigest()
		self.communicator.lock.acquire()
		self.communicator.print('login\r\n')
		self.communicator.print(usrnm+'\r\n')
		resp=self.communicator.read_line()
		print(resp)
		if resp=='nincs':
			self.frames['Login'].usrnmfail.configure(text='There is no user with this name')
			self.communicator.lock.release()
			return
		if resp=='marbent':
			self.frames['Login'].usrnmfail.configure(text='User is already logged in')
			self.communicator.lock.release()
			return
		self.communicator.print(psswrd+'\r\n')
		resp=self.communicator.read_line()
		print(resp)
		if resp!='ok':
			self.frames['Login'].psswrdfail.configure(text='Incorrect password')
			self.communicator.lock.release()
			return
		self.communicator.threads_run=True
		self.communicator.lock.release()
		threading.Thread(target=self.communicator.data_update_thread, args=[], daemon=True).start()
		threading.Thread(target=self.communicator.challenge_watcher_thread, args=[], daemon=True).start()
		self.show_frame('Room')

	def reg(self, usrnm, psswrd, psswrd2):
		self.frames['Register'].del_error()
		if psswrd2!=psswrd:
			self.frames['Register'].psswrd2fail.configure(text='The passwords do not agree')
			return
		psswrd=hashlib.md5(psswrd.encode()).hexdigest()
		self.communicator.lock.acquire()
		self.communicator.print('reg\r\n')
		self.communicator.print(usrnm+'\r\n')
		resp=self.communicator.read_line()
		if resp!='ok':
			self.frames['Register'].usrnmfail.configure(text='This username is already taken')
			self.communicator.lock.release()
			return
		self.communicator.print(psswrd+'\r\n')
		resp=self.communicator.read_line()
		if resp!='ok':
			#elvileg nem fordulhat elő. vége a világnak
			self.communicator.lock.release()
			return
		messagebox.showinfo('Hurray', 'You registered successfully')
		self.show_frame('Login')
		self.communicator.lock.release()
	def logout(self):
		print(self.frames['Room'].p_listNodes.curselection())
		self.playerbox=Player(self, self.playerdata[self.frames['Room'].p_listNodes.curselection()[0]], self.communicator)
		self.communicator.lock.acquire()
		self.communicator.print('logout\r\n')
		self.communicator.lock.release()
		self.frames['Login'].delete_entry()
		self.show_frame('Login')
	def out(self, button):
		if not self.game_runs:
			if button:
				self.on_board=False
				self.show_frame('Room')
				self.communicator.lock.acquire()
				self.communicator.print('kilep\r\n')
				self.communicator.lock.release()
				self.communicator.threads_run=True
				threading.Thread(target=self.communicator.data_update_thread, args=[], daemon=True).start()
				threading.Thread(target=self.communicator.challenge_watcher_thread, args=[], daemon=True).start()
			else:
				self.on_board=False
				self.destroy()
		else:
			self.out_popup=OutPopup(self, button)
			self.out_popup.attributes('-topmost', 'true')
			self.frames['Board'].disable()

				
	def out_resp(self, decision, button):
		self.out_popup.destroy()
		if not decision:
			self.frames['Board'].enable()
			self.frames['Board'].visszvag.configure(state=DISABLED)
		else:
			self.communicator.lock.acquire()
			self.communicator.print('dezert\r\n')
			self.communicator.lock.release()
			self.on_board=False
			if button:
				self.show_frame('Room')
				threading.Thread(target=self.communicator.data_update_thread, args=[], daemon=True).start()
				threading.Thread(target=self.communicator.challenge_watcher_thread, args=[], daemon=True).start()
			else:
				self.destroy()

	def start_game(self):
		self.game_runs=True
		self.show_frame('Board')
		self.communicator.lock.acquire()
		self.communicator.print('init\r\n')
		self.opponent=self.communicator.read_line()
		self.on_board=True
		myturn=self.communicator.read_line()
		self.myturn=bool(myturn=='true')
		if not self.myturn: 
			self.myplayerid=2
		if self.myturn:
			self.frames['Board'].turn_label.config(text='It\'s your turn')
		else:
			self.frames['Board'].turn_label.config(text=self.opponent+'\'s turn')
		self.communicator.lock.release()
		threading.Thread(target=self.communicator.in_game_comm, args=[], daemon=True).start()

	def callback(self, r, c):
		self.communicator.lock.acquire()
		if self.myturn and self.game_runs and self.frames['Board'].field_buttons[r][c].cget('text')=='':
			self.myturn=False
			self.frames['Board'].step(r, c, self.myplayerid)
			self.communicator.print('lepek\r\n')
			self.communicator.print(str(r)+'\r\n')
			self.communicator.print(str(c)+'\r\n')
			self.frames['Board'].turn_label.config(text=self.opponent+'\'s turn')
		self.communicator.lock.release()
	def opponent_step(self, r, c):
		self.frames['Board'].step(r, c, (self.myplayerid%2)+1)
		self.communicator.lock.acquire()
		self.myturn=True
		self.communicator.lock.release()
		self.frames['Board'].turn_label.config(text='It\'s your turn')
	def giveup(self):
		self.give_up_popup=GiveUpPopup(self, self.communicator)
		self.give_up_popup.attributes('-topmost', 'true')
		self.frames['Board'].disable()
	def endGame(self, state):
		self.game_runs=False
		if state==1:
			text='Draw'
		if state==2:
			text='You lose'
		if state==3:
			text='You won'
		if state==4:
		    self.frames['Board'].turn_label.config('The opponent has fled')
		    self.frames['Board'].giveup.configure(state=DISABLED)
		    return
		self.frames['Board'].turn_label.config(text=text)
		self.frames['Board'].visszvag.configure(state='normal')
		self.frames['Board'].giveup.configure(state=DISABLED)
		threading.Thread(target=self.communicator.rematch_watcher_thread, args=[self.opponent], daemon=True).start()





