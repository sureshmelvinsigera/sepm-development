from peewee import *

db = SqliteDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        database = db


class Car(BaseModel):
    car_id = TextField(primary_key=True)
    car_name = TextField()
    car_path = TextField()
    max_vel = IntegerField()
    rotation_vel = IntegerField()
    acceleration = IntegerField()

    class Meta:
        table_name = "cars"


class Path(BaseModel):
    path_order = AutoField()
    track_id = TextField()
    path_x = IntegerField()
    path_y = IntegerField()

    class Meta:
        table_name = "computer_paths"


class Profile(BaseModel):
    username = TextField(primary_key=True)
    mute = IntegerField()
    last_car_id = TextField()
    last_track_id = TextField()

    class Meta:
        table_name = "player_profiles"


class HighScore(BaseModel):
    id = AutoField()
    name = TextField()
    time = IntegerField()
    track_id = TextField()

    class Meta:
        table_name = "high_scores"


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
        table_name = "tracks"
