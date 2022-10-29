import pygame
from .board import Board
from .constants import Constants


class Game:
    """
    Initialized in main function of main file.

    The Game module manages higher-level attributes of the game. These include, but are not limited to, 
    keeping track of whose turn it is, which piece is selected and whether the selected piece has 
    completed its move or not.
    """
    def __init__(self, window):
        """
        Instance variables initialized and methods called in constructor:
            self.window: Pygame Surface object
                Pygame window to draw valid moves, board and pieces on.
            self._set_start_attributes()
                Sets initial values of attributes for a new game instance.
        """
        self.window = window
        self._set_starting_attributes()

    def update(self):
        """
        Calls all draw methods for displaying the current state of the game on the Pygame window.
        Thereafter calls Pygame method for updating Pygame display screen.
        """
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        if self.board.winner():
            self.board.print_winner(self.window)
        pygame.display.update()

    def _set_starting_attributes(self):
        """
        Sets initial values of attributes for a new game instance. The purpose of this being an own
        method is to call it not only from the constructor, but also from self.reset() which is called
        from the restart button in the menu.

        Instance variables set or modified:
            self.selected_piece: NoneType
                Will be set to a piece object if a valid piece.
            self.skipped_pieces: NoneType
                Will be set to list of skipped piece objects to remove.
            self.: bool
                Is set to true when a piece can not or is not allowed to move any further. Is condition
                for changing turn.
            self.board: Board type object
                See comments in the board module for further documentation.
            self.turn: tuple
                In this implementation of checkers "PLAYER" always makes the first move.
            self.valid_moves: dictionary
                Keys are tuples representing destination square of a move. Their values are lists
                of piece objects that have been skipped over.
        """
        self.selected_piece = None
        self.skipped_pieces = [] 
        self.has_completed_turn = False
        self.board = Board()
        self.turn = Constants.PLAYER_COLOR
        self.valid_moves = {}

    def reset(self):
        """
        This method is called from the restart button in the menu to reset the state of the game.  
        """
        self._set_starting_attributes()

    def select_piece(self, row, col):
        """
        Selects piece on the board from input mouse click.

        Parameters:
            row, col: int, int
                Row and column of the square the mouse clicked.

        Initialized/modified instance variables:
            self.selected_piece: Piece object
                Selected piece to be moved.
            self.valid_moves: dictionary
                If a valid piece is selected its valid moves will be stored in the dictionary by the
                format described in the constructor comments.
        """
        piece = self.board.get_piece(row, col)
        # The requirement "om spelaren kan skippa, måste han skippa" is dealt with in self.get_valid_pieces
        # and the logical structure in the main function. 
        valid_pieces = self.get_valid_pieces()
        if piece in valid_pieces:
            self.selected_piece = piece
            if self.board.get_valid_skips(self.selected_piece):
                self.valid_moves = self.board.get_valid_skips(self.selected_piece) 
            else:
                self.valid_moves = self.board.get_valid_steps(self.selected_piece)

    def get_valid_pieces(self):
        """
        Iterates through all squares of the board. Returns List of all pieces that can make valid skips.
        If there are no such pieces, a list of all pieces that can make valid steps are returned
        instead. 
        
        Output:
            valid_pieces_for_skip: list
                List of all pieces that can make valid skips.
            valid_pieces_for_step: list
                If not valid_pieces_for_skip, a list of valid pieces that can take a step is returned.
                returned. 
        """
        valid_pieces_for_skip, valid_pieces_for_step = [], []

        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn:
                    if self.board.get_valid_skips(piece):
                        valid_pieces_for_skip.append(piece)
                    if self.board.get_valid_steps(piece):
                        valid_pieces_for_step.append(piece)
        if valid_pieces_for_skip:
            return valid_pieces_for_skip
        else:
            return valid_pieces_for_step

    def select_move(self, row, col):
        """
        Selects valid move from input mouse click.

        Parameters:
            row, col: int, int
                Row and column of the square the mouse clicked.

        Modified instance variables: 
            self.skipped_pieces: list
                List contains piece objects that were skipped over by the selected move.
            self.valid_moves: dictionary
                Key is tuple representing destination square. Value is list of piece objects that are skipped
                by moving into destination square.
            self.has_completed_turn: bool
                Is set to True when a piece has no more valid moves. This is boolean serves as the logical
                condition for changing turns. 
        """
        if (row, col) in self.valid_moves:
            self.board.move(self.selected_piece, row, col)
            self.skipped_pieces = self.valid_moves[(row, col)]
            if self.skipped_pieces:
                self.board.remove(self.skipped_pieces)
                self.valid_moves = self.board.get_valid_skips(self.selected_piece)
                if not self.valid_moves:
                    self.has_completed_turn = True
            else:
                self.has_completed_turn = True

    def change_turn(self):
        """
        Sets game object attributes such that the next player can play.

        Modified instance variables:
            self.turn: tuple
                RGB-representation of the color of the player who the turn passes to.           
            self.selected_piece: NoneType
                Resets to None such that one player can not make a move with the other player's
                piece.
            self.skpped_pieces: list
                Resets to empty list of skipped pieces.
            self.has_completed_turn: bool
                This boolean is the logical condition for changing turns. If it is not reset, the game will
                endlessly change turn.
            self.valid_moves: dictionary
                Resets to empty dictionary such that the opponent player can not make a valid move into a
                a valid move of the previous player.
        """
        if self.turn == Constants.PLAYER_COLOR:
            self.turn = Constants.OPPONENT_COLOR
        else:
            self.turn = Constants.PLAYER_COLOR
        self.selected_piece = None
        self.skipped_pieces = []
        self.has_completed_turn = False
        self.valid_moves = {}

    def draw_valid_moves(self, moves):
        
        """
        Retrieves row and column of a valid move stored as key in the self.valid.moves dictionary.
        Draws a blue circle at the corresponding location on the Pygame window. 

        Parameters:
            moves: dictionary
                Dictionary of valid moves (self.valid_moves).
        """
        for move in moves:
            row, col = move
            radius = int(Constants.SQUARE_SIZE//2 * .4)
            pygame.draw.circle(self.window, Constants.BLUE, (col * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2, row * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2), radius=radius) 

