import pygame

from .highscore import Highscore_manager
from .constants import Constants
from .radiobuttons import RadioButtons
 

class Menu:
    def __init__(self, window, game, timer):
        """
        The menu class serves as the user interface for selecting game options, displaying time and
        resetting the game during run time.

        Parameters:
            window: Pygame Surfance object
                window to draw menu on.
            game: Game object
                Game instance to be modified by selections in the menu.
            timer: Timer object
                Timer instance to display and return time from

        Instance variables:
            self.window: [see window parameter]
            self.game: [see game parameter]
            self.timer [see timer parameter]
            self.board_size_options: dictionary
                Dictionary of possible sizes for the board size.
            self.size_buttons: RadioButtons object
                The Radiobuttons objects draws functional radiobuttons on the Pygame window for board_size selection.
            self.color_options: dictionary
                Dictionary of possible color choices.
            self.color_buttons: RadioButtons object
                The Radiobuttons objects draws functional radiobuttons on the Pygame window for piece color selection.
            self.bot_options: dictionary
                Dictionary of bot alternatives represented as a boolean.
            self.bot_buttons: Radiobuttons object
                Functional radiobuttons for selecting to play against bot or not.
            self.has_updated_highscore: bool
                Functions as a logical gatekeeper for updating highscore.
            self.filename: str
                Path to file where highscore data will be written.
        """

        self.window = window
        self.game = game
        self.timer = timer
        self.board_size_options = {'8x8': (8, 8), '10x10': (10, 10), '12x12': (12, 12)}
        self.size_buttons = RadioButtons(window=self.window, caption='Board size:', options=self.board_size_options, default=Constants.BOARD_SIZE, top_left=(5, Constants.WIDTH+10))
        self.color_options = {'White': Constants.WHITE, 'Red': Constants.RED}
        self.color_buttons = RadioButtons(window=self.window, caption='Player color:', options=self.color_options, default=self.color_options['White'], top_left=(160, Constants.WIDTH+10)) 
        self.bot_options = {'Friend': 'Friend', 'Bot': 'Bot'}
        self.bot_buttons = RadioButtons(window=self.window, caption='Opponent:', options=self.bot_options, default=self.bot_options['Friend'], top_left=(450, Constants.WIDTH+10))
        self.has_updated_highscore = False
        self.filename = 'Damspel1331/checkers/highscore.txt'        

    def update(self):
        """
        Calls method for drawing all menu widgets and updates Pygame display. If the game has a winner, the time
        is written to a highscore txt file where times are sorted under each respective valid board size. 
        """
        self.draw_menu()
        pygame.display.update()
        if self.game.board.winner():
            if self.has_updated_highscore == False:
                new_score = self.set_time_format(self.timer.winner_time)
                Highscore_manager(self.filename, self.size_buttons.selected, new_score)
                self.has_updated_highscore = True            

    def select(self, pos):
        """
        Given input mouse coordinates, selects the corresponding menu widget and makes action
        thereafter.

        Parameters:
            pos: tuple (int, int)
                X- and y-coordinates from mouse click on Pygame window.

        Modified instance variables:
            self.size_buttons.selected: tuple
                Tuple representing selected board size (e.g (8, 8) or (12, 12)).
            self.color_buttons.selected: tuple
                Tuple representing selected piece color ((255, 0, 0) for red or (255, 255, 255) for white).
        """
        x, y = pos
        if self.timer_is_clicked(x, y):
            self.restart()
        if self.size_buttons.get_clicked_button(x, y):
            clicked_button = self.size_buttons.get_clicked_button(x, y)
            self.size_buttons.selected = clicked_button
        if self.color_buttons.get_clicked_button(x, y):
            clicked_button = self.color_buttons.get_clicked_button(x, y)
            self.color_buttons.selected = clicked_button
        if self.bot_buttons.get_clicked_button(x, y):
            clicked_button = self.bot_buttons.get_clicked_button(x, y)
            self.bot_buttons.selected = clicked_button 

    def timer_is_clicked(self, x, y):
        """
        Checks if mouse click on Pygame was inside of timer area.

        Parameters:
            pos: tuple (int, int)
                X- and y-coordinates from mouse click on Pygame window.

        Output:
            bool
                True if mouse click was inside timer area and false if it was not.
        """
        if x > self.time_rect_meas[0] and x < self.time_rect_meas[2] and y > self.time_rect_meas[1] and y < self.time_rect_meas[3]:
            return True
        else:
            return False

    def draw_menu(self):
        """
        Method for drawing widgets of menu on Pygame window. This is achieved by calling methods responsible for
        drawing each seperate widget.

        For further documentation see comments for each called method. 
        """
        self.draw_menu_boarders()
        self.draw_timer()
        self.draw_turn()
        self.size_buttons.draw_buttons()
        self.color_buttons.draw_buttons()
        self.bot_buttons.draw_buttons()

    def draw_timer(self):
        """
        Draws the timer and the timer caption on the Pygame window
        """ 
        # draw timer
        if self.game.board.winner():        # If the game has a winner, the timer "freezes" on the window and 
            self.timer.set_winner_time()    # displays only the winner time.
            milliseconds = self.timer.winner_time
        else:
            milliseconds = self.timer.dt
        time_string = self.set_time_format(milliseconds)
        font_time = pygame.font.SysFont(None, 32)
        counting_text = font_time.render(time_string, 1, Constants.YELLOW, Constants.GRAY)
        counting_rect = counting_text.get_rect(centerx = Constants.WIDTH//2, top=self.upper_boarder[1]+self.upper_boarder[3])
        # self.time_rect_meas is used to make timer interactive in self.timer_is_clicked()
        self.time_rect_meas = (counting_rect.topleft[0], counting_rect.topleft[1], counting_rect.bottomright[0], counting_rect.bottomright[1])
        
        self.window.blit(counting_text, counting_rect)

        # draw caption
        font_caption = pygame.font.SysFont(None, 25)
        caption_string = "Click timer to start new game with selected options!"
        caption_text = font_caption.render(caption_string, 1, Constants.DARK_GRAY, Constants.GRAY)
        caption_rect = caption_text.get_rect(centerx=Constants.WIDTH//2, bottom=self.lower_boarder[1])
        self.window.blit(caption_text, caption_rect)

    def set_time_format(self, milliseconds):
        """
        Converts input time in milliseconds to output representing time in format h:mm:ss.

        Parameters:
            milliseconds: int
                Time in milliseconds.
        
        Output:
            time_str: str
                Time in format h:mm:ss.

        """
        seconds = milliseconds // 1000 
        second_string = str(seconds%60).zfill(2)
        minutes = seconds//60
        minute_string = str(minutes%60).zfill(2)
        hours_string = str(seconds//3600).zfill(1)
        time_str = f"{hours_string}:{minute_string}:{second_string}"
        return time_str

    def draw_menu_boarders(self):
        """
        Draws boarders in the upper and lower ends of the menu area.
        """
        boarder_height = 5
        self.upper_boarder = (0, Constants.SQUARE_SIZE*Constants.ROWS, Constants.WIDTH, boarder_height)
        self.lower_boarder = (0, Constants.HEIGHT-boarder_height, Constants.WIDTH, boarder_height)
        pygame.draw.rect(self.window, Constants.GRAY, self.upper_boarder)
        pygame.draw.rect(self.window, Constants.GRAY, self.lower_boarder)

    def draw_turn(self):
        if self.game.turn == Constants.PLAYER_COLOR:
            turn_str = '   Current turn: PLAYER   '
            turn_str_color = Constants.PLAYER_COLOR
        else:
            turn_str = 'Current turn: OPPONENT'
            turn_str_color = Constants.OPPONENT_COLOR
        if self.game.board.winner():
            turn_str_color = Constants.BLACK
        turn_font = pygame.font.SysFont(None, 25)
        turn_text = turn_font.render(turn_str, 1, turn_str_color, Constants.BLACK)
        turn_text_rect = turn_text.get_rect(centerx=Constants.WIDTH//2, bottom=self.lower_boarder[1]-27)
        self.window.blit(turn_text, turn_text_rect)


    def restart(self):
        """
        Restarts game instance with choices seleted in the menu.
        """
        self.window.fill(Constants.BLACK) # Upon restart, window is cleared by filling with black to 
                                          # erase any remainder of a previous board in the background.

        self.set_board_size()
        self.set_piece_colors()

        self.game.reset()
        self.timer.reset()
        self.has_updated_highscore = False

    def set_board_size(self):
        """
        Sets board size for new game instance as selected in menu.

        Modified instance variables:
            Constants.BOARD_SIZE: tuple
                Tuple representing board size in format (ROWS, COLS).
            Constants.ROWS, Constants.COLS: int, int
                Values for rows and columns of new board size.
            Constants.SQUARE_SIZE: int
                Size of board squares.
        """
        Constants.BOARD_SIZE = self.size_buttons.selected
        Constants.ROWS, Constants.COLS = Constants.BOARD_SIZE
        Constants.SQUARE_SIZE = Constants.WIDTH // Constants.COLS

    def set_piece_colors(self):
        """
        Sets piece colors for new game instance as selected in menu.
        
        Modified instance variables:
            Constants.PLAYER_COLOR: tuple
                Tuple representing new color for PLAYER in RGB format.
            Constants.OPPONENT_COLOR: tuple
                Tuple representing new color for OPPONENT in RGB format.
        """
        Constants.PLAYER_COLOR = self.color_buttons.selected
        if Constants.PLAYER_COLOR == Constants.RED:
            Constants.OPPONENT_COLOR = Constants.WHITE
        else:
            Constants.OPPONENT_COLOR = Constants.RED

    