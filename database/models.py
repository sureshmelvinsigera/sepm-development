from peewee import *

db = SqliteDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        database = db


# Car model fully implemented
class Car(BaseModel):
    car_id = TextField(primary_key=True)
    car_name = TextField()
    car_path = TextField()
    max_vel = IntegerField()
    rotation_vel = IntegerField()
    acceleration = IntegerField()

    class Meta:
        table_name = "kh_cars"


class Path(BaseModel):
    path_order = AutoField()
    track_id = TextField()
    path_x = IntegerField()
    path_y = IntegerField()

    class Meta:
        table_name = "kh_computer_paths"


# Profile model fully implemented
class Profile(BaseModel):
    username = TextField(primary_key=True)
    mute = IntegerField()
    last_car_id = TextField()
    last_track_id = TextField()

    class Meta:
        table_name = "kh_profiles"


class HighScore(BaseModel):
    id = AutoField()
    name = TextField()
    time = IntegerField()  # Need to figure out a datatype
    track_id = TextField()

    class Meta:
        table_name = "kh_high_scores"


# Track model fully implemented
class Track(BaseModel):
    track_id = TextField(primary_key=True)
    track_name = TextField()
    track_path = TextField()
    border_path = TextField()
    background_path = TextField()
    player_x = IntegerField()
    player_y = IntegerField()
    computer_x = IntegerField()
    computer_y = IntegerField()
    finish_x = IntegerField()
    finish_y = IntegerField()

    class Meta:
        table_name = "kh_tracks"
