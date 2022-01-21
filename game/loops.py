import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
from game.cars import PlayerCar, ComputerCar
from game.track import Track
from game.profiles import PlayerProfile
from config import con, cur

pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('./sounds/theme.wav')
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame-test")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)
SMALL_FONT = pygame.font.SysFont("comicsans", 24)

FPS = 60


class GameInfo:
    LEVELS = 10

    def __init__(self, win, width, height, main_font, small_font, level=1):
        self.win = win
        self.width = width
        self.height = height
        self.main_font = main_font
        self.small_font = small_font
        self.level = level
        self.started = False
        self.level_start_time = 0

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time, 2)


class Button:
    def __init__(self, game_info, text, text_colour, x, y, width, height, button_colour, size=True):
        self.game_info = game_info
        self.text = text.upper()
        self.text_colour = text_colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_colour = button_colour

        if size:
            self.render_text = self.game_info.main_font.render(self.text, 1, self.text_colour)
        else:
            self.render_text = self.game_info.small_font.render(self.text, 1, self.text_colour)

        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.draw_button()

    def button_text(self):
        render_text_rect = self.render_text.get_rect()
        render_text_rect.topleft = (self.x + self.width/2 - self.render_text.get_width()/2,
                                    self.y + self.height/2 - self.render_text.get_height()/2)
        self.game_info.win.blit(self.render_text, render_text_rect)

    def draw_button(self):
        pygame.draw.rect(self.game_info.win, self.button_colour, self.button_rect)
        self.button_text()


def menu_button_text(game_info, button_text, x, y):
    text = game_info.main_font.render(button_text.upper(), 1, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    game_info.win.blit(text, text_rect)


def menu_title(game_info, menu_name):
    text = game_info.main_font.render(menu_name.upper(), 1, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (game_info.win.get_width()/2 - text.get_width()/2, 10)
    game_info.win.blit(text, text_rect)


def menu_basic(run, clock, track, player_car, computer_car, game_info, images, player_profile,
               menu_name, previous_menu):

    for img, pos in images:
        game_info.win.blit(img, pos)

    computer_car.draw(game_info.win)
    player_car.draw(game_info.win)

    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

    if menu_name != 'game':
        menu_title(game_info, menu_name)

    mute = 'mute'
    if player_profile.mute:
        mute = 'unmute'

    width, height = 150, 20

    mute_button = Button(game_info, mute, (255, 255, 255), game_info.win.get_width() - width - 10, 10,
                         width, height, (255, 0, 0), False)
    if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
        player_profile.update_mute()

    if menu_name != 'main menu':
        main_menu_button = Button(game_info, 'main menu', (255, 255, 255), 10, 10, width, height, (255, 0, 0), False)
        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_info.reset()
            player_car.reset()
            computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)
            main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if menu_name != 'game' and previous_menu in ['settings', 'profiles']:
            back_button = Button(game_info, 'Back', (255, 255, 255), 10, 40, width, height, (255, 0, 0), False)
            if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                if previous_menu == 'settings':
                    settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)
                if previous_menu == 'profiles':
                    profiles_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

    if menu_name == 'game':
        time_text = game_info.main_font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
        game_info.win.blit(time_text, (10, game_info.height - time_text.get_height() - 40))

        time_text = game_info.main_font.render(f"Record: {track.track_record}s", 1, (255, 255, 255))
        game_info.win.blit(time_text, (10, game_info.height - time_text.get_height()))

    return click


def high_score_name_entry(run, clock, track, player_car, computer_car, game_info, images, time, player_profile):
    if player_profile.username == 'default':
        name = ''
    else:
        name = player_profile.username

    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'enter name', 'main menu')

        menu_button_text(game_info, f'Time: {time}', 300, 200)

        name_entry_box_button = Button(game_info, name, (255, 255, 255), 300, 300, 200, 50, (0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if len(name) != 0:
                        cur.execute("""INSERT INTO high_scores VALUES (?, ?, ?)""",
                                    (name, time, track.track_id))
                        con.commit()
                        game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

                    else:
                        game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 8:
                    name += event.unicode

        done_button = Button(game_info, 'done', (255, 255, 255), 300, 500, 200, 50, (255, 0, 0))
        if done_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            if len(name) != 0:
                cur.execute("""INSERT INTO high_scores VALUES (?, ?, ?)""",
                            (name, time, track.track_id))
                con.commit()
                game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)
            else:
                game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        pygame.display.update()


def handle_collision(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    if player_car.collide(track.border_mask) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        track.finish_mask, *track.finish_position)
    if computer_finish_poi_collide != None:
        blit_text_center(game_info.win, game_info.main_font, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)
        game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

    player_finish_poi_collide = player_car.collide(
        track.finish_mask, *track.finish_position)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            blit_text_center(game_info.win, game_info.main_font, "You Win!")
            time = game_info.get_level_time()
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)
            high_score_name_entry(run, clock, track, player_car, computer_car, game_info, images, time, player_profile)


def game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    while run:
        clock.tick(FPS)

        menu_basic(run, clock, track, player_car, computer_car, game_info, images, player_profile, 'game', 'main menu')

        while not game_info.started:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

            width, height = 150, 20

            mute = 'mute'
            if player_profile.mute:
                mute = 'unmute'

            mute_button = Button(game_info, mute, (255, 255, 255), game_info.win.get_width() - width - 10, 10,
                                 width, height, (255, 0, 0), False)
            if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                player_profile.update_mute()

            main_menu_button = Button(game_info, 'main menu', (255, 255, 255), 10, 10,
                                      width, height, (255, 0, 0), False)
            if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                game_info.reset()
                player_car.reset()
                computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)
                main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

            blit_text_center(game_info.win, game_info.main_font, "Press any key to start!")

            pygame.display.update()

        player_car.move_player()
        computer_car.move()

        handle_collision(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        pygame.display.update()


def settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile):

    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'settings', 'main menu')

        car_button = Button(game_info, 'car', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))
        if car_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            car_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        track_button = Button(game_info, 'track', (255, 255, 255), 300, 300, 200, 50, (255, 0, 0))
        if track_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            track_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        pygame.display.update()


def car_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    all_cars = cur.execute(
        """
        SELECT car_id, car_name, max_vel, rotation_vel, acceleration
        FROM cars
        WHERE car_id != 'grey_car'
        ORDER BY car_name
        """
    ).fetchall()

    start_index = 0

    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'cars', 'settings')

        car_buttons = []
        car_ids = []
        y = 200
        for car in all_cars[start_index: min(len(all_cars), start_index+5)]:
            car_id, car_name, max_vel, rotation_vel, acceleration = car
            car_ids.append(car_id)
            button = Button(game_info, car_name, (255, 255, 255), 10, y, 200, 50, (255, 0, 0))
            car_buttons.append(button)
            stats_y = button.y + button.height / 2 - button.render_text.get_height() / 2
            menu_button_text(game_info, f"Speed:{max_vel}    Hand:{rotation_vel}    Acc:{acceleration}", 200, stats_y)
            y += 100

        for button in car_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                id = car_ids[car_buttons.index(button)]
                player_car = PlayerCar(id, track.player_start_position)
                player_profile.update_last_car_id(player_car.car_id)

        width, height = 150, 30
        if start_index + 5 < len(all_cars):
            next_button = Button(game_info, 'next', (255, 255, 255),
                                 game_info.win.get_width() - width - 10, game_info.win.get_height() - height - 10,
                                 150, 30, (255, 0, 0), False)
            if next_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                start_index += 5

        if start_index > 0:
            previous_button = Button(game_info, 'previous', (255, 255, 255),
                                     10, game_info.win.get_height() - height - 10,
                                     150, 30, (255, 0, 0), False)
            if previous_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                start_index -= 5

        pygame.display.update()


def track_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    all_tracks = cur.execute(
        """
        SELECT track_id, track_name
        FROM tracks
        ORDER BY track_name
        """
    ).fetchall()

    start_index = 0

    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'tracks', 'settings')

        track_buttons = []
        track_ids = []
        y = 200
        for each_track in all_tracks[start_index: min(len(all_tracks), start_index+5)]:
            track_id, track_name = each_track
            track_ids.append(track_id)
            button = Button(game_info, track_name, (255, 255, 255), 300, y, 200, 50, (255, 0, 0))
            track_buttons.append(button)
            y += 100

        for button in track_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                id = track_ids[track_buttons.index(button)]
                track = Track(id)
                player_profile.update_last_track_id(track.track_id)

        width, height = 150, 30
        if start_index + 5 < len(all_tracks):
            next_button = Button(game_info, 'next', (255, 255, 255),
                                 game_info.win.get_width() - width - 10, game_info.win.get_height() - height - 10,
                                 150, 30, (255, 0, 0), False)
            if next_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                start_index += 5

        if start_index > 0:
            previous_button = Button(game_info, 'previous', (255, 255, 255),
                                     10, game_info.win.get_height() - height - 10,
                                     150, 30, (255, 0, 0), False)
            if previous_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                start_index -= 5

        pygame.display.update()


def high_scores(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'high scores', 'main menu')

        top_scores = cur.execute(
                                """
                                SELECT name, time 
                                FROM high_scores 
                                WHERE track_id = ? 
                                ORDER BY time 
                                LIMIT 5
                                """,
                                (track.track_id,)
                                ).fetchall()

        x, y, score_pos = 150, 200, 1
        for name, time in top_scores:
            menu_button_text(game_info, f"{score_pos}.", x - 50, y)
            menu_button_text(game_info, name, x, y)
            menu_button_text(game_info, str(round(time, 3)), x + 300, y)
            y += 100
            score_pos += 1

        pygame.display.update()


def profiles_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    all_profiles = cur.execute(
        """
        SELECT username
        FROM player_profiles
        ORDER BY username
        """
    ).fetchall()

    start_index = 0

    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'create profile', 'main menu')

        create_profile_button = Button(game_info, 'create profile', (255, 255, 255), 300, 100, 200, 50, (255, 0, 0))
        if create_profile_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            create_profile(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        profile_buttons = []
        y = 200
        for profile in all_profiles[start_index: min(len(all_profiles), start_index+5)]:
            for username in profile:
                profile_buttons.append(Button(game_info, username, (255, 255, 255), 300, y, 200, 50, (255, 0, 0)))
                y += 100

        for button in profile_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                player_profile = PlayerProfile(button.text.lower())
                track = Track(player_profile.last_track_id)
                player_car = PlayerCar(player_profile.last_car_id, track.player_start_position)
                computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)

        width, height = 150, 30
        if start_index + 5 < len(all_profiles):
            next_button = Button(game_info, 'next', (255, 255, 255),
                                 game_info.win.get_width() - width - 10, game_info.win.get_height() - height - 10,
                                 150, 30, (255, 0, 0), False)
            if next_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                start_index += 5

        if start_index > 0:
            previous_button = Button(game_info, 'previous', (255, 255, 255),
                                     10, game_info.win.get_height() - height - 10,
                                     150, 30, (255, 0, 0), False)
            if previous_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                start_index -= 5

        pygame.display.update()


def create_profile(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    name = ''
    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'create profile', 'profiles')

        menu_button_text(game_info, 'enter new username', 300, 200)

        name_entry_box = Button(game_info, name, (255, 255, 255), 300, 300, 200, 50, (0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if len(name) != 0 \
                            and name not in cur.execute("""SELECT username FROM player_profiles""").fetchall():
                        cur.execute("""INSERT INTO player_profiles VALUES (?, ?, ?, ?)""",
                                    (name, player_profile.mute, player_car.car_id, track.track_id))
                        con.commit()
                        player_profile = PlayerProfile(name)
                        profiles_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 8:
                    name += event.unicode

        done_button = Button(game_info, 'done', (255, 255, 255), 300, 500, 200, 50, (255, 0, 0))
        if done_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            if len(name) != 0 \
                    and name not in cur.execute("""SELECT username FROM player_profiles""").fetchall():
                cur.execute("""INSERT INTO player_profiles VALUES (?, ?, ?, ?)""",
                            (name, player_profile.mute, player_car.car_id, track.track_id))
                con.commit()
                player_profile = PlayerProfile(name)
                profiles_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        pygame.display.update()


def main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    while run:
        clock.tick(FPS)

        click = menu_basic(run, clock, track, player_car, computer_car, game_info, images,
                           player_profile, 'main menu', 'main menu')

        play_button = Button(game_info, 'Play', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))
        if play_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        settings_button = Button(game_info, 'Settings', (255, 255, 255), 300, 300, 200, 50, (255, 0, 0))
        if settings_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        high_scores_button = Button(game_info, 'High Scores', (255, 255, 255), 300, 400, 200, 50, (255, 0, 0))
        if high_scores_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            high_scores(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        profiles_button = Button(game_info, 'profiles', (255, 255, 255), 300, 500, 200, 50, (255, 0, 0))
        if profiles_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            profiles_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        pygame.display.update()


def main_game_loop():

    run = True

    clock = pygame.time.Clock()

    player_profile = PlayerProfile('default')

    track = Track(player_profile.last_track_id)

    player_car = PlayerCar(player_profile.last_car_id, track.player_start_position)

    computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)

    game_info = GameInfo(WIN, WIDTH, HEIGHT, MAIN_FONT, SMALL_FONT)

    images = [(track.background_image, (0, 0)), (track.track_image, (0, 0)),
              (track.finish_image, track.finish_position), (track.border_image, (0, 0))]

    main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)
