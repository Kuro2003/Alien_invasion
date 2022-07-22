class GameStats:
    """ Track statistics for Alien Invasion """
    def __init__(self,ai_game):
        """ Initiaalize statics.  """
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # # High score should never be reset.
        # self.high_score = 0
        self.load_high_score()

    def load_high_score(self):
        filename = 'highscore.txt'
        try:
            with open(filename) as file_object:
                score = file_object.read()
                self.high_score = int(score)
        except FileNotFoundError:
            # High score should never be reset.
            self.high_score = 0

    def reset_stats(self):
        """ Initialize statistics that can change during the game. """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1