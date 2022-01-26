import pygame
from game.utilities import scale_image
from config import con, cur
from database import models


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
            models.HighScore.select().order_by(models.HighScore.time.desc()).get().time
        )

        self.computer_path = cur.execute(
            """
                                        SELECT path_x, path_y
                                        FROM computer_paths 
                                        WHERE track_id = ? 
                                        ORDER BY path_order
                                        """,
            (self.track_id,),
        ).fetchall()

        self.track_image = scale_image(pygame.image.load(self.track_path), 0.9)
        self.border_image = scale_image(pygame.image.load(self.border_path), 0.9)
        self.border_mask = pygame.mask.from_surface(self.border_image)
        self.background_image = scale_image(
            pygame.image.load(self.background_path), 2.5
        )

        self.finish_image = pygame.image.load("assets/img/finish.png")
        self.finish_mask = pygame.mask.from_surface(self.finish_image)
        self.finish_position = (self.finish_x, self.finish_y)

        self.player_start_position = (self.player_x, self.player_y)
        self.computer_start_position = (self.computer_x, self.computer_y)
