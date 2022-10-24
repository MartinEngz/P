import pygame
from .constants import Constants
from .piece import Piece

class Board():
    """
    The Board class creates and operates the board data structure.
    """
    def __init__(self):
        """
        Instance variables initialized and methods called in constructor:
            self.player_left: int
                Number of pieces of the player's color left in the game.
            self.opponent_left: int
                Number of pieces of the opponent's color left in the game.
            self.create_board()
                Creates matrix representation of the board.
        """
        self.create_board()
        self.player_left = self.opponent_left = (Constants.COLS//2) * (Constants.ROWS//2-1)
    
    def create_board(self):
        """
        Creates the matrix representation of the board. Pieces are initialized and placed in
        a checker board pattern. An element of the matrix representing a square with a 
        piece has its value set to an object of the class Piece. The value of an empty square  
        is set to zero.
        
        Instance variables created or modified:
            self.board: list (matrix of size Constants.ROWS x Constants.COLS)
                Data structure representation of board with elements either set to zero or a
                Piece-object.
        """
        self.board = []
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < Constants.ROWS // 2 - 1:
                        self.board[row].append(Piece(row, col, Constants.OPPONENT_COLOR))
                    elif row > Constants.ROWS // 2:
                        self.board[row].append(Piece(row, col, Constants.PLAYER_COLOR))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self, window):
        """
        Draws the squares of the checker board on the Pygame window.

        Parameters:
            window: Pygame Surface object
                Pygame window to draw checker board on.
        """
        for row in range(Constants.ROWS):
            for col in range(row % 2, Constants.COLS, 2):
                pygame.draw.rect(window, Constants.RED, (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))
            for col in range(row % 2 - 1, Constants.COLS, 2):
                pygame.draw.rect(window, Constants.BLACK, (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))


    def move(self, piece, row, col):
        """
        'Moves' a Piece object by switching values of source and destination square of a moving piece.
        Eg. a piece moves from square A3 to the empty square B4. After the move, the square A3 is now
        an empty square and B4 is hosting a piece. If a piece moves into either the first or the last
        row, it is promoted to king.

        Parameters:
            piece: object of class Piece
                Piece to move.
            row, col: int, int
                Row and column of the destination square.
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.update_position(row, col)
        if row == Constants.ROWS-1 or row == 0:
            piece.make_king()


    def get_piece(self, row, col):
        """
        Returns value stored in the row:th row and the col:th column of the board matrix. 
        """
        return self.board[row][col]

    
    def draw(self, win):
        """
        Draws the board by calling self.draw_squares() and the pieces by iterating over all values
        of the board matrix and calling the self.piece.draw() method for every element which contains a
        piece.
        
        Parameters:
            window: Pygame Surface object
                Pygame window to draw checker board and pieces on.
        """ 
        self.draw_squares(win)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.get_piece(row, col)
                if piece != 0:
                    piece.draw(win)

    def remove(self, skipped_pieces):
        """
        Sets the value of skipped pieces' host squares to zero in the board matrix. The counter
        of how many pieces the corresponding participant has left is updated there after.

        Parameters:
            skipped_pieces: list
                List of skipped piece objects. 
        """
        for piece in skipped_pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Constants.PLAYER_COLOR:
                    self.player_left -= 1
                elif piece.color == Constants.OPPONENT_COLOR:
                    self.opponent_left -= 1
    
    def winner(self):
        """
        If one of the participants doesn't have any pieces left the other one wins. The winner is
        returned as a string.
        """
        if self.player_left == 0:
            return "OPPONENT WINS"
        elif self.opponent_left == 0:
            return "PLAYER WINS"
        return None

    def print_winner(self, window):
        """
        Prints the winner on the middle of the Pygame window.

        Parameters:
            window: Pygame Surface object
                Pygame window to draw checker board and pieces on.
        """
        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render(self.winner(), True, Constants.YELLOW)
        textRect = text.get_rect()
        textRect.center = (Constants.WIDTH//2, Constants.HEIGHT//2)
        window.blit(text, textRect)

    def get_valid_steps(self, piece):
        """
        Given a piece and with respect to the current state of the board, returns dictionary of its valid steps 
        (i.e moves that do not skip any opponent piece). This dictionary is a subset of the dictionary 
        valid_paths from self.get_valid_paths-method.

        Parameters:
            piece: Piece object
                The piece we want to find valid steps for.

        Output:
            valid_steps: dictionary
                Dictionary with keys of tuples, e.g (row, col), representing the destination row and column
                of the valid steps. If the input piece can make valid steps, this dictionary will not be empty.
        """
        valid_steps = {}
        valid_paths = self.get_valid_paths(piece)
        for (row, col) in valid_paths:
            if len(valid_paths[(row, col)]) == 0:
                valid_steps.update({(row, col): valid_paths[(row, col)]})
        return valid_steps

    def get_valid_skips(self, piece):
        """
        Given a piece and with respect to the current state of the board, returns dictionary of its valid skips 
        (i.e moves that skip an opponent piece). This dictionary is a subset of the dictionary valid_paths from
        self.get_valid_paths-method.

        Parameters:
            piece: Piece object
                The piece we want to find valid skips for.

        Output:
            valid_steps: dictionary
                Dictionary with keys of tuples, e.g (row, col), representing the destination row and column
                of the valid skips. The value of a key will be a list containing the opponent piece that
                was skipped over in order to move to the destination. 
        """
        valid_skips = {}
        valid_paths = self.get_valid_paths(piece)
        for (row, col) in valid_paths:
            if len(valid_paths[(row, col)]) == 1:
                valid_skips.update({(row, col): valid_paths[(row, col)]})
        return valid_skips
      
  
    def get_valid_paths(self, piece):
        """
        Returns a dictionary whose keys are all possible destination squares (row, col) and intermediary squares
        an input piece can move into during one turn. The value of a key will be a list whose elements are all 
        piece object the input piece has to skip over in order to reach the key destination square.
        
        Parameters:
            piece: Piece object
                Piece to find valid paths for.

        Output:
            valid_paths: dictionary
                Dictionary of all valid paths. Key is destination square and value is list of skipped pieces.  
        """
        valid_paths = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == Constants.PLAYER_COLOR or piece.king:
            valid_paths.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left)) 
            valid_paths.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        if piece.color == Constants.OPPONENT_COLOR or piece.king:
            valid_paths.update(self._traverse_left(row+1, min(row+3, Constants.ROWS), 1, piece.color, left))
            valid_paths.update(self._traverse_right(row+1, min(row+3, Constants.ROWS), 1, piece.color, right))
        
        # Propsosal for longest move finder "compatible with consecutive king moves in different
        # directions".
        # if last or first row in key_x of valid_paths:
        #     run traverse algo in both directions
        #     valid_paths.update(king_paths)

        return valid_paths

    def _traverse_left(self, start, stop, step, color, left_col, skipped=[]):
        """
        Algorithm for exploring the left diagonal for valid paths. If an opponent piece is skipped within the
        first move (same as the previous piece was an opponent piece), the algorithm calls self._traverse_left()
        and self._traverse_right() to check for possible double jumps. Then the same methods are called again
        to check for triple, quadruple, quintiple jumps etc. if possible.

        ** CONSIDER HAVING PIECE AS A PARAMETER FOR _TRAVERSE METHOD** and write logic depending on if the piece
        is king or not
        """
        moves = {}
        previous_opp_piece = []
        for row_i in range(start, stop, step):
            if left_col < 0:
                break
            
            current_diagonal_piece = self.board[row_i][left_col]
            if current_diagonal_piece == 0:
                if skipped and not previous_opp_piece:
                    break
                elif skipped:
                    moves[(row_i, left_col)] = previous_opp_piece + skipped
                else:
                    moves[(row_i, left_col)] = previous_opp_piece

                if previous_opp_piece: # this if-block basically checks if double or triple jumps are possible, my program must ultimately expand to quadruple and quintiple jumps as well if the board is 12x12
                    if step == -1:
                        stop_from_row_i = max(row_i - 3, -1)
                    else:
                        stop_from_row_i = min(row_i + 3, Constants.ROWS)
                    moves.update(self._traverse_left(row_i+step, stop_from_row_i, step, color, left_col-1, skipped=previous_opp_piece+skipped))
                    moves.update(self._traverse_right(row_i+step, stop_from_row_i, step, color, left_col+1, skipped=previous_opp_piece+skipped))
                    
                break
            elif current_diagonal_piece.color == color:
                break
            else:
                previous_opp_piece = [current_diagonal_piece]

            left_col -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right_col, skipped=[]):
        moves = {}
        previous_opp_piece = []
        for row_i in range(start, stop, step):
            if right_col >= Constants.COLS:
                break
            
            current_diagonal_piece = self.board[row_i][right_col]
            if current_diagonal_piece == 0:
                if skipped and not previous_opp_piece:
                    break
                elif skipped:
                    moves[(row_i, right_col)] = previous_opp_piece + skipped
                else:
                    moves[(row_i, right_col)] = previous_opp_piece

                if previous_opp_piece: # this if-block basically checks if double or triple jumps are possible, my program must ultimately expand to quadruple and quintiple jumps as well if the board is 12x12
                    if step == -1:
                        stop_from_row_i = max(row_i - 3, -1)
                    else:
                        stop_from_row_i = min(row_i + 3, Constants.ROWS)
                    
                    moves.update(self._traverse_left(row_i+step, stop_from_row_i, step, color, right_col-1, skipped=previous_opp_piece+skipped))
                    moves.update(self._traverse_right(row_i+step, stop_from_row_i, step, color, right_col+1, skipped=previous_opp_piece+skipped))
                    
                break
            elif current_diagonal_piece.color == color:
                break
            else:
                previous_opp_piece = [current_diagonal_piece]

            right_col += 1

        return moves