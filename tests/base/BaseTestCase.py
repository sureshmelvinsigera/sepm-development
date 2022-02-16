import os
import unittest

import yaml
from peewee import *

from database.models import Car, HighScore, Path, Profile, Track

MODELS = [Car, HighScore, Path, Profile, Track]


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        test_db = SqliteDatabase(":memory:")
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=True, bind_backrefs=True)
        #
        test_db.connect()
        test_db.create_tables(MODELS)
        for import_file in (x for x in os.listdir("database") if x.endswith(".yaml")):
            with open(f"database/{import_file}") as f:
                for item in yaml.safe_load(f):
                    if item.get("model").upper() == "CAR":
                        item.pop("model")
                        Car.create(**item)
                    elif item.get("model").upper() == "TRACK":
                        item.pop("model")
                        Track.create(**item)
                    elif item.get("model").upper() == "HIGHSCORE":
                        item.pop("model")
                        HighScore.create(**item)
                    elif item.get("model").upper() == "PATH":
                        item.pop("model")
                        Path.create(**item)
                    elif item.get("model").upper() == "PROFILE":
                        item.pop("model")
                        Profile.create(**item)
