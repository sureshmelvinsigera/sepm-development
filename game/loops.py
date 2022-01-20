import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
from game.cars import PlayerCar, ComputerCar, AbstractCar
from game.track import Track
from game.profiles import PlayerProfile
from config import con, cur

pygame.font.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame-test")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551),
        (613, 715), (736, 713), (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71),
        (303, 78), (275, 377), (176, 388), (178, 260)]


class GameInfo:
    LEVELS = 10

    def __init__(self, win, width, height, main_font, level=1):
        self.win = win
        self.width = width
        self.height = height
        self.main_font = main_font
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
    def __init__(self, game_info, text, text_colour, x, y, width, height, button_colour):
        self.game_info = game_info
        self.text = text.upper()
        self.text_colour = text_colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_colour = button_colour

        self.render_text = self.game_info.main_font.render(self.text, 1, self.text_colour)
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


def high_score_name_entry(run, clock, track, player_car, computer_car, game_info, images, time, player_profile):
    if player_profile.username == 'default':
        name = ''
    else:
        name = player_profile.username

    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        main_menu_button = Button(game_info, 'menu', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        done_button = Button(game_info, 'done', (255, 255, 255), 300, 500, 200, 50, (255, 0, 0))

        menu_title(game_info, 'Enter Name')

        menu_button_text(game_info, f'Time: {time}', 300, 200)

        name_entry_box_button = Button(game_info, name, (255, 255, 255), 300, 300, 200, 50, (0, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
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

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()):
            if click:
                game_info.reset()
                player_car.reset()
                computer_car.reset()
                main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if done_button.button_rect.collidepoint(pygame.mouse.get_pos()):
            if click:
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

        for img, pos in images:
            game_info.win.blit(img, pos)

        time_text = game_info.main_font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
        game_info.win.blit(time_text, (10, game_info.height - time_text.get_height() - 40))

        time_text = game_info.main_font.render(f"Record: {track.track_record}s", 1, (255, 255, 255))
        game_info.win.blit(time_text, (10, game_info.height - time_text.get_height()))

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        main_menu_button = Button(game_info, 'menu', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        pygame.display.update()

        while not game_info.started:
            blit_text_center(game_info.win, game_info.main_font, "Press any key to start!")
            pygame.display.update()

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

                if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                    player_profile.update_mute()

                if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                    game_info.reset()
                    player_car.reset()
                    computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)
                    main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_info.reset()
            player_car.reset()
            computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)
            main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        player_car.move_player()
        computer_car.move()

        handle_collision(run, clock, track, player_car, computer_car, game_info, images, player_profile)


def settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile):

    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "Settings")

        car_button = Button(game_info, 'car', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))
        track_button = Button(game_info, 'track', (255, 255, 255), 300, 300, 200, 50, (255, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if car_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            car_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if track_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            track_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        pygame.display.update()


def car_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "Cars")

        all_cars = cur.execute(
            """
            SELECT car_id, car_name, max_vel, rotation_vel, acceleration
            FROM cars
            WHERE car_id != 'grey_car'
            """
        ).fetchall()

        car_buttons = []
        car_ids = []
        y = 200
        for car in all_cars:
            car_id, car_name, max_vel, rotation_vel, acceleration = car
            car_ids.append(car_id)
            button = Button(game_info, car_name, (255, 255, 255), 10, y, 200, 50, (255, 0, 0))
            car_buttons.append(button)
            stats_y = button.y + button.height / 2 - button.render_text.get_height() / 2
            menu_button_text(game_info, f"Speed:{max_vel}    Hand:{rotation_vel}    Acc:{acceleration}", 200, stats_y)
            y += 100

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        for button in car_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                id = car_ids[car_buttons.index(button)]
                player_car = PlayerCar(id, track.player_start_position)
                player_profile.update_last_car_id(player_car.car_id)

        pygame.display.update()


def track_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "Tracks")

        track_1_button = Button(game_info, 'Track 1', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if track_1_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            track = Track('track_1')
            player_profile.update_last_track_id(track.track_id)
            player_car.start_position = track.player_start_position
            computer_car.start_position = track.computer_start_position

        pygame.display.update()


def high_scores(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "High Scores")

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

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        pygame.display.update()


def profiles_settings(run, clock, track, player_car, computer_car, game_info, images, player_profile):

    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "Profiles")

        create_profile_button = Button(game_info, 'create profile', (255, 255, 255), 300, 100, 200, 50, (255, 0, 0))

        all_profiles = cur.execute(
            """
            SELECT username
            FROM player_profiles
            """
        ).fetchall()

        profile_buttons = []
        y = 200
        for profile in all_profiles:
            for username in profile:
                profile_buttons.append(Button(game_info, username, (255, 255, 255), 300, y, 200, 50, (255, 0, 0)))
                y += 100

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if create_profile_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            create_profile(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        for button in profile_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                player_profile = PlayerProfile(button.text.lower())
                track = Track(player_profile.last_track_id)
                player_car = PlayerCar(player_profile.last_car_id, track.player_start_position)
                computer_car = ComputerCar('grey_car', track.computer_start_position, track.computer_path)

        pygame.display.update()


def create_profile(run, clock, track, player_car, computer_car, game_info, images, player_profile):
    name = ''
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        main_menu_button = Button(game_info, 'menu', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        done_button = Button(game_info, 'done', (255, 255, 255), 300, 500, 200, 50, (255, 0, 0))

        menu_title(game_info, 'Create profile')

        menu_button_text(game_info, 'enter new username', 300, 200)

        name_entry_box_button = Button(game_info, name, (255, 255, 255), 300, 300, 200, 50, (0, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

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

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_info.reset()
            player_car.reset()
            computer_car.reset()
            main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)

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

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        menu_title(game_info, 'Main Menu')

        mute = 'mute'
        if player_profile.mute:
            mute = 'unmute'

        mute_button = Button(game_info, mute, (255, 255, 255), 600, 10, 200, 50, (255, 0, 0))

        play_button = Button(game_info, 'Play', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))
        settings_button = Button(game_info, 'Settings', (255, 255, 255), 300, 300, 200, 50, (255, 0, 0))
        high_scores_button = Button(game_info, 'High Scores', (255, 255, 255), 300, 400, 200, 50, (255, 0, 0))
        profiles_button = Button(game_info, 'profiles', (255, 255, 255), 300, 500, 200, 50, (255, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_profile.update_mute()

        if play_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if settings_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images, player_profile)

        if high_scores_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            high_scores(run, clock, track, player_car, computer_car, game_info, images, player_profile)

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

    game_info = GameInfo(WIN, WIDTH, HEIGHT, MAIN_FONT)

    images = [(track.background_image, (0, 0)), (track.track_image, (0, 0)),
              (track.finish_image, track.finish_position), (track.border_image, (0, 0))]

    main_menu(run, clock, track, player_car, computer_car, game_info, images, player_profile)
