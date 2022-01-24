from config import con, cur


def create_tracks():
    cur.execute(
        """CREATE TABLE tracks
                    (
                    track_id text PRIMARY KEY,
                    track_name text,
                    track_path text,
                    border_path text,
                    background_path text,
                    player_x int,
                    player_y int,
                    computer_x int,
                    computer_y int,
                    finish_x int,
                    finish_y int
                    )
                """
    )

    track_list = [
        (
            "track_1",
            "Track 1",
            "assets/img/track.png",
            "assets/img/track-border.png",
            "assets/img/grass.jpg",
            180,
            200,
            150,
            200,
            130,
            250,
        ),
    ]

    cur.executemany(
        """INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", track_list
    )
    con.commit()


def create_cars():
    cur.execute(
        """CREATE TABLE cars
                    (
                    car_id text PRIMARY KEY,
                    car_name text,
                    car_path text,
                    max_vel int,
                    rotation_vel int,
                    acceleration int
                    )
                """
    )

    car_list = [
        ("red_car", "Red", "assets/img/red-car.png", 4, 4, 1),
        ("green_car", "Green", "assets/img/green-car.png", 4, 4, 1),
        ("grey_car", "Grey", "assets/img/grey-car.png", 4, 4, 1),
        ("purple_car", "Purple", "assets/img/purple-car.png", 4, 4, 1),
        ("white_car", "White", "assets/img/white-car.png", 4, 4, 1),
    ]

    cur.executemany("""INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?)""", car_list)
    con.commit()


def create_high_scores():
    cur.execute(
        """CREATE TABLE high_scores
                    (
                    name text,
                    time real,
                    track_id text
                    )
                """
    )

    high_scores_list = [
        ("testname", 50, "track_1"),
        ("NAME", 55, "track_1"),
        ("name123", 44, "track_1"),
        ("Lewis", 48, "track_1"),
        ("Max", 43, "track_1"),
    ]

    cur.executemany("""INSERT INTO high_scores VALUES (?, ?, ?)""", high_scores_list)
    con.commit()


def create_computer_paths():
    cur.execute(
        """CREATE TABLE computer_paths
                    (
                    path_order INTEGER PRIMARY KEY AUTOINCREMENT,
                    track_id text,
                    path_x int,
                    path_y int
                    )
                """
    )

    computer_paths_list = [
        ("track_1", 175, 119),
        ("track_1", 110, 70),
        ("track_1", 56, 133),
        ("track_1", 70, 481),
        ("track_1", 318, 731),
        ("track_1", 404, 680),
        ("track_1", 418, 521),
        ("track_1", 507, 475),
        ("track_1", 600, 551),
        ("track_1", 613, 715),
        ("track_1", 736, 713),
        ("track_1", 734, 399),
        ("track_1", 611, 357),
        ("track_1", 409, 343),
        ("track_1", 433, 257),
        ("track_1", 697, 258),
        ("track_1", 738, 123),
        ("track_1", 581, 71),
        ("track_1", 303, 78),
        ("track_1", 275, 377),
        ("track_1", 176, 388),
        ("track_1", 178, 260),
    ]

    cur.executemany(
        """INSERT INTO computer_paths(track_id, path_x, path_y) VALUES (?, ?, ?)""",
        computer_paths_list,
    )
    con.commit()


def create_player_profiles():
    cur.execute(
        """CREATE TABLE player_profiles
                    (
                    username text PRIMARY KEY,
                    mute int,
                    last_car_id text,
                    last_track_id text
                    )
                """
    )

    player_profiles_list = [
        ("default", 0, "red_car", "track_1"),
        ("username", 0, "red_car", "track_1"),
        ("user123", 1, "green_car", "track_1"),
        ("test name", 0, "purple_car", "track_1"),
        ("default23", 0, "red_car", "track_1"),
        ("abc123", 0, "red_car", "track_1"),
        ("xyz987", 1, "green_car", "track_1"),
        ("testing", 0, "purple_car", "track_1"),
        ("max", 0, "red_car", "track_1"),
        ("lewis", 0, "red_car", "track_1"),
        ("mike", 1, "green_car", "track_1"),
        ("alex", 0, "purple_car", "track_1"),
        ("kieron", 0, "red_car", "track_1"),
        ("kike", 0, "red_car", "track_1"),
        ("suresh", 1, "green_car", "track_1"),
        ("antonios", 0, "purple_car", "track_1"),
    ]

    cur.executemany(
        """INSERT INTO player_profiles VALUES (?, ?, ?, ?)""", player_profiles_list
    )
    con.commit()


def build_db():
    create_tracks()
    create_cars()
    create_high_scores()
    create_computer_paths()
    create_player_profiles()
