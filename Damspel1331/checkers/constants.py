import pygame

class Constants:
    def __init__(self):
        self.WIDTH = 700
        self.HEIGHT = 800
        self.ROWS, self.COLS = 10, 10
        self.SQUARE_SIZE = self.WIDTH // self.COLS

        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GRAY = (122, 122, 122)
        self.YELLOW = (255, 255, 0)

        self.CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25))

Constants = Constants()