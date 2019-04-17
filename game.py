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
marks={1:'X', 2:'O'}
class Board(object):

    def __init__(self,
                 width=BOARD_SIZE,
                 height=BOARD_SIZE,
                 n_in_row=5,
                 start_player=0):
        '''
        Variables:
            \n\t * width: table size
            \n\t * height: table size
            \n\t * n_in_row: need n symbol in a row
            \n\t * availables: available fields
            \n\t * states: step and player
            \n\t * players: [1,2]
            \n\t * current_player: next player
            \n\t * last_move: index of the last move 
        Methods:
            \n\t * init_board: initialize the table
            \n\t * move_to_location: translate index to coordinates
            \n\t * location_to_move: translate coordinates to index
            \n\t * current_state: returns with the state tensor
            \n\t * do_move: next move
            \n\t * has_a_winner: check for winner
            \n\t * game_end: run has_a_winner
            \n\t * get_current_player: returns with the current player 
        '''

        if width < n_in_row or height < n_in_row:
            raise Exception('Width and height should be greater than the "n_in_row"')

        self.width = width
        self.height = height
        self.n_in_row = n_in_row

        self.states = {}

        self.players = [1, 2]  # player1 and player2

    def init_board(self, start_player=0):
        self.availables = list(range(self.width * self.height))
        self.current_player = self.players[start_player]  # start player
        self.last_move = -1

    def move_to_location(self, move):
        return GU.position.IDX_to_position(height=self.height,
                                           width=self.width,
                                           IDX=move)

    def location_to_move(self, location):
        return GU.position.position_to_IDX(height=self.height,
                                           width=self.width,
                                           position=location)

    def current_state(self):
        """return the board state from the perspective of the current player.
        state shape: 4*width*height
        """

        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width,
                            move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width,
                            move_oppo % self.height] = 1.0
            # indicate the last move location
            square_state[2][self.last_move // self.width,
                            self.last_move % self.height] = 1.0
        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0  # indicate the colour to play
        return square_state[:, ::-1, :]

    def do_move(self, move):
        self.states[move] = self.current_player
        self.availables.remove(move)
        self.current_player = (
            self.players[0] if self.current_player == self.players[1]
            else self.players[1]
        )
        self.last_move = move

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < self.n_in_row * 2 - 1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):
            return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player


class Game(object):
    """game server"""

    def __init__(self, board, **kwargs):
        self.board = board

    def graphic(self, board, player1, player2, players, p1, p2):
        root = tkinter.Tk()
        root.title("Gomoku game")

        def callback(r, c):
            global player
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]

            if (player_in_turn.player == player2):  # robot step
                move = player_in_turn.set_action(self.board)
                pos = GU.position.IDX_to_position(self.board.width, self.board.height, move)
                b[pos[0]][pos[1]].configure(text='O', fg='blue', bg='white')
            else:  # human step
                move = -1
                while (move == -1):
                    b[r][c].configure(text='X', fg='red', bg='white')
                    move = player_in_turn.set_action(self.board, [r, c])
                    if (move == -1 or move not in self.board.availables):
                        print("invalid move")
                        move = -1

            self.board.do_move(move)
            end, winner = self.board.game_end()
            if end:
                if winner != -1:
                    print("Game end. Winner is", players[winner])
                else:
                    print("Game end. Tie")
                return winner

        def generate_list_table(N):
            out = []
            for idx in range(N):
                tmp = []
                for jdx in range(N):
                    tmp.append(0)
                out.append(tmp)
            return out

        N = self.board.width
        b = generate_list_table(N)
        for i in range(N):
            for j in range(N):
                b[i][j] = tkinter.Button(font=('Arial', 20), width=4, bg='powder blue',
                                         command=lambda r=i, c=j: callback(r, c))
                b[i][j].grid(row=i, column=j)
        tkinter.mainloop()

    def start_play(self, player1, player2, start_player=0, is_shown=1):
        """start a game between two players"""
        if start_player not in (0, 1):
            raise Exception('start_player should be either 0 (player1 first) '
                            'or 1 (player2 first)')
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if is_shown:
            self.graphic(self.board, player1.player, player2.player, players, p1, p2)

    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree,
        and store the self-play data: (state, mcts_probs, z) for training
        """
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board,
                                                 temp=temp,
                                                 return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            # perform a move
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, p1, p2)
            end, winner = self.board.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)


def close_window():
    root.destroy()
    exit()


# def click():
def textchanger():
    global szam

    szam = (szam + 1) % 3

    if szam == 1:
        text = "1 vs 1"
    if szam == 2:
        text = "1 vs cpu"
    if szam == 0:
        text = "2 player"
    # btn['text'] = text
    b.config(text=text)


def jatek():
    window = Toplevel(root)
    def callback(r, c):
        global player
        print(r)
        print(c)
        if states[r][c] == 0 and stop_game == False:
            b[r][c].configure(text=marks[player], fg=['red', 'blue'][player-1], bg='white')
            states[r][c] = player
            player = (player % 2) +1
            print(player)
        check_for_winner(r, c)

    def check_for_winner(r, c):
        global stop_game
        for i2 in range(15):
            for j2 in range(11):
                if states[i2][j2] == states[i2][j2 + 1] == states[i2][j2 + 2] == states[i2][j2 + 3] == states[i2][
                    j2 + 4] != 0:
                    for h in range(5):
                        b[i2][j2 + h].config(bg='grey')
                    stop_game = True
        for i2 in range(11):
            for j2 in range(15):
                if states[i2][j2] == states[i2 + 1][j2] == states[i2 + 2][j2] == states[i2 + 3][j2] == states[i2 + 4][
                    j2] != 0:
                    for h in range(5):
                        b[i2 + h][j2].config(bg='grey')
                    stop_game = True
        for i2 in range(11):
            for j2 in range(11):
                if states[i2][j2] == states[i2 + 1][j2 + 1] == states[i2 + 2][j2 + 2] == states[i2 + 3][j2 + 3] == \
                        states[i2 + 4][j2 + 4] \
                        != 0:
                    for h in range(5):
                        b[i2 + h][j2 + h].config(bg='grey')
                    stop_game = True
        for i2 in range(15):
            for j2 in range(15):
                if states[i2][j2] == states[i2 + 1][j2 - 1] == states[i2 + 2][j2 - 2] == states[i2 + 3][j2 - 3] == \
                        states[i2 + 4][j2 - 4] \
                        != 0:
                    for h in range(5):
                        b[i2 + h][j2 - h].config(bg='grey')
                    stop_game = True


    states = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    b = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            b[i][j] = Button(window, font=('Arial', 20), width=4, bg='powder blue',
                             command=lambda r=i, c=j: callback(r, c))
            b[i][j].grid(row=i, column=j)
    player = 1
    stop_game = False




def indito():
    # if szam ==1: # Andris vmilyét hívja meg

    # if szam == 2:
    # start_play()
    if szam == 3 or szam == 0:
        jatek()


szam = 0
root = Tk()
root.title("Gomoku game")

photo1 = PhotoImage(file="gom.gif")
Label(root, image=photo1).grid(row=0, column=5)
a = Button(root, text="START", width=7, command=indito)
a.grid(row=2, column=5)
b = Button(root, text="2 player", width=7, command=textchanger)
b.grid(row=3, column=5)
player = 1
root.mainloop()
