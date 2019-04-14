from tkinter import *

def callback(r,c):
    global player

    if player == 'X' and states[r][c]==0 and stop_game== False:
        b[r][c].configure(text='X', fg='red', bg='white')
        states[r][c] ='X'
        player = 'O'

    if player == 'O' and states[r][c]==0 and stop_game== False:
        b[r][c].configure(text='O', fg='blue', bg='white')
        states[r][c] ='O'
        player = 'X'
    check_for_winner()

def check_for_winner():
    global stop_game
    for i2 in range(15):
        for j2 in range(11):
            if states[i2][j2] == states[i2][j2+1] == states[i2][j2+2] == states[i2][j2+3] == states[i2][j2+4] != 0:
                for h in range(5):
                    b[i2][j2+h].config(bg='grey')
                stop_game = True
    for i2 in range(11):
        for j2 in range(15):
            if states[i2][j2] == states[i2+1][j2] == states[i2+2][j2] == states[i2+3][j2] == states[i2+4][j2] != 0:
                for h in range(5):
                    b[i2+h][j2].config(bg='grey')
                stop_game = True
    for i2 in range(11):
        for j2 in range(11):
            if states[i2][j2] == states[i2+1][j2+1] == states[i2+2][j2+2] == states[i2+3][j2+3] == states[i2+4][j2+4] \
                    != 0:
                for h in range(5):
                    b[i2+h][j2+h].config(bg='grey')
                stop_game = True
    for i2 in range(15):
        for j2 in range(15):
            if states[i2][j2] == states[i2+1][j2-1] == states[i2+2][j2-2] == states[i2+3][j2-3] == states[i2+4][j2-4]\
                    != 0:
                for h in range(5):
                    b[i2+h][j2-h].config(bg='grey')
                stop_game = True

root = Tk()
root.title("Gomoku game")

b = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

states = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

for i in range(15):
    for j in range(15):
        b[i][j] = Button(font=('Arial', 20), width=4, bg='powder blue',
                         command=lambda r=i, c=j: callback(r, c))
        b[i][j].grid(row=i, column=j)
player='X'
stop_game = False

mainloop()