import pygame
from config import con, cur


class PlayerProfile:
    def __init__(self, username):
        self.username = username
        self.mute = cur.execute("""SELECT mute FROM player_profiles WHERE username = ?""",
                                    (self.username,)).fetchone()[0]
        self.last_car_id = cur.execute("""SELECT last_car_id FROM player_profiles WHERE username = ?""",
                                    (self.username,)).fetchone()[0]
        self.last_track_id = cur.execute("""SELECT last_track_id FROM player_profiles WHERE username = ?""",
                                (self.username,)).fetchone()[0]

    def update_mute(self):
        if self.mute:
            self.mute = 0
        else:
            self.mute = 1

        if self.username != 'default':
            cur.execute("""UPDATE player_profiles SET mute = ? WHERE username = ?""",
                        (self.mute, self.username))
            con.commit()

    def update_last_car_id(self, car_id):
        self.last_car_id = car_id

        if self.username != 'default':
            cur.execute("""UPDATE player_profiles SET last_car_id = ? WHERE username = ?""",
                        (car_id, self.username))
            con.commit()

    def update_last_track_id(self, track_id):
        self.last_track_id = track_id

        if self.username != 'default':
            cur.execute("""UPDATE player_profiles SET last_track_id = ? WHERE username = ?""",
                        (track_id, self.username))
            con.commit()
