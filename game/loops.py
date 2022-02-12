import time

import pygame

from database import models
from game.cars import ComputerCar, PlayerCar
from game.profiles import PlayerProfile
from game.track import Track
from game.utilities import blit_text_center, censor_word, draw_computer_path

pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/theme.wav")
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Track-Surf")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)
SMALL_FONT = pygame.font.SysFont("comicsans", 24)

FPS = 60


class GameInfo:
    def __init__(self):
        self.started = False
        self.race_start_time = 0

    def reset(self):
        """Resets start time and started to false."""
        self.started = False
        self.race_start_time = 0

    def start_race(self):
        """Sets start to true and gets start time."""
        self.started = True
        self.race_start_time = time.time()

    def get_race_time(self):
        """Returns race time if race is started."""
        if not self.started:
            return 0
        return round(time.time() - self.race_start_time, 2)


class Button:
    """self.width = width
    self.height = height
    self.button_colour = button_colour

    if size:
        self.render_text = MAIN_FONT.render(self.text, 1, self.text_colour)
    else:
        self.render_text = SMALL_FONT.render(self.text, 1, self.text_colour)

    self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)"""

    def __init__(self, text, text_colour, x, y, button_type):
        self.text = text.upper()
        self.text_colour = text_colour
        self.x = x
        self.y = y
        self.button_position = (self.x, self.y)
        self.render_text = MAIN_FONT.render(self.text, 1, self.text_colour)

        self.image_path = f"assets/interface/{button_type}.png"
        self.button_image = pygame.image.load(self.image_path)

        self.width = self.button_image.get_width()
        self.height = self.button_image.get_height()

        self.button_rect = pygame.Rect(
            self.x,
            self.y,
            self.button_image.get_width(),
            self.button_image.get_height(),
        )

        self.draw_button()

    def button_text(self):
        """Draws button text onto the button rectangle."""
        WIN.blit(
            self.render_text,
            (
                self.x
                + self.button_image.get_width() / 2
                - self.render_text.get_width() / 2,
                self.y
                + self.button_image.get_height() / 2
                - self.render_text.get_height() / 2,
            ),
        )

    def draw_button(self):
        """Draws the button and button text."""
        WIN.blit(self.button_image, self.button_position)
        self.button_text()


class TextBox:
    def __init__(self, text=""):
        self.text = text.lower()
        self.text_colour = (255, 255, 255)
        self.x = 300
        self.y = 300
        self.width = 200
        self.height = 50
        self.background_colour = (0, 0, 0)

        self.render_text = MAIN_FONT.render(self.text, 1, self.text_colour)

        self.textbox_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def input_text(self):
        """Draws the text the text box"""
        WIN.blit(
            self.render_text,
            (
                self.x + self.width / 2 - self.render_text.get_width() / 2,
                self.y + self.height / 2 - self.render_text.get_height() / 2,
            ),
        )

    def draw_textbox(self):
        """Draws the text bow"""
        pygame.draw.rect(WIN, self.background_colour, self.textbox_rect)
        self.input_text()

    def update_text(self, event):
        """Updates the text in the text box if the string is less than 8 characters.

        Args:
            event -- a pygame event.
        """
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        elif len(self.text) < 8:
            self.text += event.unicode
            self.text = self.text.lower()

        self.render_text = MAIN_FONT.render(self.text, 1, self.text_colour)


def quit_game():
    """Quits pygame and exits."""
    pygame.quit()
    exit()


def menu_text(button_text, x, y):
    """Draws text at the appropriate co-ordinates

    Args:
        button_text -- text to be drawn on screen.
        x -- x co-ordinate of top left corner of text.
        y -- y co-ordinate of top left corner of text.
    """
    text = MAIN_FONT.render(button_text.upper(), 1, (255, 255, 255))
    WIN.blit(text, (x, y))


def menu_title(menu_name):
    """Draws menu title text at the top centre of the window.

    Args:
        menu_name -- menu title text to be drawn.
    """
    text = MAIN_FONT.render(menu_name.upper(), 1, (255, 255, 255))
    WIN.blit(text, (WIN.get_width() / 2 - text.get_width() / 2, 10))


def menu_basic(
    clock,
    track,
    player_car,
    computer_car,
    game_info,
    player_profile,
    menu_name,
    previous_menu,
    click,
):
    """Draws the basic menu screen, or game window, and navigation buttons as appropriate.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
        menu_name -- current menu title.
        previous_menu -- previous menu name.
        click -- boolean based on if the player has clicked their mouse.
    """
    track.draw_track(WIN)
    computer_car.draw(WIN)
    player_car.draw(WIN)

    if menu_name != "game":
        menu_title(menu_name)

    mute = "sound-on"
    if player_profile.mute:
        mute = "sound-off"

    width, height = 150, 20

    mute_button = Button("", (255, 255, 255), WIDTH - 100, 10, mute)
    if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
        player_profile.update_mute()

    if menu_name != "main menu":
        main_menu_button = Button("", (255, 255, 255), 10, 10, "main-menu")
        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_info.reset()
            player_car.reset()
            computer_car = ComputerCar(
                "black_car",
                track.computer_start_position,
                track.computer_path,
                track.track_record,
            )
            main_menu(clock, track, player_car, computer_car, game_info, player_profile)

        if menu_name != "game" and previous_menu in ["settings", "profiles"]:
            back_button = Button("", (255, 255, 255), 10, 80, "back")
            if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                if previous_menu == "settings":
                    settings_loop(
                        clock,
                        track,
                        player_car,
                        computer_car,
                        game_info,
                        player_profile,
                    )
                if previous_menu == "profiles":
                    profiles_settings(
                        clock,
                        track,
                        player_car,
                        computer_car,
                        game_info,
                        player_profile,
                    )

    if menu_name == "game":
        time_text = MAIN_FONT.render(
            f"Time: {game_info.get_race_time()}s", 1, (255, 255, 255)
        )
        WIN.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

        time_text = MAIN_FONT.render(
            f"Record: {track.track_record}s", 1, (255, 255, 255)
        )
        WIN.blit(time_text, (10, HEIGHT - time_text.get_height()))


def menu_bottom_nav_buttons(start_index, all_list, click):
    """Displays the forward/back navigation buttons on menus when appropriate.

    Args:
        start_index -- index the data will begin being displayed from.
        all_list -- list of all data being displayed.
        click -- boolean based on if the player has clicked their mouse.
    """
    if start_index + 5 < len(all_list):
        next_button = Button(
            "",
            (255, 255, 255),
            WIDTH - 100,
            HEIGHT - 100,
            "forward",
        )
        if next_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            start_index += 5

    if start_index > 0:
        previous_button = Button("", (255, 255, 255), 10, HEIGHT - 100, "back")
        if previous_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            start_index -= 5

    return start_index


def high_score_name_entry(
    clock, track, player_car, computer_car, game_info, time, player_profile
):
    """Displays the name entry screen for the player to save their race time.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        time -- race finish time.
        player_profile -- current PlayerProfile object.
    """
    if player_profile.username == "default":
        name_entry_box = TextBox()
    else:
        name_entry_box = TextBox(player_profile.username)

    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            if event.type == pygame.KEYDOWN:
                name_entry_box.update_text(event)

                if event.key == pygame.K_RETURN:
                    if name_entry_box.text != "":
                        models.HighScore.create(
                            name=name_entry_box.text, time=time, track_id=track.track_id
                        )
                        game_loop(
                            clock,
                            track,
                            player_car,
                            computer_car,
                            game_info,
                            player_profile,
                        )
                    else:
                        game_loop(
                            clock,
                            track,
                            player_car,
                            computer_car,
                            game_info,
                            player_profile,
                        )

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "enter name",
            "main menu",
            click,
        )

        menu_text(f"Time: {time}", 300, 200)

        name_entry_box.draw_textbox()

        done_button = Button("done", (255, 255, 255), 300, 500, "menu-button")
        if done_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            if name_entry_box.text != "":
                models.HighScore.create(
                    name=name_entry_box.text, time=time, track_id=track.track_id
                )
                game_loop(
                    clock, track, player_car, computer_car, game_info, player_profile
                )
            else:
                game_loop(
                    clock, track, player_car, computer_car, game_info, player_profile
                )

        pygame.display.update()


def handle_collision(clock, track, player_car, computer_car, game_info, player_profile):
    """Handles collisions between the player car, track, and finish line. Also handles collisions
    between the computer car and finish line.

        Args:
            clock -- pygame clock.
            track -- current Track object.
            player_car -- current PlayerCar object.
            computer_car -- current ComputerCar object.
            game_info -- GameInfo object.
            player_profile -- current PlayerProfile object.
    """
    if player_car.collide(track.border_mask) is not None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        track.finish_mask, track.finish_x, track.finish_y
    )
    if computer_finish_poi_collide is not None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(2000)
        game_info.reset()
        player_car.reset()
        computer_car = ComputerCar(
            "black_car",
            track.computer_start_position,
            track.computer_path,
            track.track_record,
        )
        game_loop(clock, track, player_car, computer_car, game_info, player_profile)

    player_finish_poi_collide = player_car.collide(
        track.finish_mask, track.finish_x, track.finish_y
    )
    if player_finish_poi_collide is not None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, "You Win!")
            time = game_info.get_race_time()
            pygame.display.update()
            pygame.time.wait(2000)
            game_info.reset()
            player_car.reset()
            computer_car = ComputerCar(
                "black_car",
                track.computer_start_position,
                track.computer_path,
                track.track_record,
            )
            high_score_name_entry(
                clock, track, player_car, computer_car, game_info, time, player_profile
            )


def game_loop(clock, track, player_car, computer_car, game_info, player_profile):
    """The main game loop that draws the race and handles car movement.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "game",
            "main menu",
            click,
        )

        ################################################
        # for finding new track path
        # draw_computer_path(click, computer_car, track, WIN)
        ###############################################

        while not game_info.started:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.KEYDOWN:
                    game_info.start_race()

            width, height = 150, 20

            mute = "sound-on"
            if player_profile.mute:
                mute = "sound-off"

            mute_button = Button("", (255, 255, 255), WIDTH - 100, 10, mute)
            if mute_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                player_profile.update_mute()

            main_menu_button = Button("", (255, 255, 255), 10, 10, "main-menu")
            if (
                main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos())
                and click
            ):
                game_info.reset()
                player_car.reset()
                computer_car = ComputerCar(
                    "black_car",
                    track.computer_start_position,
                    track.computer_path,
                    track.track_record,
                )
                main_menu(
                    clock, track, player_car, computer_car, game_info, player_profile
                )

            blit_text_center(WIN, MAIN_FONT, "Press any key to start!")

            pygame.display.update()

        player_car.move_player()
        computer_car.move()

        handle_collision(
            clock, track, player_car, computer_car, game_info, player_profile
        )

        pygame.display.update()


def settings_loop(clock, track, player_car, computer_car, game_info, player_profile):
    """Displays the main settings menu.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "settings",
            "main menu",
            click,
        )

        car_button = Button("car", (255, 255, 255), 300, 200, "menu-button")
        if car_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            car_settings(
                clock, track, player_car, computer_car, game_info, player_profile
            )

        track_button = Button("track", (255, 255, 255), 300, 300, "menu-button")
        if track_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            track_settings(
                clock, track, player_car, computer_car, game_info, player_profile
            )

        pygame.display.update()


def car_settings(clock, track, player_car, computer_car, game_info, player_profile):
    """Displays the car selection menu.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    all_cars = (
        models.Car.select(
            models.Car.car_id,
            models.Car.car_name,
            models.Car.max_vel,
            models.Car.rotation_vel,
            models.Car.acceleration,
        )
        .where(models.Car.car_id != "black_car")
        .order_by(models.Car.car_name)
    )

    start_index = 0

    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "cars",
            "settings",
            click,
        )

        car_buttons = []
        car_ids = []
        y = 200
        for item in all_cars:
            car_ids.append(item.car_id)
            button = Button(item.car_name, (255, 255, 255), 10, y, "menu-button")
            car_buttons.append(button)
            stats_y = button.y + button.height / 2 - button.render_text.get_height() / 2
            menu_text(
                f"Speed:{item.max_vel}    Hand:{item.rotation_vel}    Acc:{item.acceleration}",
                200,
                stats_y,
            )
            y += 100

        for button in car_buttons[start_index : min(start_index + 5, len(all_cars))]:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                id = car_ids[car_buttons.index(button)]
                player_car = PlayerCar(id, track.player_start_position)
                player_profile.update_last_car_id(player_car.car_id)

        start_index = menu_bottom_nav_buttons(start_index, all_cars, click)

        pygame.display.update()


def track_settings(clock, track, player_car, computer_car, game_info, player_profile):
    """Displays the track selection menu.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    all_tracks = models.Track.select(
        models.Track.track_id, models.Track.track_name
    ).order_by(models.Track.track_name)
    start_index = 0

    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "tracks",
            "settings",
            click,
        )

        track_buttons = []
        track_ids = []
        y = 200
        for item in all_tracks[start_index : min(start_index + 5, len(all_tracks))]:
            track_ids.append(item.track_id)
            button = Button(item.track_name, (255, 255, 255), 300, y, "menu-button")
            track_buttons.append(button)
            y += 100

        for button in track_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                id = track_ids[track_buttons.index(button)]
                track = Track(id)
                player_car = PlayerCar(
                    player_profile.last_car_id, track.player_start_position
                )
                computer_car = ComputerCar(
                    "black_car",
                    track.computer_start_position,
                    track.computer_path,
                    track.track_record,
                )
                player_profile.update_last_track_id(track.track_id)

        start_index = menu_bottom_nav_buttons(start_index, all_tracks, click)

        pygame.display.update()


def high_scores(clock, track, player_car, computer_car, game_info, player_profile):
    """Displays the high scores screen for the current track.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    top_scores = (
        models.HighScore.select(models.HighScore.name, models.HighScore.time)
        .where(models.HighScore.track_id == track.track_id)
        .order_by(models.HighScore.time)
        .limit(50)
    )
    start_index = 0
    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "high scores",
            "main menu",
            click,
        )

        x, y = 150, 200
        score_pos = 1
        for item in top_scores[start_index : min(start_index + 5, len(top_scores))]:
            menu_text(f"{start_index + score_pos}.", x - 50, y)
            if (
                models.Profanity.select()
                .where(models.Profanity.word == item.name.lower())
                .exists()
            ):
                menu_text(censor_word(item.name), x, y)
            else:
                menu_text(item.name, x, y)
            menu_text(str(round(item.time, 3)), x + 300, y)
            y += 100
            score_pos += 1

        start_index = menu_bottom_nav_buttons(start_index, top_scores, click)

        pygame.display.update()


def profiles_settings(
    clock, track, player_car, computer_car, game_info, player_profile
):
    """Displays the profile selection menu.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    all_profiles = models.Profile.select(models.Profile.username).order_by(
        models.Profile.username
    )

    start_index = 0

    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "profiles",
            "main menu",
            click,
        )

        create_profile_button = Button(
            "new profile", (255, 255, 255), 250, 100, "menu-button-large"
        )
        if (
            create_profile_button.button_rect.collidepoint(pygame.mouse.get_pos())
            and click
        ):
            create_profile(
                clock, track, player_car, computer_car, game_info, player_profile
            )

        profile_buttons = []
        y = 200
        for profile in all_profiles[
            start_index : min(start_index + 5, len(all_profiles))
        ]:
            profile_buttons.append(
                Button(profile.username, (255, 255, 255), 250, y, "menu-button-large")
            )
            y += 100

        for button in profile_buttons:
            if button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                player_profile = PlayerProfile(button.text.lower())
                track = Track(player_profile.last_track_id)
                player_car = PlayerCar(
                    player_profile.last_car_id, track.player_start_position
                )
                computer_car = ComputerCar(
                    "black_car",
                    track.computer_start_position,
                    track.computer_path,
                    track.track_record,
                )

        start_index = menu_bottom_nav_buttons(start_index, all_profiles, click)

        pygame.display.update()


def create_profile(clock, track, player_car, computer_car, game_info, player_profile):
    """Displays profile creation menu.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    name_entry_box = TextBox()
    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            if event.type == pygame.KEYDOWN:

                name_entry_box.update_text(event)

                if (
                    event.key == pygame.K_RETURN
                    and len(name_entry_box.text) != 0
                    and not models.Profile.select()
                    .where(models.Profile.username == name_entry_box.text)
                    .exists()
                ):
                    models.Profile.create(
                        username=name_entry_box.text,
                        mute=player_profile.mute,
                        last_car_id=player_car.car_id,
                        last_track_id=track.track_id,
                    )
                    player_profile = PlayerProfile(name_entry_box.text)
                    profiles_settings(
                        clock,
                        track,
                        player_car,
                        computer_car,
                        game_info,
                        player_profile,
                    )

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "create profile",
            "profiles",
            click,
        )

        menu_text("enter new username", 300, 200)

        name_entry_box.draw_textbox()

        done_button = Button("done", (255, 255, 255), 300, 500, "menu-button")
        if done_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            if (
                name_entry_box.text != ""
                # and name_entry_box.text
                # not in cur.execute(
                #     """SELECT username FROM player_profiles"""
                # ).fetchall()
                and not models.Profile.select()
                .where(models.Profile.username == name_entry_box.text)
                .exists()
            ):
                models.Profile.create(
                    username=name_entry_box.text,
                    mute=player_profile.mute,
                    last_car_id=player_car.car_id,
                    last_track_id=track.track_id,
                )
                player_profile = PlayerProfile(name_entry_box.text)
                profiles_settings(
                    clock, track, player_car, computer_car, game_info, player_profile
                )

        pygame.display.update()


def main_menu(clock, track, player_car, computer_car, game_info, player_profile):
    """Displays the main menu.

    Args:
        clock -- pygame clock.
        track -- current Track object.
        player_car -- current PlayerCar object.
        computer_car -- current ComputerCar object.
        game_info -- GameInfo object.
        player_profile -- current PlayerProfile object.
    """
    while True:
        clock.tick(FPS)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        menu_basic(
            clock,
            track,
            player_car,
            computer_car,
            game_info,
            player_profile,
            "main menu",
            "main menu",
            click,
        )

        play_button = Button("Play", (255, 255, 255), 250, 200, "menu-button-large")
        if play_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_loop(clock, track, player_car, computer_car, game_info, player_profile)

        settings_button = Button(
            "Settings", (255, 255, 255), 250, 300, "menu-button-large"
        )
        if settings_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(
                clock, track, player_car, computer_car, game_info, player_profile
            )

        high_scores_button = Button(
            "records", (255, 255, 255), 250, 400, "menu-button-large"
        )
        if (
            high_scores_button.button_rect.collidepoint(pygame.mouse.get_pos())
            and click
        ):
            high_scores(
                clock, track, player_car, computer_car, game_info, player_profile
            )

        profiles_button = Button(
            "profiles", (255, 255, 255), 250, 500, "menu-button-large"
        )
        if profiles_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            profiles_settings(
                clock, track, player_car, computer_car, game_info, player_profile
            )

        pygame.display.update()


def main_game_loop():
    """Creates the game clock and initial required objects, and then runs main menu loop."""
    clock = pygame.time.Clock()

    player_profile = PlayerProfile("default")

    track = Track(player_profile.last_track_id)

    player_car = PlayerCar(player_profile.last_car_id, track.player_start_position)

    computer_car = ComputerCar(
        "black_car",
        track.computer_start_position,
        track.computer_path,
        track.track_record,
    )

    game_info = GameInfo()

    main_menu(clock, track, player_car, computer_car, game_info, player_profile)
