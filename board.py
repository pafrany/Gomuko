import game

BOARD_SIZE=game.BOARD_SIZE

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