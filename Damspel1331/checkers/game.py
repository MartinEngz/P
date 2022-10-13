# Vilken funktionalitet tillför return True/return False på raderna 37-38 och 47-49

import pygame
from .board import Board
from .constants import Constants

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Constants.WHITE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
        #     return True
        # return False

    def _move(self, row, col):
        if (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        # else: 
        #     return False
        # return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, Constants.BLUE, (col * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2, row * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2), 15) # Change blue size to fit all board sizes

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Constants.RED:
            self.turn = Constants.WHITE
        else:
            self.turn = Constants.RED
        