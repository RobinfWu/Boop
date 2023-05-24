from BoopLogic import Board
import numpy as np
import copy

class BoopGame():
    def __init__(self, n=6):
        self.n = n
        self.pieces = {
            1: {1: 8, 2: 0},  # For Orange (1: Kitten, 2: Cat)
            -1: {-1: 8, -2: 0},  # For Grey (-1: Kitten, -2: Cat)
        }

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.board)

    # Add this method to your BoopGame class
    def getInitialPieces(self):
        return {
            1: {1: 8, 2: 0},  # For Orange (1: Kitten, 2: Cat)
            -1: {-1: 8, -2: 0},  # For Grey (-1: Kitten, -2: Cat)
        }

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions: 2 actions (place kitten or cat) for each square, plus 1 for pass
        return self.n*self.n*2
    
    def getNextState(self, board, player, action, pieces):
        b = Board(self.n, copy.deepcopy(pieces))
        b.board = np.copy(board)
        
        pieceType = 1 * player if action < self.n*self.n else 2 * player  # 1 for kitten, 2 for cat
        action = action % (self.n*self.n)  # Now action is within the range of the number of board positions

        move = (int(action/self.n), action%self.n)
        b.execute_move(move, player, pieceType)
        assert sum(value for key, value in b.pieces[player].items()) + np.count_nonzero(b.board == player * 1) + np.count_nonzero(b.board == player * 2) == 8, "The number of pieces on the board and off the board do not sum up to 8"
        return (b.board, -player, b.pieces)

    # 1 = Player Orange, -1 = Player Grey
    def getValidMoves(self, board, player, pieces):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n, copy.deepcopy(pieces))
        b.board = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves)==0:
            return np.array(valids)

        for move in legalMoves:
            (x, y), piece = move

            if piece == player * 1:  # If it's a kitten
                index = self.n*x + y
                valids[index] = 1

            elif piece == player * 2:  # If it's a cat
                index = self.n*self.n + self.n*x + y
                valids[index] = 1

        return np.array(valids)

    def getGameEnded(self, board, player, pieces):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        b = Board(self.n, copy.deepcopy(pieces))
        b.board = np.copy(board)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1

        # draw has a very little value 
        return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == 2 * self.n**2)  # No pass action
        mid_index = len(pi) // 2
        pi_board_kittens = np.reshape(pi[:mid_index], (self.n, self.n))
        pi_board_cats = np.reshape(pi[mid_index:], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi_kittens = np.rot90(pi_board_kittens, i)
                newPi_cats = np.rot90(pi_board_cats, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi_kittens = np.fliplr(newPi_kittens)
                    newPi_cats = np.fliplr(newPi_cats)
                newPi = np.concatenate((newPi_kittens.ravel(), newPi_cats.ravel()))
                l += [(newB, list(newPi))]
        return l

    @staticmethod
    def display(board):
        display(board)