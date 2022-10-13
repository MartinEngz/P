import pygame
from .constants import Constants
from .piece import Piece

class Board():
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_left = self.white_left = (Constants.COLS//2) * (Constants.ROWS//2-1)
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(Constants.GRAY) 
        for row in range(Constants.ROWS):
            for col in range(row % 2, Constants.COLS, 2):
                pygame.draw.rect(win, Constants.RED, (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))
            for col in range(row % 2 - 1, Constants.COLS, 2):
                pygame.draw.rect(win, Constants.BLACK, (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))


    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        

        if row == Constants.ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == Constants.WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < Constants.ROWS // 2 - 1:
                        self.board[row].append(Piece(row, col, Constants.WHITE))
                    elif row > Constants.ROWS // 2:
                        self.board[row].append(Piece(row, col, Constants.RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Constants.RED:
                    self.red_left -= 1
                elif piece.color == Constants.WHITE:
                    self.white_left -= 1
    
    def winner(self):
        if self.white_left <= 0:
            return "RED WINS"
        elif self.red_left <= 0:
            return "WHITE WINS"
        return None


    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == Constants.RED or piece.king:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left)) 
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        if piece.color == Constants.WHITE or piece.king:
            moves.update(self._traverse_left(row+1, min(row+3, Constants.ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row+1, min(row+3, Constants.ROWS), 1, piece.color, right))
        
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last: # this if-block basically checks if double or triple jumps are possible, my program must ultimately expand to quadruple and quintiple jumps as well if the board is 12x12
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, Constants.ROWS)

                    if skipped:
                        moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last+skipped))
                        moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last+skipped))
                    else:
                        moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))

                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= Constants.COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last: # this if-block basically checks if double or triple jumps are possible, my program must expand to quadruple and quintiple jumps as well if the board is 12x12
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, Constants.ROWS)
                    if skipped:
                        moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last+skipped))
                        moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last+skipped))
                    else:
                        moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))

                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves