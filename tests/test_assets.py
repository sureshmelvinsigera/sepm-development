from tests.base.BaseTestCase import BaseTestCase
from os.path import exists
from database.models import Car, Track


class TestAssets(BaseTestCase):

    def test_if_backgrounds_exist(self):
        """Test if backgrounds exist from array"""
        backgrounds = ["dirt.png", "grass.png", "stone.png"]
        for item in backgrounds:
            self.assertTrue(exists(f"assets/images/backgrounds/{item}"))

    def test_if_cars_exist(self):
        """Test if cars exist from array"""
        pass

    def test_if_audio_exists(self):
        """Test if audio exists from array"""
        audio = ["8-Bit March - Twin Musicom.mp3", "theme.wav"]
        for item in audio:
            self.assertTrue(exists(f"assets/audio/{item}"))

    def test_if_tracks_exist(self):
        """Test if tracks exist from array"""
        no_of_tracks = 2
        track_file = "track-{trackno}.png"
        track_border_file = "track-{trackno}.png"
        finish_line = "finish.png"
        self.assertTrue(exists(f"assets/images/tracks/{finish_line}"))
        for track in range(1, no_of_tracks + 1):
            self.assertTrue(
                exists(f"assets/images/tracks/track-{str(track)}/{track_file.replace('{trackno}', str(track))}"))
            self.assertTrue(
                exists(f"assets/images/tracks/track-{str(track)}/{track_border_file.replace('{trackno}', str(track))}"))

    def test_if_database_track_files_exist(self):
        """Test if tracks in the database have associated files"""
        for item in Track.select():
            self.assertTrue(exists(item.track_path))
            self.assertTrue(exists(item.border_path))
            self.assertTrue(exists(item.background_path))

    def test_if_database_car_files_exist(self):
        """Test if cars in the database have associated files"""
        for item in Car.select():
            self.assertTrue(exists(item.car_path))
