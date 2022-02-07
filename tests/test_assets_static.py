import re
from os import listdir
from os.path import exists

from tests.base.BaseTestCase import BaseTestCase


class TestStaticAssetsExist(BaseTestCase):
    """Checks all static files are present."""

    def test_if_track_files_exist(self):
        """Check if each track directory contains the required assets."""
        track_folder_names = [
            fname
            for fname in listdir("assets/images/tracks")
            if re.match(r"track-[0-9]", fname)
        ]
        for track_title in track_folder_names:
            self.assertTrue(
                exists(f"assets/images/tracks/{track_title}/{track_title}.png"),
                f"{track_title}.png does not exist in /assets/images/tracks/{track_title}/",
            )
            self.assertTrue(
                exists(f"assets/images/tracks/{track_title}/{track_title}-border.png"),
                f"{track_title}-border.png does not exist in /assets/images/tracks/{track_title}/",
            )
        self.assertTrue(
            exists(f"assets/images/tracks/finish.png"),
            f"File finish.png does not exist in /assets/images/tracks/",
        )

    def test_if_background_files_exist(self):
        """Check if the background files exist."""
        file_list = ["dirt.png", "grass.png", "stone.png"]
        for item in file_list:
            self.assertTrue(
                exists(f"assets/images/backgrounds/{item}"),
                f"File {item} does not exist in /assets/images/backgrounds/",
            )

    def test_if_car_files_exist(self):
        """Check if the car files exist."""
        file_list = [
            "black-car.png",
            "blue-car.png",
            "green-car.png",
            "red-car.png",
            "yellow-car.png",
        ]
        for item in file_list:
            self.assertTrue(
                exists(f"assets/images/cars/{item}"),
                f"File {item} does not exist in /assets/images/cars/",
            )

    def test_if_audio_files_exist(self):
        """Check if the audio files exist."""
        file_list = ["8-Bit March - Twin Musicom.mp3", "theme.wav"]
        for item in file_list:
            self.assertTrue(
                exists(f"assets/audio/{item}"),
                f"File {item} does not exist in /assets/audio/",
            )

    def test_if_ui_assets_exist(self):
        """Check whether static ui assets (Buttons, Icons etc.) exist."""
        file_list = [
            "back.png",
            "forward.png",
            "main-menu.png",
            "menu-button.png",
            "menu-button-large.png",
            "sound-off.png",
            "sound-on.png",
        ]
        for item in file_list:
            self.assertTrue(exists(f"assets/interface/{item}"))
