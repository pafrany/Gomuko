# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:23:27 2019
@author: KemyPeti
"""

import numpy as np

#%%
from enum import Enum, unique
@unique
class Colors(Enum): # enum for the 2 "colors"
    O = 'O'
    X = 'X'
@unique
class Status(Enum): # enum for status
    before_starting = 0
    in_process = 1
    after_finish = 2
    
#%%
class Player():
    def __init__(self, name, color):
        self.name = name
        
        self.color = color
        if(color == Colors.X):
            self.sig = 1
        elif(color == Colors.O):
            self.sig = -1
        else:
            raise Exception('Incorrect color!')
        
#%%

class table():
    def __init__(self, table_size, NumCharsInRow = 5):
        if(table_size[0] < NumCharsInRow or table_size[1] < NumCharsInRow):
            raise Exception("Table with shape {0} is less than the minimum, NumCharsInRow: {1} !".format(table_size, NumCharsInRow))
            
        self.TABLE = np.zeros((table_size))
        self.height = self.TABLE.shape[0]
        self.width = self.TABLE.shape[1]
        self.chars_in_row = NumCharsInRow
        
#%%

class GameParty():
    def __init__(self, Table_size):
        self.__Table_size__ = [Table_size, Table_size]
        self.Table = table(self.__Table_size__);
        self.Players = [Player('P1', Colors.X), Player('P2', Colors.O)]; # 'X' starts
        
        #creates an array with the availabl coordinates on the table
        self.possible_steps = np.array(np.meshgrid(np.arange(0,self.__Table_size__[0]), np.arange(0,self.__Table_size__[1]))).T.reshape(-1,2)
        
        self.Status = Status.before_starting; #0 before starting, #1 in process, #2 closed session
    
    def start_game(self):
        
        self.Status = Status.in_process
        self.CurrentPlayer = self.Players[0]
        self.new_step()
        self.WINNER = None
    
    def __del__(self):
        self.Status = Status.after_finish
        print("Player "+ self.WINNER.name +" won the game")
        self.print_table()
    
    def __refresh_player__(self):
        
        if(self.CurrentPlayer == self.Players[0]):
            self.CurrentPlayer = self.Players[1]
        else:
            self.CurrentPlayer = self.Players[0]
    
    def communication(self, message):
        '''
        Azért csináltam, mert ezt helyettesíteni fogja valami GUI!!
        '''
        print(message)
        
    def get_new_coordinates(self):
        '''
        Azért csináltam, mert ezt helyettesíteni fogja valami GUI!!
        '''
        new_coordinate1 = int(input("Type the first coordinate of the next move!"))
        new_coordinate2 = int(input("Type the second coordinate of the next move!"))
        
        #check if the next field is available or not
        #ezt is GUIval kell kezelni
        if(len(np.where(np.all(self.possible_steps == np.array([new_coordinate1,new_coordinate2]),axis = 1))[0]) != 1):
            print("This coordinate [{0} {1}] is not available!".format(new_coordinate1,new_coordinate2))
            new_coordinate1,new_coordinate2 = self.get_new_coordinates()
            
        return [new_coordinate1,new_coordinate2]
    
    def print_table(self):
        '''
        Azért csináltam, mert ezt helyettesíteni fogja valami GUI!!
        '''
        
        for idx in range(self.__Table_size__[0]):
            print('| ',end="")
            for jdx in range(self.__Table_size__[0]):
                if(self.Table.TABLE[idx,jdx] == self.Players[0].sig):
                    print("X",end="")
                elif(self.Table.TABLE[idx,jdx] == self.Players[1].sig):
                    print("O",end="")
                elif(self.Table.TABLE[idx,jdx] == 0):
                    print(' ',end="")
            print('| ')
            
    def new_step(self):
        
        self.communication("\n\n\n")
        self.communication("The next player is '{0}'!".format(self.CurrentPlayer.color))
        
        self.print_table()
        next_move = self.get_new_coordinates()
        
        delete_where = np.where(np.all(self.possible_steps == np.array([next_move[0],next_move[1]]),axis = 1))[0][0]
        self.possible_steps = np.delete(self.possible_steps, delete_where, axis=0)
        
        # Next step
        self.Table.TABLE[next_move[0],next_move[1]] = self.CurrentPlayer.sig
        
        
        #refresh
        self.__refresh_player__()
        self.__won()
        self.new_step()
        
        
    def __won(self):
        for idx in range(self.__Table_size__[0]):
            for jdx in range(self.__Table_size__[1]):
                if(any([self.__check_win_rule_1([idx,jdx]),
                        self.__check_win_rule_2([idx,jdx]),
                        self.__check_win_rule_3([idx,jdx]),
                        self.__check_win_rule_4([idx,jdx])])):
                    if(self.Table.TABLE[idx,jdx] == self.Players[0].sig):
                        self.WINNER = self.Players[0]
                    else:
                        self.WINNER = self.Players[1]
                    self.__del__()
                
    def __check_win_rule_1(self, coordinates):
        '''
        5 in 1 row
        '''
        if(coordinates[1] + 4>=self.__Table_size__[1]):
            return 0
        else:
            if(self.Table.TABLE[coordinates[0],coordinates[1]] == 
               self.Table.TABLE[coordinates[0],coordinates[1]+1] == 
               self.Table.TABLE[coordinates[0],coordinates[1]+2] ==
               self.Table.TABLE[coordinates[0],coordinates[1]+3] ==
               self.Table.TABLE[coordinates[0],coordinates[1]+4] and
               self.Table.TABLE[coordinates[0],coordinates[1]] != 0 ):
                return 1
            else:
                return 0
        
    def __check_win_rule_2(self, coordinates):
        '''
        5 in diagonal,  left->right
                        top->bottom
        '''
        if(coordinates[0] + 4>=self.__Table_size__[0] or 
           coordinates[1] + 4>=self.__Table_size__[1]):
            return 0
        
        else:
            if(self.Table.TABLE[coordinates[0],coordinates[1]] == 
               self.Table.TABLE[coordinates[0]+1,coordinates[1]+1] == 
               self.Table.TABLE[coordinates[0]+2,coordinates[1]+2] ==
               self.Table.TABLE[coordinates[0]+3,coordinates[1]+3] ==
               self.Table.TABLE[coordinates[0]+4,coordinates[1]+4] and
               self.Table.TABLE[coordinates[0],coordinates[1]] != 0 ):
                return 1
            else:
                return 0
            
    def __check_win_rule_3(self, coordinates):
        '''
        5 in diagonal,  right->left
                        top->bottom
        '''
        if(coordinates[0] + 4>=self.__Table_size__[0] or 
           coordinates[1] - 4<0):
            return 0
        
        else:
            if(self.Table.TABLE[coordinates[0],coordinates[1]] == 
               self.Table.TABLE[coordinates[0]+1,coordinates[1]-1] == 
               self.Table.TABLE[coordinates[0]+2,coordinates[1]-2] ==
               self.Table.TABLE[coordinates[0]+3,coordinates[1]-3] ==
               self.Table.TABLE[coordinates[0]+4,coordinates[1]-4] and
               self.Table.TABLE[coordinates[0],coordinates[1]] != 0 ):
                return 1
            else:
                return 0
        
    def __check_win_rule_4(self, coordinates):
        '''
        5 in diagonal,  right->left
                        top->bottom
        '''
        if(coordinates[0] + 4>=self.__Table_size__[0]):
            return 0
        
        else:
            if(self.Table.TABLE[coordinates[0],coordinates[1]] == 
               self.Table.TABLE[coordinates[0]+1,coordinates[1]] == 
               self.Table.TABLE[coordinates[0]+2,coordinates[1]] ==
               self.Table.TABLE[coordinates[0]+3,coordinates[1]] ==
               self.Table.TABLE[coordinates[0]+4,coordinates[1]] and
               self.Table.TABLE[coordinates[0],coordinates[1]] != 0 ):
                return 1
            else:
                return 0
          

#%% Example

Party = GameParty()
Party.start_game()
