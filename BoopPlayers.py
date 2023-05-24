import numpy as np
import random 

# Agent that randomly selects a move.
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board, player, pieces):
        print("___________________")
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, player, pieces)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a

# Agent that randomly selects a move, but the center four squares has 10 times the likelihood of being selected.
class RandomPlayerWithCenterBias():
    def __init__(self, game):
        self.game = game

    def play(self, board, player, pieces):
        print("___________________")
        
        # Define the weights for each number
        weights = [10 if x in [14, 15, 20, 21] else 1 for x in list(range(72))]
        a = random.choices(list(range(72)), weights, k=1)[0]
        valids = self.game.getValidMoves(board, player, pieces)
        while valids[a]!=1:
            # Randomly select a number with the specified weights
            a = random.choices(list(range(72)), weights, k=1)[0]
        return a