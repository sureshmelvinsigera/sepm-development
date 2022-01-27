import pygame

from database import models


class PlayerProfile:
    def __init__(self, username):
        self.username = username
        lookup_profile = models.Profile.get(models.Profile.username == username)
        self.mute = lookup_profile.mute
        self.last_car_id = lookup_profile.last_car_id
        self.last_track_id = lookup_profile.last_track_id

    def update_mute(self):
        if self.mute:
            self.mute = 0
            pygame.mixer.music.unpause()
        else:
            self.mute = 1
            pygame.mixer.music.pause()

        if self.username != "default":
            models.Profile.update(mute=self.mute).where(
                models.Profile.username == self.username
            )

    def update_last_car_id(self, car_id):
        self.last_car_id = car_id

        if self.username != "default":
            models.Profile.update(last_car_id=car_id).where(
                models.Profile.username == self.username
            )

    def update_last_track_id(self, track_id):
        self.last_track_id = track_id

        if self.username != "default":
            models.Profile.update(last_track_id=track_id).where(
                models.Profile.username == self.username
            )
