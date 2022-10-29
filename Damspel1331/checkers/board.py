import pygame
from .constants import Constants
from .piece import Piece

class Board():
    """
    Initialized from _set_starting_attributes() method in Game class instance. 
    
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

    def get_valid_steps(self, piece) -> dict[tuple: list]:
        """
        Given a piece and with respect to the current state of the board, returns dictionary of its valid steps 
        (i.e moves that do not skip any opponent piece). This dictionary is a subset of the dictionary 
        valid_moves from self.get_valid_moves-method.

        Parameters:
            piece: Piece object
                The piece we want to find valid steps for.

        Output:
            valid_steps: dictionary
                Dictionary with keys of tuples, e.g (row, col), representing the destination row and column
                of the valid steps. If the input piece can make valid steps, this dictionary will not be empty.
        """
        valid_steps = self.get_valid_moves(piece, get_skips=False)
        return valid_steps

    def get_valid_skips(self, piece) -> dict[tuple: list]:
        """
        Given a piece and with respect to the current state of the board, returns dictionary of its valid skips 
        (i.e moves that skip an opponent piece). This dictionary is a subset of the dictionary valid_moves from
        self.get_valid_moves-method.

        Parameters:
            piece: Piece object
                The piece we want to find valid skips for.

        Output:
            valid_steps: dictionary
                Dictionary with keys of tuples, e.g (row, col), representing the destination row and column
                of the valid skips. The value of a key will be a list containing the opponent piece that
                was skipped over in order to move to the destination. 
        """
        valid_skips = self.get_valid_moves(piece, get_steps=False)
        return valid_skips
      
  
    def get_valid_moves(self, piece, get_steps=True, get_skips=True, recursive_skipping=False) -> dict[tuple: list]:
        """
        Returns a dictionary whose keys are all possible destination squares (row, col) and intermediary squares
        an input piece can move into during one turn. The value of a key will be a list whose elements are all 
        piece object the input piece has to skip over in order to reach the key destination square.
        
        Parameters:
            piece: Piece object
                Piece to find valid paths for.
            get_steps: bool 
                OPTIONAL. Default value: True. Whether get_valid_moves() method is to consider moves of step size 1.
            get_skips: bool
                OPTIONAL. Default value: True. Whether get_valid_moves() method is to consider moves of step size 2.
            recursive_skipping: bool
                OPTIONAL. Default value: False. Boolean condition if recursion is to be used. As this is only desired 
                for the bot calculating its longest possible move, recursion is set to False by default.

        Output:
            valid_moves: dictionary
                Dictionary of all valid paths. Key is destination square and value is list of skipped pieces.  
        """
        valid_moves = {}
        if get_steps == True:
            valid_moves.update(self.explore_valid_moves(piece, piece.row, piece.col, 1))
        if get_skips == True:
            valid_moves.update(self.explore_valid_moves(piece, piece.row, piece.col, 2, recursive_skipping=recursive_skipping))

        return valid_moves

    def explore_valid_moves(self, piece, current_row, current_col, step_size, skip_path=[], recursive_skipping=False):
        """
        Explores valid moves for a piece by examining its four surrounding diagonal squares at a sitance of [step_size]
        diagnonal squares away. If consecutive moves during the same turn is to be examined, the method calls itself
        recursively. 

        Parameters:
            piece: Piece object
                Piece to find valid moves for.
            current_row: int
                Starting row from which we want to find valid moves from.
            current_col: int
                Starting column from which we want to find valid moves from.
            step_size: int
                Distance a piece moves vertically respectively horisontally during a single move. A step has a step size
                of 1 whereas a skip has a step size of 2. NOTE: Method only compatible with step_size 1 or 2.
            skip_path: list
                OPTIONAL. Default value: []. When the method calls itself recursively, keeping track of
                which pieces has been skipped over is necessary in order to prevent the program from endlessly skipping
                the same piece until the system recursion limit is met.
            recursive skipping: bool
                OPTIONAL. Default value: False. Whether the move finder method is to consider consecutive skip moves during 
                the same turn. This is used by the BotMover class in order to calculate the longest possible move.

        Output:
            valid_moves: dictionary
                Dictionary of all valid paths. Key is destination square and value is list of skipped pieces.  
        """


        up, down, left, right = [x + y * step_size for x in [current_row, current_col] for y in [-1, 1]]

        valid_moves = {}

        for target_row in [up, down]:
            for target_col in [left, right]:
                if not self.is_valid_move(piece, current_row, current_col, target_row, target_col, step_size):
                    continue
                else:
                    if step_size == 1:
                        valid_moves[target_row, target_col] = []
                    else: # If step_size is not 1, step_size is 2. Then we check for skip moves. 
                        skipped_row = (current_row + target_row) // 2
                        skipped_col = (current_col + target_col) // 2
                        if self.get_piece(skipped_row, skipped_col) in skip_path:
                            continue
                        new_skip_path = skip_path.copy()
                        new_skip_path.append(self.get_piece(skipped_row, skipped_col))
                        valid_moves[(target_row, target_col)] = new_skip_path
                        if recursive_skipping == True: # Recursive skipping is used by BotMover instance for calculating longest possible move.
                            valid_moves.update(self.explore_valid_moves(piece, target_row, target_col, 2, new_skip_path, recursive_skipping=True))
        return valid_moves
 
    def is_valid_move(self, piece, current_row, current_col, target_row, target_col, step_size) -> bool:
        """
        Set of logical conditions that has to be met in order for the move from current row and column to target
        row and column to be valid.

        Parameters:
            piece: Piece Object
                Piece to find valid moves for.
            current_row, current_col: int, int
                Current row and column where the piece is residing during the move. When the explore_valid_moves() 
                method is called recursively, current row and column is in most cases not equivalent with the piece
                object attributes piece.row and piece.col but a previous target row and target column.
            target_row, target_col: int, int
                Target row and column of the move being examined.
            step_size: int
                Distance a piece moves vertically respectively horisontally during a single move. A step has a step size
                of 1 whereas a skip has a step size of 2.
        
        Output:
            bool
                True if move is valid. False if it is not.

        """

        if not (piece.king or target_row == current_row + piece.direction * step_size):
            # invalid direction
            return False
        if not (0 <= target_row < Constants.ROWS and 0 <= target_col < Constants.COLS):
            return False
        target_square = self.get_piece(target_row, target_col)
        if target_square != 0:
            # target_square not empty
            return False
        # all base obstacle conditions are overcome, the skipping case logic remains:
        if step_size == 2:
            skipped_row = (current_row + target_row) // 2
            skipped_col = (current_col + target_col) // 2
            skipped_piece = self.get_piece(skipped_row, skipped_col)
            if skipped_piece == 0 or skipped_piece.color == piece.color:
                return False
        return True
