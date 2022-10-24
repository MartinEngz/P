import pygame

class Timer:
    def __init__(self):
        """
        Timer class built using Pygame's time module.

        Instance variables initialized and methods called in constructor:
            self.winner_time: int
                Winner time in milliseconds. This is initialized to None.
        """
        self.winner_time = None
        self.start_timer()
          
    def start_timer(self):
        """
        Starts timer. This method is called once only, before the start of the while loop of the
        main function. Thus, the instance variable self.t0 is not continuously updated. 

        Initialized/modified instance variables:
            self.t0: int
                Measures time in milliseconds from that pygame.init() is called.
        """
        self.t0 = pygame.time.get_ticks()

    def update_time(self):
        """
        This method is called at the beginning of every while loop of the main function and is thus
        continuously updated. 
        """
        self.t1 = pygame.time.get_ticks()
        self.dt = self.t1 - self.t0

    def set_winner_time(self):
        """
        Sets winner time.

        Instance variables modified:
            self.winner_time: int
                Winner time in milliseconds. This sets winner time only when the winner time is
                not already set, resulting in setting it only once and not continuously for as
                long as there is a winner in the game instance.
        """
        if not self.winner_time:
            self.winner_time = self.dt

    def reset(self):
        """
        Resets the timer by setting the value of t0 to the value of t1. Also resets the winner
        time to None.

        Modified instance variables:
            self.t0: int
                To visually reset the timer on the Pygame window, the value of self.t0 is set to 
                the current value of self.t1
            self.winner_time: NoneType
                Reset to None in because when the timer restarts, a new game starts, which has no winner yet. 
        """
        self.t0 = self.t1
        self.winner_time = None
