from tests.base.BaseTestCase import BaseTestCase
import yaml
import os


class TestDatabaseSeeder(BaseTestCase):
    """Test the database seeder files are valid"""

    def test_database_seeder_files(self):
        """Test the database seeder files follow the correct format."""
        allowed_models = ['CAR', 'TRACK', 'HIGHSCORE', 'PATH', 'PROFILE', 'PROFANITY']
        for import_file in (x for x in os.listdir("database") if x.endswith(".yaml")):
            with open(f"database/{import_file}") as f:
                for item in yaml.safe_load(f):
                    self.assertTrue(item.get("model"), f"The model directive does not exist in {import_file} seeder.")
                    self.assertIn(item.get("model").upper(), allowed_models, f"{item.get('model')} is not a valid model type in the {import_file} seeder.")
