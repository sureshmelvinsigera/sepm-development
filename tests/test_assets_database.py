from tests.base.BaseTestCase import BaseTestCase
from database.models import Car, Track
from os.path import exists


class TestDatabaseAssetsExist(BaseTestCase):
    """Checks whether database assets exist in the current file structure."""

    def test_if_track_files_exist_database(self):
        """Test if tracks in the database have associated files"""
        for item in Track.select():
            self.assertTrue(
                exists(item.track_path),
                f"File {item.track_path} referenced in the Tracks model does not exist.",
            )
            self.assertTrue(
                exists(item.border_path),
                f"File {item.border_path} referenced in the Tracks model does not exist.",
            )
            self.assertTrue(
                exists(item.background_path),
                f"File {item.background_path} referenced in the Tracks model does not exist.",
            )

    def test_if_car_files_exist_database(self):
        """Test if cars in the database have associated files"""
        for item in Car.select():
            self.assertTrue(
                exists(item.car_path),
                f"File {item.car_path} referenced in the Cars model does not exist.",
            )
