
from pathlib import Path

class GameStats:
    """Track stats for the game."""

    def __init__(self, ai_game):
        """Init the stats."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # High score should never be reset.
        self._get_saved_score()

    def reset_stats(self):
        """Init stats that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_saved_score(self):
        path = Path('max_scores.txt')
        if path.exists():
            last_score = int(path.read_text())
            self.high_score = last_score
        else:
            self.high_score = 0
