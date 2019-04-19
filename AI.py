from game import *
from mcts_alphaZero import MCTSPlayer
from policy_value_net_play import PolicyValueNetPlay
from random import randint


class AI:
	def __init__(self):
		self.availables = list(range(self.width * self.height))

	def move_to_location(self, move):
        return GU.position.IDX_to_position(height=game.BOARD_SIZE,
                                           width=game.BOARD_SIZE,
                                           IDX=move)

    def location_to_move(self, location):
        return GU.position.position_to_IDX(height=game.BOARD_SIZE,
                                           width=game.BOARD_SIZE,
                                           position=location)
	
	def get_AI_move(self, states): 
		while True:
			a=randint(0, 15)
			b=randint(0, 15)
			if states[a][b]==0:
				return (a, b)

	def capture_location(self, location):
		self.availables.remove(self.location_to_move(location))

	def free_location(self, location): #undo esetére
		self.availables.append(self.location_to_move(location))
		self.availables=sorted(self.availables)

