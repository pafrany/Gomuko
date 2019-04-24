import tkinter as tk
from tkinter import *
from tkinter import messagebox
BOARD_SIZE=15
MARKS={1:'X', 2:'O'}
COLORS={1: 'red', 2: 'blue'}

class Board(Frame):
    def __init__(self, parent, game, mode):
        Frame.__init__(self, parent, width=1000, height=700)
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
        #self.controller = controller
        self.p_scrollview=Frame(self, width=20, height=10)
        self.p_scrollview.place(x=10, y=200)
        self.p_listNodes = Listbox(self.p_scrollview, font=("Helvetica", 12))
        self.p_listNodes.grid(row=0, column=0)
        for i in range(20):
            self.p_listNodes.insert(END, str(i))
        self.p_scrollbar = Scrollbar(self.p_scrollview, orient="vertical")
        self.p_scrollbar.config(command=self.p_listNodes.yview)
        self.p_scrollbar.grid(row=0, column=1)

        self.p_listNodes.config(yscrollcommand=self.p_scrollbar.set)
        self.g_scrollview=Frame(self, width=20, height=10)
        self.g_scrollview.place(x=600, y=200)
        self.g_listNodes = Listbox(self.g_scrollview, font=("Helvetica", 12))
        self.g_listNodes.grid(row=0, column=0)
        for i in range(20):
            self.g_listNodes.insert(END, str(i))
        self.g_scrollbar = Scrollbar(self.g_scrollview, orient="vertical")
        self.g_scrollbar.config(command=self.g_listNodes.yview)
        self.g_scrollbar.grid(row=0, column=1)

        self.g_listNodes.config(yscrollcommand=self.g_scrollbar.set)
        button = Button(self, text="Log out", width=1, height=1,
                           command=lambda: controller.logout())
        button.place(x=30, y=50)
    def set_player_list(self,list):
        self.p_listNodes.delete(0, END)
        for i in range(len(list)):
            self.p_listNodes.insert(END, list[i])
    def set_games_list(self, list):
        self.g_listNodes.delete(0, END)
        for i in range(len(list)):
            self.g_listNodes.insert(END, list[i])
