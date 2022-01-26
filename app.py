import pygame
import yaml
from peewee import *

from game.loops import main_game_loop
from db_build import build_db
from database.models import Car, Path, Profile, Track, HighScore

# Start of Peewee ORM Build
database = SqliteDatabase(":memory:")
database.connect()

database.create_tables([Car, Path, Profile, Track, HighScore])

for item in yaml.load(open("database/seed.yaml"), Loader=yaml.FullLoader):
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
        pass
    elif item.get("model").upper() == "PROFILE":
        item.pop("model")
        Profile.create(**item)

# End of Peewee ORM Build

build_db()

main_game_loop()

pygame.quit()
