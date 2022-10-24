import pygame
from .constants import Constants

class Piece():
    def __init__(self, row, col, color):
        """
        Piece objects are the value of elements of the matrix representation of the board that
        contain pieces.

        Instance variables initialized in the constructor:
            self.row, self.col: int, int
                row and col represent the position of the piece on the checker board.
            self.color: tuple
                Tuple representing color of the piece in RGB-format. All colors in 
                this program are passed from the checkers.constants module.
            self.king: bool
                A piece being a king or not rules whether a piece is allowed to move
                in one or both directions on the board. 
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.calc_pos()

    def calc_pos(self):
        """
        Inverse function of get_row_col_from_mouse function in main function in main file. 
        Drawing circles with Pygame requires the x- and y-coordinates on the Pygame window
        where a piece is to be drawn.

        Instance variables initialized/modified:
            self.x, self.y: int, int
                x- and y-coordinates corresponding to center of the square containing
                the Piece object on the Pygame window.
        """
        self.x = Constants.SQUARE_SIZE * self.col + Constants.SQUARE_SIZE // 2
        self.y = Constants.SQUARE_SIZE * self.row + Constants.SQUARE_SIZE // 2

    def make_king(self):
        """
        A piece is promoted to king when it reaches the last row of the opposite side of 
        the board. This method is called in the move method of the class Board.
        
        Instance variables modified:
            self.king: bool
        """
        self.king = True

    def draw(self, window):
        """
        Method responsible for drawing the pieces on the Pygame window. If a Piece object
        has been promoted to king, a crown is drawn on top of its circle representation in 
        Pygame. The radius of the circle is calculated to properly scale as the size of the
        board is changed.
        
        Parameters:
            window: Pygame Surface object
                Pygame window to draw piece representation on.
        """
        radius = int(Constants.SQUARE_SIZE//2 * 0.7)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius=radius)
        if self.king:
            window.blit(Constants.CROWN, (self.x - Constants.CROWN.get_width()//2, self.y - Constants.CROWN.get_height()//2))

    def update_position(self, row, col):
        """
        This method updates the row and column as well as the x and y salues of the Piece instance such that the 
        corresponding circle is drawn in the position where the piece object moved.
            
        Parameters:
            row: int
                Row of destination square the piece is moving to.
            col: int
                Column of destination square the piece is moving to.
        """
        self.row = row
        self.col = col
        self.calc_pos()
        