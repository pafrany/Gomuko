from __future__ import print_function
import pickle
from game import *
from tkinter import *


class MainMenu:
	def __init__(self):
		self.mode = 0
		self.root = Tk()
		self.root.title("Gomoku game")

		self.photo1 = PhotoImage(file="gom.gif")
		Label(self.root, image=self.photo1).grid(row=0, column=5)
		self.a = Button(self.root, text="START", width=7, command=self.indito)
		self.a.grid(row=2, column=5)
		self.b = Button(self.root, text="Online 2 player", width=7, command=self.textchanger)
		self.b.grid(row=3, column=5)
	def textchanger(self):
		self.mode = (self.mode + 1) % 3
		if self.mode == 1:
			text = "1 vs 1"
		if self.mode == 2:
			text = "1 vs cpu"
		if self.mode == 0:
			text = "Online 2 player"
		self.b.config(text=text)
	def indito(self):	
		if self.mode>0:
			game=Game_offline(self.mode)
			game.geometry("1000x700") #You want the size of the app to be 500x500
			game.resizable(0, 0)
			game.mainloop()
		else:
			game=Game_online()
			game.geometry("1000x700") #You want the size of the app to be 500x500
			game.resizable(0, 0)
			game.mainloop()	
	def start(self):
		self.root.mainloop()

main_menu=MainMenu()
main_menu.start()