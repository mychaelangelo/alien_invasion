import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from option_field import OptionField
from random import randint


class AlienInvasion:
    """Overall class to manage game assets & behaviour."""

    def __init__(self):
        """Initialize game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Create dispaly window with set resolution as class attribute.
        self.screen =pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Create instance to store game statistics and with scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        #Groupings
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_constellation()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play button
        self.play_button = Button(self, "Play")

        # Make selection field for speed
        options = ["Normal", "Medium", "Fast"]
        placeholder = "Select Alien Speed"
        self.speed_dropdown = OptionField(self, 500, 450, options, placeholder)

    

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_stars()
            self._update_screen()
            self.clock.tick(60)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien heigh.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
            """Create an alien and place it in the fleet."""
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop entire fleet when one of aliens hits the edges."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    
    def _create_constellation(self):
        """Create constellation of stars"""
        count = 500
        while count >= 0:
            x_position = randint(0, self.settings.screen_width)
            y_position = randint(-10, self.settings.screen_height)
            self._create_star(x_position, y_position)
            count -= 1

    
    
    def _create_star(self, x_position, y_position):
        """Create a star and place it in the fleet"""
        new_star = Star(self)
        new_star.x = x_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)

    def _update_stars(self):
        for star in self.stars.sprites():
            star.set_rand_brightness()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            # to quit
            if event.type == pygame.QUIT:
                sys.exit()
            
            # keyboard events
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)     
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event) 
            
            # mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # check play button
                self._check_play_button(mouse_pos)
                
                # check option field button
                self.speed_dropdown.handle_event(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) 
        if button_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        # Reset game stats
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Set speed difficulty
        if self.speed_dropdown.selected_option:
            if self.speed_dropdown.selected_option == "Normal":
                self.settings.alien_speed = 1.0
            elif self.speed_dropdown.selected_option == "Medium":
                self.settings.alien_speed = 1.5
            elif self.speed_dropdown.selected_option == "Fast":
                self.settings.alien_speed = 2.0   

        # Set game to be active
        self.game_active = True

        # Remove any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)      
    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif (event.key == pygame.K_p) and not (self.game_active):
            self._start_game()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty() # empty() removes all sprites from group
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

        
    
    def _update_aliens(self):
        """Check if fleet is at edge, then update position."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting bottom of screen.
        self._check_aliens_bottom()
    
    def _update_screen(self):
    # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # draw stars first so they are behind all objects
        self.stars.draw(self.screen)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        # Draw score info
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            # play button
            self.play_button.draw_button()

            #draw alien speed dropdown
            self.speed_dropdown.draw_button()

        self.ship.blitme()



        pygame.display.flip()

    def _ship_hit(self):
        """Respond to ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
        
            # Create new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause the game momentarily
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Checks if aliens have reached bottom of screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if ship got hit.
                self._ship_hit()
                break


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

