import logging
from tqdm import tqdm

log = logging.getLogger(__name__)

class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it. Is necessary for verbose
                     mode.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns: player who won the game (1 if player1, -1 if player2)
 
        """
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        pieces = self.game.getInitialPieces()
        it = 0
        while self.game.getGameEnded(board, curPlayer, pieces) == 0:
            it += 1
            if verbose:
                assert self.display
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.display(board)
            action = players[curPlayer + 1](board, curPlayer, pieces)

            valids = self.game.getValidMoves(board, curPlayer, pieces)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer, pieces = self.game.getNextState(board, curPlayer, action, pieces)
        if verbose:
            assert self.display
            print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board, curPlayer, pieces)))
            self.display(board)
        return curPlayer * self.game.getGameEnded(board, curPlayer, pieces), it

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
        """

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        iterations = 0
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult, it = self.playGame(verbose=verbose)
            iterations += it
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult, it = self.playGame(verbose=verbose)
            iterations += it
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1

        return oneWon, twoWon, iterations
