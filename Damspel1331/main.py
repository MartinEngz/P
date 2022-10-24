# ATT GÖRA
    # FORTSÄTT KOMMENTERA

    # menu.py & andra filer
        # modularisera pygame utskrifter. t ex att skriva text på brädet. Blir mycket "kodupprepning"
        # printa någonstans på skärmen vems tur det är ("Current turn: OPPONENT/PLAYER")
        # 

    # B-uppgift:
        # botens moves: tech with tim 10:00
        #
        # skapa klassen Player??
        # consider using research pygame.time.delay
        #
        # draw two radio buttons for playing against a bot or not (Constants attribute OPPONENT)
        # caption: BOT OR NOT (options BOT, NOT)
        # NOT checked by default (these will be static buttons until later)

import pygame
from checkers.constants import Constants
from checkers.game import Game
from checkers.menu import Menu
from checkers.timer import Timer

def get_row_col_from_mouse(pos):
    """
    Converts x- and y-coordinates from mouse click on pygame window to corresponding 
    row and column on the checker board.
        Parameters:
            pos: tuple
                Tuple containg x- and y-coordinates to be converted.
        Output:
            row, col: int, int
    """
    x, y = pos
    row = y // Constants.SQUARE_SIZE
    col = x // Constants.SQUARE_SIZE
    return row, col

def main():
    """
    Main function of the game. Here the pygame workspace is defined and instances of the 
    game-necessary classes Game, Timer and Menu are initialized. The main function also
    contains the while-loop of the game.
    """
    FPS = 60
    WINDOW = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption('Checkers')
    pygame.init()

    clock = pygame.time.Clock()
    game = Game(WINDOW)
    timer = Timer()    
    menu = Menu(WINDOW, game=game, timer=timer)

    run = True
    while run:
        clock.tick(FPS)
        timer.update_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < Constants.SQUARE_SIZE*Constants.COLS and pos[1] < Constants.SQUARE_SIZE*Constants.ROWS:
                    row, col = get_row_col_from_mouse(pos)
                    
                    if not game.selected:
                        game.select_piece(row, col)
                    else:
                        if game.has_skipped:
                            game.select_move(row, col) 
                        else:
                            game.select_piece(row,col) 
                            game.select_move(row,col) 
                    if game.has_completed_move == True: 
                        game.change_turn()

                else:
                    menu.select(pos)
        
        game.update()
        menu.update() 

    pygame.quit()


if __name__ == '__main__':
    main()