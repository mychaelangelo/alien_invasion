import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    """A class to represent a single star."""

    def __init__(self, ai_game):
        # inherit from the Sprite class
        super().__init__()
        self.screen = ai_game.screen

        # create a surface (2x2 pixel) to draw a star
        self.image = pygame.Surface((2, 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # Color the star
        self.image.fill((255, 255, 255, 255)) 

        # set initial brightness
        self.brightness = 255
        self.update_image()

        # Get the rect of the image
        self.rect = self.image.get_rect()

        # Set init position of the star
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store star's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update_image(self):
        # Set color of star based on brightness
        color = (self.brightness, self.brightness, self.brightness, 255)
        self.image.fill(color)

    def set_rand_brightness(self):
        # modify brightness by a random amount
        change = randint(-10, 10)
        self.brightness = max(100, min(255, self.brightness + change))
        self.update_image()