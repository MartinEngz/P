import pygame

class Constants:
    def __init__(self):
        """
        A collection of useful variables that are used in multiple other modules. An instance of this object is
        initilized module such that the same instance of the class might be modified and dynamically used
        between different modules. 

        Initialized instance variables:
            self.RED: tuple
                Used to draw color of red pieces and of red squares in Pygame window. Also used as a representation 
                of a team in logical statements. E.g if piece.color == Constants.PLAYER_COLOR: execute [action]
            self.WHITE: tuple
                Similar to self.RED
            self.BLACK: tuple
                Used to draw black board squares and clear window when starting a new game.
            self.GRAY: tuple
                Used to color menu boarders and radiobutton text
            self.YELLOW: tuple
                Colors timer, winner text and highlights selected radiobutton button.
            self.DARK_GRAY: tuple
                Colors timer caption and highlighted radiobutton choice text.
            self.WIDTH, self.HEIGHT: int, int
                Width and height of Pygame window.
            self.BOARD_SIZE: tuple
                Tuple representing board size in format (ROWS, COLUMNS)
            self.ROWS, self.COLS: int, int
                Amount of rows and columns retrieved from self.BOARD_SIZE tuple
            self.SQUARE_SIZE: int
                Size of board squares caluclated from given board width and amount of columns.
            self.PLAYER_COLOR: tuple
                PLAYER represents the player who starts the game with pieces on the lower rows of the board.
            self.OPPONENT_COLOR: tuple
                OPPONENT represents the player who starts the game with pieces on the upper rows of the board.
            self.BOT_ACITVE: boolean
                Boolean representation of whether the bot is active or not. 
            self.Crown: Pygame Surface (image)
                Image to be printed on top of pieces when they are promoted to king.
        """

        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (190, 190, 190)
        self.YELLOW = (255, 255, 0)
        self.DARK_GRAY = (50, 50, 50)

        self.WIDTH = 700
        self.HEIGHT = 800

        self.BOARD_SIZE = (8, 8)
        self.ROWS, self.COLS = self.BOARD_SIZE
        self.SQUARE_SIZE = self.WIDTH // self.COLS

        self.PLAYER_COLOR = self.WHITE
        self.OPPONENT_COLOR = self.RED

        self.BOT_ACTIVE = False

        self.CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25))
        

Constants = Constants()