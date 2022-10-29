import pygame
from checkers.constants import Constants
from checkers.game import Game
from checkers.menu import Menu
from checkers.timer import Timer
from checkers.bot import BotMover

def main():
    """
    Main function of the game. The pygame workspace is defined and instances of the 
    game-necessary classes Game, Timer and Menu are initialized. The main function also
    contains the while-loop of the game.
    """
    pygame.init()
    WINDOW = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption('Checkers DD1331')

    timer = Timer()    
    game = Game(WINDOW)
    menu = Menu(WINDOW, game=game, timer=timer)

    run = True
    while run:
        timer.update_time()

        if Constants.BOT_ACTIVE and game.turn == Constants.OPPONENT_COLOR and not game.board.winner():
            BotMover(game)
            game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if board_is_clicked(pos):
                    row, col = get_row_col_from_mouse(pos)
                    if not game.selected_piece:
                        game.select_piece(row, col)
                    else:
                        if game.skipped_pieces:
                            game.select_move(row, col) 
                        else:
                            game.select_piece(row,col) 
                            game.select_move(row,col) 
                    if game.has_completed_turn == True: 
                        game.change_turn()
                else:
                    menu.select(pos)

        game.update()
        menu.update() 

    pygame.quit()



def board_is_clicked(pos):
    """
    Given x- and y-coordinates from mouse click on pygame window, checks whether the click was inside 
    checker board or not.

    Parameters:
        pos: tuple[int, int]
            Tuple containg x- and y-coordinates.

    Output:
        bool
            If click was inside checker board, return True. If not, return False.

    """
    if pos[0] < Constants.SQUARE_SIZE*Constants.COLS and pos[1] < Constants.SQUARE_SIZE*Constants.ROWS:
        return True
    else:
        return False

def get_row_col_from_mouse(pos):
    """
    Converts x- and y-coordinates from mouse click on pygame window to corresponding 
    row and column on the checker board.
        Parameters:
            pos: tuple[int, int]
                Tuple containg x- and y-coordinates to be converted.
        Output:
            row, col: int, int
                Row and column of the square that was clicked.
    """
    x, y = pos
    row = y // Constants.SQUARE_SIZE
    col = x // Constants.SQUARE_SIZE
    return row, col
    

if __name__ == '__main__':
    main()