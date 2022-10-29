import random
import pygame

from .piece import Piece
from .constants import Constants

class BotMover:
    """
    BotMover instances are initialized in the while-loop of the main function if the bot has been activated in the 
    in-game menu, it is the opponent's turn and the game is yet to have a winner. 

    BotMover looks at the current state of the board and executes the longest move possible. 
    """
    def __init__(self, game):
        """
        Parameters:
            game: Game object
                The current state of the game is passed to the constructor upon initializing 
                a BotMover instance.
        Instance variables initialized:
            self.game: see game parameter.
        """
        self.game = game
        self.move_longest_possible()
        

    def move_longest_possible(self):
        """
        Finds the piece/pieces that can make the longest possible moves. If there are multiple pieces that can
        make equally long moves, a single piece is randomized out of these. If the chosen piece can make multiple
        moves of the same longest length, a single move is randomized out of these. Finally, this move is executed. 
        """
        longest_path_pieces = self.get_longest_path_pieces()
        piece_to_move = self.randomize_piece_to_move(longest_path_pieces)
        longest_move = self.randomize_longest_move(piece_to_move)
        self.move(piece_to_move, longest_move)

    def get_longest_path_pieces(self) -> list:
        """
        Given the current state of the board, returns a list of the opponent teams' pieces that can make the longest
        possible moves.

        Output:
            longest_path_pieces: list
                List of the opponent teams' pieces that can make the longest possible moves. 
        """
        longest_path_pieces = []
        longest_move_length = 0 # measured in amound of pieces skipped during the move
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.game.board.get_piece(row, col)
                if piece != 0 and piece.color == Constants.OPPONENT_COLOR:
                        moves_of_current_piece = self.game.board.get_valid_moves(piece, recursive_skipping=True)
                        if not moves_of_current_piece:
                            continue
                        for (target_row, target_col) in moves_of_current_piece:
                            if len(moves_of_current_piece[target_row, target_col]) == longest_move_length and piece not in longest_path_pieces:
                                longest_path_pieces.append(piece)
                            elif len(moves_of_current_piece[target_row, target_col]) > longest_move_length:
                                longest_path_pieces = [piece]
                                longest_move_length = len(moves_of_current_piece[target_row, target_col])
        return longest_path_pieces

    def randomize_piece_to_move(self, longest_path_pieces) -> Piece:
        """
        Randomizes which piece to move out of the pieces that can make move the longest possible.

        Parameters:
            longest_path_pieces: list
                List of the opponent teams' pieces that can make the longest possible moves.

        Output:
            piece_to_move: Piece
                Randomized piece valid to make the longest possible move.

        """
        amount_valid_pieces = len(longest_path_pieces)
        randomized_piece_index = random.randint(0, amount_valid_pieces-1)
        piece_to_move = longest_path_pieces[randomized_piece_index]
        return piece_to_move

    def randomize_longest_move(self, piece_to_move) -> dict[tuple[int, int]: list[Piece]]:
        """
        Randomizes a single longest moves out of possible longest moves. 
        
        Example: 
        If the randomized piece can make multiple longest moves, one of these moves is returned at
        random.

        Parameters:
            piece_to_move: Piece
                Randomized piece valid to make the longest possible move.

        Output:
            longest_move: dict[tuple[int, int]: list[Piece]]
                Longest possible move the parameter piece can make. Randomized if multiple options.
        
        """
        # Finds longest moves. Note that this can be multiple moves as more than one valid move can 
        # be of a certain length.
        valid_moves = self.game.board.get_valid_moves(piece_to_move, recursive_skipping=True)
        longest_moves = {}
        longest_move_length = 0
        for (target_row, target_col) in valid_moves:
            if len(valid_moves[(target_row, target_col)]) == longest_move_length:
                longest_moves.update({(target_row, target_col): valid_moves[target_row, target_col]})
            elif len(valid_moves[target_row, target_col]) > longest_move_length:
                longest_moves = {(target_row, target_col): valid_moves[target_row, target_col]}
                longest_move_length = len(valid_moves[target_row, target_col])
        # Randomizes a move out of the possible longest moves
        amount_longest_moves = len(longest_moves)
        randomized_move_index = random.randint(0, amount_longest_moves-1)
        for idx, (target_row, target_col) in enumerate(longest_moves):
            if idx == randomized_move_index:
                randomized_move = {(target_row, target_col): longest_moves[target_row, target_col]}
        longest_move = randomized_move

        return longest_move

    def move(self, piece_to_move, longest_move):
        """
        Calls board class methods for moving piece on the board and removing any skipped pieces.

        Parameters:
            piece_to_move: Piece
            longest_move: dict[tuple[int, int]: list[Piece]]
                Dictionary where key represents target square and value is a list of skipped pieces.
        """
        
        target_row, target_col = list(longest_move.keys())[0]
        if len(longest_move[target_row, target_col]) == 0:
            pygame.time.delay(1000)
            self.game.board.move(piece_to_move, target_row, target_col)
            skipped_piece = longest_move[target_row, target_col]
            if skipped_piece:
                self.game.board.remove(skipped_piece)
        else:
            for _, skipped_piece in enumerate(longest_move[target_row, target_col]):
                pygame.time.delay(1000)
                valid_skips = self.game.board.get_valid_skips(piece_to_move)
                skip_target_row, skip_target_col = list(valid_skips.keys())[list(valid_skips.values()).index([skipped_piece])]
                self.game.board.move(piece_to_move, skip_target_row, skip_target_col)
                self.game.board.remove([skipped_piece])

                self.game.update()
