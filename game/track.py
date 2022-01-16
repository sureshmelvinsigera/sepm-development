import pygame
from game.utilities import scale_image
import config

con = config.con
cur = con.cursor()


class Track:
    def __init__(self, track_id):
        self.track_id = track_id
        self.track_name = cur.execute("""SELECT track_name FROM tracks WHERE track_id = ?""",
                                   (self.track_id,)).fetchone()[0]
        self.track_path = cur.execute("""SELECT track_path FROM tracks WHERE track_id = ?""",
                                      (self.track_id,)).fetchone()[0]
        self.border_path = cur.execute("""SELECT border_path FROM tracks WHERE track_id = ?""",
                                      (self.track_id,)).fetchone()[0]
        self.background_path = cur.execute("""SELECT background_path FROM tracks WHERE track_id = ?""",
                                      (self.track_id,)).fetchone()[0]
        self.player_x = cur.execute("""SELECT player_x FROM tracks WHERE track_id = ?""",
                                           (self.track_id,)).fetchone()[0]
        self.player_y = cur.execute("""SELECT player_y FROM tracks WHERE track_id = ?""",
                                           (self.track_id,)).fetchone()[0]
        self.computer_x = cur.execute("""SELECT computer_x FROM tracks WHERE track_id = ?""",
                                           (self.track_id,)).fetchone()[0]
        self.computer_y = cur.execute("""SELECT computer_y FROM tracks WHERE track_id = ?""",
                                           (self.track_id,)).fetchone()[0]
        self.finish_x = cur.execute("""SELECT finish_x FROM tracks WHERE track_id = ?""",
                                       (self.track_id,)).fetchone()[0]
        self.finish_y = cur.execute("""SELECT finish_y FROM tracks WHERE track_id = ?""",
                                       (self.track_id,)).fetchone()[0]

        self.track_image = scale_image(pygame.image.load(self.track_path), 0.9)
        self.border_image = scale_image(pygame.image.load(self.border_path), 0.9)
        self.border_mask = pygame.mask.from_surface(self.border_image)
        self.background_image = scale_image(pygame.image.load(self.background_path), 2.5)

        self.finish_image = pygame.image.load("imgs/finish.png")
        self.finish_mask = pygame.mask.from_surface(self.finish_image)
        self.finish_position = (self.finish_x, self.finish_y)

        self.player_start_position = (self.player_x, self.player_y)
        self.computer_start_position = (self.computer_x, self.computer_y)


