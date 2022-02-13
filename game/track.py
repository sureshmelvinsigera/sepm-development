import pygame

from database import models
from game.utilities import scale_image


class Track:
    def __init__(self, track_id):
        self.track_id = track_id
        lookup_track = models.Track.get(models.Track.track_id == track_id)
        self.track_name = lookup_track.track_name
        self.track_path = lookup_track.track_path
        self.border_path = lookup_track.border_path
        self.background_path = lookup_track.background_path
        self.player_x = lookup_track.player_x
        self.player_y = lookup_track.player_y
        self.computer_x = lookup_track.computer_x
        self.computer_y = lookup_track.computer_y
        self.finish_x = lookup_track.finish_x
        self.finish_y = lookup_track.finish_y

        self.track_record = (
            models.HighScore.select().order_by(models.HighScore.time.asc()).get().time
        )
        self.computer_path = (
            models.Path.select(models.Path.path_x, models.Path.path_y)
            .where(models.Path.track_id == self.track_id)
            .order_by(models.Path.path_order)
        )

        self.track_image = pygame.image.load(self.track_path)
        self.border_image = pygame.image.load(self.border_path)
        self.border_mask = pygame.mask.from_surface(self.border_image)
        self.background_image = pygame.image.load(self.background_path)

        self.finish_image = pygame.image.load("assets/images//tracks/finish.png")
        self.finish_mask = pygame.mask.from_surface(self.finish_image)
        self.finish_position = (self.finish_x, self.finish_y)

        self.player_start_position = (self.player_x, self.player_y)
        self.computer_start_position = (self.computer_x, self.computer_y)

    def draw_track(self, win):
        """Draws the track in the game window.

        Args:
            win -- window, or surface, the track will be drawn on.
        """
        win.blit(self.background_image, (0, 0))     # draws track background
        win.blit(self.track_image, (0, 0))      # draws track
        win.blit(self.finish_image, self.finish_position)       # draws finish line
        win.blit(self.border_image, (0, 0))     # draws track border for collision detection
