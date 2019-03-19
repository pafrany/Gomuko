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
    def __init__(self, name,color):
        self.name = name
        
        self.color = color
        if(color == Colors.X):
            self.sig = 1
        elif(color == Colors.O):
            self.sig = -1
        else:
            raise('Incorrect color!')
        
#%%

class table():
    def __init__(self, table_size):
        self.TABLE = np.zeros((table_size))
        
#%%

class GameParty():
    def __init__(self, Table_size):
        self.__Table_size__ = [Table_size, Table_size]
        self.Table = table(self.__Table_size__);
        self.Player1 = Player('P1', Colors.X);
        self.Player2 = Player('P2', Colors.O);
        self.Status = Status.before_starting; #0 before starting, #1 in process, #2 closed session
    def new_step(self, player_number, coordinates):
        '''
        
        Player1  --  X  --  1
        Player2  --  O  -- -1
        
        '''
        if(player_number != 1 and player_number != 2): # Check correct player number
            raise("player_number should be 1 or 2")
        if(coordinates[0]+1 > self.__Table_size__[0] or coordinates[0] < 0 or 
           coordinates[1]+1 > self.__Table_size__[1] or coordinates[1] < 1):
            raise("The coordinates are incorrect! Table size: {0}".format(self.Table_size))
        
        if(self.Table.TABLE[coordinates] != 0): # Check the place on the table
            raise("This place is already used!")
        
        if(np.sum(self.Table.TABLE) == 1 and player_number == 1):  # Check if the next player is the correct one!
            raise("Next step -> Player 2")
        elif(np.sum(self.Table.TABLE) == 0 and player_number == 2):
            raise("Next step -> Player 1")
        
        if(not (np.any(self.Table == -1) or np.any(self.Table == 1))): # Change game status
            self.Status = Status.in_process
        
        # Next step
        self.Table.TABLE[coordinates] = eval("self.Player" + str(player_number) +  ".sig")
        
          
          

#%% Example

Party = GameParty(Table_size = 11)

Party.new_step(1,(1,1))

Party.new_step(2,(2,1))
A = Party.Table.TABLE