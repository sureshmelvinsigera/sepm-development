import os

import pygame
import yaml
from peewee import *

from database.models import Car, HighScore, Path, Profile, Track
from game.loops import main_game_loop

database = SqliteDatabase(":memory:")
database.connect()
database.create_tables([Car, Path, Profile, Track, HighScore])

# Used Generator Function (PEP 289) to iterate through *.yaml files in /database
for import_file in (x for x in os.listdir("database") if x.endswith(".yaml")):
    for item in yaml.load(open(f"database/{import_file}"), Loader=yaml.FullLoader):
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

main_game_loop()

pygame.quit()
