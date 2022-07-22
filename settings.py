import pygame
class Settings:
    # A class to store all settings for Alien Invasion.
    # Screen settings
    def __init__(self):
        # Screen setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,255,255)
        self.background = pygame.image.load('images\Background.jpg')

        # Bullet setting
        self.bullet_speed = 1.75
        self.bullet_width = 8
        self.bullet_height = 15
        self.bullet_color = (255,255,255)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed = 1.2
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represent left
        self.fleet_direction = 1

        # Ship settings
        self.ship_speed = 2.2
        self.ship_limit = 2

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game """
        self.ship_speed = 2.0
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        # fleet_direction of 1 represents right; -1 represent left
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50
    
    def increase_speed(self):
        """ Increase speed settings. """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)