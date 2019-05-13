import tkinter as tk
from tkinter import *
from tkinter import messagebox
BOARD_SIZE=15
MARKS={1:'X', 2:'O'}
COLORS={1: 'red', 2: 'blue'}

class Board(Frame):
	def __init__(self, parent, game, mode):
		Frame.__init__(self, parent, width=1000, height=750)
		Frame.config(self,bg="black")
		self.parent=parent
		self.game=game
		self.field_buttons = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
		self.other_buttons=[]
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				self.field_buttons[i][j] = Button(self, font=('Arial', 20), width='1', height='1', bg='powder blue',
						 command=lambda r=i, c=j: self.game.callback(r, c))
				#self.field_buttons[i][j].grid(row=i, column=j)
				self.field_buttons[i][j].place(x=200+45*i, y=45+45*j,width=45, height=45)
		if mode==2:
			self.other_buttons.append(Button(self, font=('Arial', 20), width=4, text='Undo',
						 command=lambda: self.game.undo()))
			self.other_buttons[0].place(x=900, y=100)
		if mode==0:
			self.turn_label=Label(self, text='', fg='white', bg='black')
			self.turn_label.place(x=900, y=100)
			self.visszvag=Button(self, command=self.game.communicator.i_propose_rematch, text='Rematch', state=DISABLED)
			self.visszvag.place(x=900, y=200)
			self.other_buttons.append(self.visszvag)
			self.giveup=Button(self, command=self.game.giveup, text='Give up', state='normal')
			self.giveup.place(x=900, y=250)
			self.other_buttons.append(self.giveup)


	def clear(self):
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				self.field_buttons[i][j].configure(text='', bg='powder blue', state='normal')
	def step(self, r, c, player):
		self.field_buttons[r][c].configure(text=MARKS[player], disabledforeground=COLORS[player], bg='white', state=DISABLED)
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
	def disable(self):
		for widget in self.other_buttons:
			widget.configure(state=DISABLED)
	def enable(self):
		for widget in self. other_buttons:
			widget.configure(state='normal')

class Login(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent, width=1000, height=700)
		#self.controller = controller
		self.usrnm=Entry(self, width=20)
		self.usrnm.place(x=400, y=250)
		self.usrnmfail=Label(self, text='', fg='red')
		self.usrnmfail.place(x=420, y=270)
		self.psswrd=Entry(self, show="*", width=20)
		self.psswrd.place(x=400, y=350)
		self.psswrdfail=Label(self, text='', fg='red')
		self.psswrdfail.place(x=420, y=370)
		button1 = Button(self, text="Login",
							command=lambda: controller.login(self.usrnm.get(), self.psswrd.get()))
		button2 = Button(self, text="Register",
							command=lambda: controller.show_frame("Register"))
		button1.place(x=400, y=400)
		button2.place(x=500, y=400)
		label1=Label(self, text='Username')
		label1.place(x=400, y=200)
		label2=Label(self, text='Password')
		label2.place(x=400, y=300)
	def del_error(self):
		self.usrnmfail.configure(text='')
		self.psswrdfail.configure(text='')
	def delete_entry(self):
		self.psswrd.delete('0', 'end')
		self.usrnm.delete('0', 'end')
class Register(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.usrnm=Entry(self, width=20)
		self.usrnm.place(x=400, y=250)
		self.usrnmfail=Label(self, text='', fg='red')
		self.usrnmfail.place(x=420, y=270)
		self.psswrd=Entry(self, show="*", width=20)
		self.psswrd.place(x=400, y=350)
		self.psswrdfail=Label(self, text='', fg='red')
		self.psswrdfail.place(x=420, y=370)
		self.psswrd2=Entry(self, show="*", width=20)
		self.psswrd2.place(x=400, y=450)
		self.psswrd2fail=Label(self, text='', fg='red')
		self.psswrd2fail.place(x=420, y=470)
		button1 = Button(self, text="Cancel",
							command=lambda: controller.show_frame("Login"))
		button2 = Button(self, text="Create account",
							command=lambda: controller.reg(self.usrnm.get(), self.psswrd.get(), self.psswrd2.get()))
		button1.place(x=400, y=500)
		button2.place(x=500, y=500)
		self.label1=Label(self, text='Username')
		self.label1.place(x=400, y=200)
		self.label2=Label(self, text='Password')
		self.label2.place(x=400, y=300)
		self.label2=Label(self, text='Password (Again)')
		self.label2.place(x=400, y=400)
	def del_error(self):
		self.usrnmfail.configure(text='')
		self.psswrdfail.configure(text='')
		self.psswrd2fail.configure(text='')

class Room(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		
		self.widgets=[]
		self.p_scrollview=Frame(self, width=20, height=10)
		self.p_scrollview.place(x=10, y=200)
		self.p_listNodes = Listbox(self.p_scrollview, font=("Helvetica", 12))
		self.p_listNodes.grid(row=0, column=0)
		self.widgets.append(self. p_listNodes)
		self.p_scrollbar = Scrollbar(self.p_scrollview, orient="vertical")
		self.p_scrollbar.config(command=self.p_listNodes.yview)
		self.p_scrollbar.grid(row=0, column=1)
		self.p_listNodes.bind("<Double-Button-1>", controller.show_player)
		
		self.p_listNodes.config(yscrollcommand=self.p_scrollbar.set)
		self.g_scrollview=Frame(self, width=20, height=10)
		self.g_scrollview.place(x=600, y=200)
		self.g_listNodes = Listbox(self.g_scrollview, font=("Helvetica", 12))
		self.g_listNodes.grid(row=0, column=0)
		self.g_scrollbar = Scrollbar(self.g_scrollview, orient="vertical")
		self.g_scrollbar.config(command=self.g_listNodes.yview)
		self.g_scrollbar.grid(row=0, column=1)
		self.g_listNodes.config(yscrollcommand=self.g_scrollbar.set)        
		self.widgets.append(self.g_listNodes)

		
		self.i_scrollview=Frame(self, width=20, height=10)
		self.i_scrollview.place(x=10, y=400)
		self.i_listNodes = Listbox(self.i_scrollview, font=("Helvetica", 12))
		self.i_listNodes.grid(row=0, column=0)
		self.i_listNodes.insert(END, 'Hello!')
		self.i_scrollbar = Scrollbar(self.i_scrollview, orient="vertical")
		self.i_scrollbar.config(command=self.i_listNodes.yview)
		self.i_scrollbar.grid(row=0, column=1)
		self.i_listNodes.config(yscrollcommand=self.g_scrollbar.set)
		self.widgets.append(self.i_listNodes)

		button = Button(self, text="Log out", width=2, height=1,
						   command=lambda: controller.logout())
		self.widgets.append(button)
		button.place(x=30, y=50)
	def set_player_list(self,list):
		self.p_listNodes.delete(0, END)
		for i in range(len(list)):
			self.p_listNodes.insert(END, list[i])
	def set_games_list(self, list):
		self.g_listNodes.delete(0, END)
		for i in range(len(list)):
			self.g_listNodes.insert(END, list[i])
	def disable(self):
		for widget in self.widgets:
			widget.configure(state=DISABLED)
	def enable(self):
		for widget in self. widgets:
			widget.configure(state='normal')

class Challenged(Toplevel):
	def __init__(self, parent, communicator, who):
		Toplevel.__init__(self, parent)
		self.geometry('300x200')
		self.message=Label(self, text=who+' has challenged you')
		self.message.place(x=100, y=30)
		self.decline=Button(self, text='Decline', command=communicator.decline)
		self.decline.place(x=155, y=140)
		self.accept=Button(self, text='Accept', command=communicator.accept)
		self.accept.place(x=80, y=140)
		self.protocol("WM_DELETE_WINDOW", communicator.decline)
		#self.withdraw()
class ChallengeInProgress(Toplevel):
	def __init__(self, parent, communicator, who):
		Toplevel.__init__(self, parent)
		self.geometry('300x200')
		self.message=Label(self, text='the challenge of '+who['name']+' is in progress')
		self.message.place(x=100, y=30)
		self.decline=Button(self, text='Cancel', command=communicator.cancel)
		self.decline.place(x=155, y=140)
		self.protocol("WM_DELETE_WINDOW", communicator.cancel)
class Player(Toplevel):
	def __init__(self, parent, player, communicator):
		Toplevel.__init__(self, parent)
		self.geometry('250x300')
		ratio=str(player['won']*100/player['played']) if player['played']>0 else '0'
		texxt=player['name']+'\r\nMatch played: '+str(player['played'])+'\r\nMatch won: '+str(player['won'])+'\r\nWin percentage: '+ratio+'%'
		self.blabla=Label(self, text=player['name']+'\r\nMatch played: '+str(player['played'])+'\r\nMatch won: '+str(player['won'])+'\r\nWin percentage: '+ratio+'%', height=8)
		self.blabla.place(x=20, y=50)
		self.challenge=Button(self, text='Challenge', command=lambda: communicator.challenge(player))
		self.challenge.place(x=50, y=200)
class RematchProposalOut(Toplevel):
	def __init__(self, parent, communicator):
		Toplevel.__init__(self, parent)
		self.geometry('300x200')
		self.message=Label(self, text='You are proposing a rematch...')
		self.message.place(x=100, y=30)
		self.decline=Button(self, text='Cancel', command=communicator.rematch_cancel)
		self.decline.place(x=155, y=140)
		self.protocol("WM_DELETE_WINDOW", communicator.rematch_cancel)
class RematchProposalIn(Toplevel):
	def __init__(self, parent, communicator, who):
		Toplevel.__init__(self, parent)
		self.geometry('300x200')
		self.message=Label(self, text=who+' propses a rematch')
		self.message.place(x=100, y=30)
		self.decline=Button(self, text='Decline', command=communicator.rematch_decline)
		self.decline.place(x=155, y=140)
		self.accept=Button(self, text='Accept', command=communicator.rematch_accept)
		self.accept.place(x=80, y=140)
		self.protocol("WM_DELETE_WINDOW", communicator.rematch_decline)
class GiveUpPopup(Toplevel):
	def __init__(self, parent, communicator):
		Toplevel.__init__(self, parent)
		self.geometry('300x200')
		self.message=Label(self, text='Do you want to give up the match?')
		self.message.place(x=100, y=30)
		self.decline=Button(self, text='Yes', command=lambda: communicator.giveup(True))
		self.decline.place(x=155, y=140)
		self.accept=Button(self, text='cancel', command=lambda: communicator.giveup(False))
		self.accept.place(x=80, y=140)