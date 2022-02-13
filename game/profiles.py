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
        """Updates the player's mute preference and plays or pauses the music as appropriate."""
        if self.mute:
            self.mute = 0
            pygame.mixer.music.unpause()
        else:
            self.mute = 1
            pygame.mixer.music.pause()

        if self.username != "default":
            # updates the players mute preference in the database if the player is not using the default profile.
            models.Profile.update(mute=self.mute).where(
                models.Profile.username == self.username
            )

    def update_last_car_id(self, car_id):
        """Updates the player's last used car, providing that the player isn't using the default profile.

        Args:
            car_id -- id of the newly chosen car
        """
        self.last_car_id = car_id

        if self.username != "default":
            # updates the player's car prerference in the database when if the player is not using the default profile.
            models.Profile.update(last_car_id=car_id).where(
                models.Profile.username == self.username
            )

    def update_last_track_id(self, track_id):
        """Updates the player's last chosen track, providing that the player isn't using the default profile.

        Args:
            track_id -- id of the newly chosen track
        """
        self.last_track_id = track_id

        if self.username != "default":
            # updates the player's track preference in the database when if the player is not using the default profile.
            models.Profile.update(last_track_id=track_id).where(
                models.Profile.username == self.username
            )
