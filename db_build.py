from config import con, cur


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


def build_db():
    create_computer_paths()
