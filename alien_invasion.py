from operator import le
import sys
from time import sleep
import pygame
from pyparsing import col
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
# Overall class to manage game assets and behavior. 
    def __init__(self):

        # Initialize the game, and create game resources.
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Alien Invasion")  
        self.settings = Settings() 
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        # Create an instance to store game statistics
        # and createa a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Call ship
        self.ship = Ship(self)
        # Call bullets
        self.bullets = pygame.sprite.Group()
        # Call aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self,"Play")

    def run_game(self):
    # Start the main loop for the game
        while True:
            self.clock.tick(120)
            self._check_events()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # Draw the play button if the game is inactive
            if not self.stats.game_active:
                # self._update_screen()
                self.play_button.draw_button()

            self._update_screen()
            pygame.display.flip()

    def _check_events(self):
        # respond to keypress and mouse events.
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    filename = 'highscore.txt'
                    with open(filename, 'w') as file_object:
                        file_object.write(str(self.stats.high_score))
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos =pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
    def _check_play_button(self,mouse_pos):
        """ Start a new game when the player click Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics
            self.stats.game_active = True
            self.stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.sb.prep_score()
            self.sb.prep_level()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
    def _check_keydown_events(self,event):
        # Respond to keypress.
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
                
    def _check_keyup_events(self,event):
        # Rcespond to release.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            filename = 'highscore.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _update_screen(self):
        # update images on the screen, and flip to the new screen.
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        self.aliens.draw(self.screen)
        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
    
    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets. """
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappear
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to bullet-alien collisions. """
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def get_number_aliens_x(self,alien_width):
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        return number_aliens_x

    def get_number_rows(self,alien_height):
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height) - 1
        return number_rows 

    def _create_fleet(self):
        """ Create the fleet of aliens """
        # Create an alien and find the number of aliens in a row
        # Spacing berween each alien is equal to one alien width

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        number_aliens_x = self.get_number_aliens_x(alien_width)
        number_rows = self.get_number_rows(alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
            
    def _create_alien(self,alien_number,row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x

        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 100
        self.aliens.add(alien)
    
    def _update_aliens(self):
        """ 
        Check if the fleet is at an edge,
        update the positions of all aliens in the fleet. """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        
    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet's direction. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien. """
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            # Get rid of aany remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """ Check if aliens have reached the bottom of the screen. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # Treat this the same as if the ship got hit.
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
if __name__ == "__main__":
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai = ai.run_game()