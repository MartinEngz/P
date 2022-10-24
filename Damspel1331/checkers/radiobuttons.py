import pygame
from .constants import Constants


# create class RadioButtons __init__(self, caption, options, default) --> opponent_choice = RadioButtons(caption="BOT OR NOT", options=["BOT", "NOT"], default="NOT")
        # self.temp_ROWS, self.temp_COLS = 8, 8 WRITE A METHOD AND A BUTTON FOR THIS

class RadioButtons:
    def __init__(self, window, caption, options, default, top_left):
        """
        Self-made radiobuttons.

        Parameters:
            window: Pygame Surface object
                Pyagem window to draw radiobuttons on.
            caption: str
                Description of choices (e.g "Board size:"). 
            options: dictionary
                Key is string shown as a choice in the gui (e.g "RED"). Value is the data that the 
                choice "activates" (e.g the RGB color code (255, 0, 0)).
            default: [Same type as value of options dictionary]
                Which of the options are chosen by default.
            top_left: tuple
                X- and y-coordinates of text rectangle for caption.
        Instance variables initialized/modified:
            self.window: see window parameter
            self.caption: see caption parameter
            self.options: see options parameter
            self.selected: see default parameter
            self.top_left: see top_left parameter
            self.button_meas: dictionary
                This dictionary will store a button's text as the key, and its button measurements 
                in a list as value. This will be used to make the buttons interactive in the
                self.clicked_button() method.
        """
        self.window = window
        self.caption = caption
        self.options = options
        self.selected = default
        self.top_left = top_left
        self.button_meas = {}

    def draw_buttons(self):
        """
        Draws caption and options for a RadioButton object. If an option is selected, 
        its background is highlighted in yellow.
        """
        radio_font = pygame.font.SysFont(None, 22)
        caption_text = radio_font.render(self.caption, 1, Constants.GRAY, Constants.BLACK)
        caption_rect = caption_text.get_rect(topleft=self.top_left)
        self.window.blit(caption_text, caption_rect)
        for i, opt in enumerate(self.options):
            if self.selected == self.options[opt]:
                txt_color, bkgrnd_color = Constants.DARK_GRAY, Constants.YELLOW
            else:
                txt_color, bkgrnd_color = Constants.GRAY, Constants.BLACK
            option_text = radio_font.render(opt, 1, txt_color, bkgrnd_color)
            option_rect = option_text.get_rect(topleft=(caption_rect.right+5, caption_rect.top+caption_rect.height*i))
            self.button_meas[opt] = [option_rect.topleft[0], option_rect.topleft[1], option_rect.bottomright[0], option_rect.bottomright[1]]
            self.window.blit(option_text, option_rect)

    def get_clicked_button(self, x, y):
        """
        Given input cooardinates x and y from a mouse click on the screen, select an option
        if the coordinates are within the text rectangle of an option.

        Parameters:
            x, y: int, int
                X- and y-coordinates of a mouse click on the Pygame window. 
        """
        for button in self.button_meas:
            if x > self.button_meas[button][0] and x < self.button_meas[button][2] and y > self.button_meas[button][1] and y < self.button_meas[button][3]:
                return self.options[button]
    