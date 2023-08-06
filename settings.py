class Settings:
    """A class to store all settings for the Alien Invasion game."""

    def __init__(self):
        """Init the game settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5

        # Alien settings
        self.alien_speed = 1.0
        self.ship_limit = 3
        self.fleet_drop_speed = 100 # default is 10
        # fleet direction of 1 represents right, -1 is left.
        self.fleet_direction = 1

        # Bullet settings
        self.bullet_speed = 10.0 # init seting is value 2.5
        self.bullet_width = 300 # init setting is value 3.0
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3