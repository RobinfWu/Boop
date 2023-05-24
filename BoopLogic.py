class Board():
    def __init__(self, n=6, pieces=None):
        self.n = n
        self.pieces = pieces if pieces else {
            1: {1: 8, 2: 0},  # For Orange (1: Kitten, 2: Cat)
            -1: {-1: 8, -2: 0},  # For Grey (-1: Kitten, -2: Cat)
        }

        # Create the empty board array.
        self.board = [None]*self.n
        for i in range(self.n):
            self.board[i] = [0]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    # returns a list of coordinates of playable moves.
    def get_legal_moves(self, player):
        """Returns all the legal moves for the given color.
        (2 for Orange Cat, 1 for Orange Kitten, -1 for Grey Kitten, -2 for Grey Cat)
        """
        moves = []  # stores the legal moves.

        # Check if player is out of pieces altogether
        total_pieces = sum(self.pieces[player].values())

        # If player has no more pieces left, remove a piece from the board
        if total_pieces <= 0:  
            for y in range(self.n):
                for x in range(self.n):
                    if self.board[x][y] == player * 1:  # If there's a kitten of the same color at (x, y)
                        newmove = ((x, y), player*2)  # Promotion move, kitten is removed from the board
                        moves.append(newmove)
        else:
            # Check which pieces are available for current player
            available_pieces = [piece for piece, count in self.pieces[player].items() if count > 0]
            # For each available piece, find the legal moves
            for piece in available_pieces:
                for y in range(self.n):
                    for x in range(self.n):
                        if self.board[x][y] == 0:  # ensure the cell is empty
                            newmove = ((x, y), piece)
                            moves.append(newmove)
        return moves
    
    def execute_move(self, move, color, pieceType):
        """Perform the given move on the board; 
        color gives the color of the piece to play (1=orange, -1=grey)
        type indicates type of the piece to play (1=kitten, 2=cat)
        """

        (x,y) = move
        
        # If the cell is empty, add the piece to the empty square.
        if self.board[x][y] == 0:
            self.board[x][y] = pieceType
            self.boop(x, y)
            self.checkPromotion()
            self.pieces[color][pieceType] -= 1
            
        # If the cell contains a kitten of the same color, promote the kitten to a cat.
        elif self.board[x][y] == color:
            self.board[x][y] = 0
            self.pieces[color][2*color] += 1  # Increase cat count
            
    def boop(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # 8 directions
        current_piece = self.board[row][col]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 6 and 0 <= new_col < 6:  # check if in bounds
                if self.board[new_row][new_col] != 0:  # check if the spot is not empty
                    # Do not move if the current piece is a kitten and the piece to be moved is a cat
                    if abs(current_piece) == 1 and abs(self.board[new_row][new_col]) == 2:
                        continue
                    new_new_row, new_new_col = new_row + dr, new_col + dc
                    if 0 <= new_new_row < 6 and 0 <= new_new_col < 6:  # check if new spot is in bounds
                        if self.board[new_new_row][new_new_col] == 0:  # check if new spot is unoccupied
                            self.board[new_new_row][new_new_col] = self.board[new_row][new_col]  # move piece
                            self.board[new_row][new_col] = 0  # empty old spot
                    else:
                        # If the new spot is out of bounds, remove the piece and update the counts
                        piece = self.board[new_row][new_col]
                        color = piece / abs(piece)  # This will give 1 for Orange and -1 for Grey
                        self.board[new_row][new_col] = 0
                        if abs(piece) == 1:
                            self.pieces[color][1 * color] += 1  # increase kitten count
                        if abs(piece) == 2:
                            self.pieces[color][2 * color] += 1  # increase cat count

    def findThreeInRowHorizontal(self):
        for row in self.board:
            for i in range(4):
                # Check if the pieces are of the same color (positive for Orange, negative for Grey)
                if (row[i] > 0 and row[i + 1] > 0 and row[i + 2] > 0) or (row[i] < 0 and row[i + 1] < 0 and row[i + 2] < 0):
                    # If all pieces are Cats, skip this row
                    if abs(row[i]) == abs(row[i + 1]) == abs(row[i + 2]) == 2:
                        continue
                    color = 1 if row[i] > 0 else -1  # get color
                    self.pieces[color][color * 2] += 3  # increment the cat count for this color
                    row[i] = row[i + 1] = row[i + 2] = 0
                    return True
        return False

    def findThreeInRowVertical(self):
        for j in range(6):
            for i in range(4):
                # Check if the pieces are of the same color (positive for Orange, negative for Grey)
                if (self.board[i][j] > 0 and self.board[i + 1][j] > 0 and self.board[i + 2][j] > 0) or \
                   (self.board[i][j] < 0 and self.board[i + 1][j] < 0 and self.board[i + 2][j] < 0):
                    # If all pieces are Cats, skip this row
                    if abs(self.board[i][j]) == abs(self.board[i + 1][j]) == abs(self.board[i + 2][j]) == 2:
                        continue
                    color = 1 if self.board[i][j] > 0 else -1  # get color
                    self.pieces[color][color * 2] += 3  # increment the cat count for this color
                    self.board[i][j] = self.board[i + 1][j] = self.board[i + 2][j] = 0
                    return True
        return False

    def findThreeInRowMainDiagonals(self):
        for i in range(4):
            for j in range(4):
                # Check if the pieces are of the same color (positive for Orange, negative for Grey)
                if (self.board[i][j] > 0 and self.board[i + 1][j + 1] > 0 and self.board[i + 2][j + 2] > 0) or \
                   (self.board[i][j] < 0 and self.board[i + 1][j + 1] < 0 and self.board[i + 2][j + 2] < 0):
                    # If all pieces are Cats, skip this row
                    if abs(self.board[i][j]) == abs(self.board[i + 1][j + 1]) == abs(self.board[i + 2][j + 2]) == 2:
                        continue
                    color = 1 if self.board[i][j] > 0 else -1  # get color
                    self.pieces[color][color * 2] += 3  # increment the cat count for this color
                    self.board[i][j] = self.board[i + 1][j + 1] = self.board[i + 2][j + 2] = 0
                    return True
        return False    

    def findThreeInRowMainAntiDiagonals(self):
        for i in range(4):
            for j in range(2, 6):
                # Check if the pieces are of the same color (positive for Orange, negative for Grey)
                if (self.board[i][j] > 0 and self.board[i + 1][j - 1] > 0 and self.board[i + 2][j - 2] > 0) or \
                   (self.board[i][j] < 0 and self.board[i + 1][j - 1] < 0 and self.board[i + 2][j - 2] < 0):
                    # If all pieces are Cats, skip this row
                    if abs(self.board[i][j]) == abs(self.board[i + 1][j - 1]) == abs(self.board[i + 2][j - 2]) == 2:
                        continue
                    color = 1 if self.board[i][j] > 0 else -1  # get color
                    self.pieces[color][color * 2] += 3  # increment the cat count for this color
                    self.board[i][j] = self.board[i + 1][j - 1] = self.board[i + 2][j - 2] = 0
                    return True
        return False    
    
    def checkPromotion(self):
        if self.findThreeInRowHorizontal() or self.findThreeInRowVertical() or self.findThreeInRowMainDiagonals() or self.findThreeInRowMainAntiDiagonals():
            return True
        else:
            return False
        
    def findThreeCatsInRowHorizontal(self, color):
        for row in self.board:
            for i in range(4):
                if row[i] == row[i + 1] == row[i + 2] == color * 2:
                    return True
        return False

    def findThreeCatsInRowVertical(self, color):
        for j in range(6):
            for i in range(4):
                if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == color * 2:
                    return True
        return False

    def findThreeCatsInRowMainDiagonals(self, color):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == color * 2:
                    return True
        return False    

    def findThreeCatsInRowMainAntiDiagonals(self, color):
        for i in range(4):
            for j in range(2, 6):
                if self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == color * 2:
                    return True
        return False  

    def is_win(self, color):
        # Check horizontal, vertical and both diagonal directions
        if self.findThreeCatsInRowHorizontal(color) or \
            self.findThreeCatsInRowVertical(color) or \
            self.findThreeCatsInRowMainDiagonals(color) or \
            self.findThreeCatsInRowMainAntiDiagonals(color):
            return True

        # check for eight cats of the same color on the board
        flat_board = [item for sublist in self.board for item in sublist]
        if flat_board.count(color * 2) == 8:
            return True

        # no win condition satisfied
        return False