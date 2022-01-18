import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
from game.cars import PlayerCar, ComputerCar, AbstractCar
from game.track import Track
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
    text_rect.topleft = (300, 50)
    game_info.win.blit(text, text_rect)


def high_score_name_entry(run, clock, track, player_car, computer_car, game_info, images, time):
    name = ''

    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        main_menu_button = Button(game_info, 'menu', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

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
                        game_loop(run, clock, track, player_car, computer_car, game_info, images)
                    else:
                        game_loop(run, clock, track, player_car, computer_car, game_info, images)
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 8:
                    name += event.unicode

        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()):
            if click:
                game_info.reset()
                player_car.reset()
                computer_car.reset()
                main_menu(run, clock, track, player_car, computer_car, game_info, images)

        if done_button.button_rect.collidepoint(pygame.mouse.get_pos()):
            if click:
                if len(name) != 0:
                    cur.execute("""INSERT INTO high_scores VALUES (?, ?, ?)""",
                                (name, time, track.track_id))
                    con.commit()
                    game_loop(run, clock, track, player_car, computer_car, game_info, images)
                else:
                    game_loop(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def handle_collision(run, clock, track, player_car, computer_car, game_info, images):
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
        computer_car = ComputerCar('grey_car', track.computer_start_position, PATH)
        game_loop(run, clock, track, player_car, computer_car, game_info, images)

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
            computer_car = ComputerCar('grey_car', track.computer_start_position, PATH)
            high_score_name_entry(run, clock, track, player_car, computer_car, game_info, images, time)


def game_loop(run, clock, track, player_car, computer_car, game_info, images):
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

                if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
                    game_info.reset()
                    player_car.reset()
                    computer_car.reset()
                    main_menu(run, clock, track, player_car, computer_car, game_info, images)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if main_menu_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_info.reset()
            player_car.reset()
            computer_car.reset()
            main_menu(run, clock, track, player_car, computer_car, game_info, images)

        player_car.move_player()
        computer_car.move()

        handle_collision(run, clock, track, player_car, computer_car, game_info, images)


def settings_loop(run, clock, track, player_car, computer_car, game_info, images):

    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

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
            main_menu(run, clock, track, player_car, computer_car, game_info, images)

        if car_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            car_settings(run, clock, track, player_car, computer_car, game_info, images)

        if track_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            track_settings(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def car_settings(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "Cars")

        green_button = Button(game_info, 'Green', (255, 255, 255), 10, 200, 200, 50, (255, 0, 0))
        green_stats = cur.execute(
                                """
                                SELECT max_vel, rotation_vel, acceleration
                                FROM cars 
                                WHERE car_id = 'green_car'
                                """
                                ).fetchall()

        purple_button = Button(game_info, 'Purple', (255, 255, 255), 10, 300, 200, 50, (255, 0, 0))
        purple_stats = cur.execute(
                                """
                                SELECT max_vel, rotation_vel, acceleration
                                FROM cars
                                WHERE car_id = 'purple_car'
                                """
                                ).fetchall()

        red_button = Button(game_info, 'red', (255, 255, 255), 10, 400, 200, 50, (255, 0, 0))
        red_stats = cur.execute(
                                """
                                SELECT max_vel, rotation_vel, acceleration
                                FROM cars
                                WHERE car_id = 'red_car'
                                """
                                ).fetchall()

        white_button = Button(game_info, 'white', (255, 255, 255), 10, 500, 200, 50, (255, 0, 0))
        white_stats = cur.execute(
                                """
                                SELECT max_vel, rotation_vel, acceleration
                                FROM cars
                                WHERE car_id = 'white_car'
                                """
                                ).fetchall()

        stats = [green_stats, purple_stats, red_stats, white_stats]
        stats_y = green_button.y + green_button.height/2 - green_button.render_text.get_height()/2
        for car in stats:
            for speed, hand, acc in car:
                menu_button_text(game_info, f"Speed:{speed}    Hand:{hand}    Acc:{acc}", 200, stats_y)
            stats_y += 100

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if green_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_car = PlayerCar('green_car', track.player_start_position)

        if purple_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_car = PlayerCar('purple_car', track.player_start_position)

        if red_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_car = PlayerCar('red_car', track.player_start_position)

        if white_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            player_car = PlayerCar('white_car', track.player_start_position)

        pygame.display.update()


def track_settings(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

        menu_title(game_info, "Tracks")

        track_1_button = Button(game_info, 'Track 1', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if back_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if track_1_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            track = Track('track_1')
            player_car.start_position = track.player_start_position
            computer_car.start_position = track.computer_start_position

        pygame.display.update()


def high_scores(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        back_button = Button(game_info, 'Back', (255, 255, 255), 10, 10, 200, 50, (255, 0, 0))

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
            main_menu(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def main_menu(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)

        menu_title(game_info, 'Main Menu')

        play_button = Button(game_info, 'Play', (255, 255, 255), 300, 200, 200, 50, (255, 0, 0))
        settings_button = Button(game_info, 'Settings', (255, 255, 255), 300, 300, 200, 50, (255, 0, 0))
        high_scores_button = Button(game_info, 'High Scores', (255, 255, 255), 300, 400, 200, 50, (255, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if play_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            game_loop(run, clock, track, player_car, computer_car, game_info, images)

        if settings_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if high_scores_button.button_rect.collidepoint(pygame.mouse.get_pos()) and click:
            high_scores(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def main_game_loop():

    run = True

    clock = pygame.time.Clock()

    track = Track("track_1")

    player_car = PlayerCar('red_car', track.player_start_position)

    computer_car = ComputerCar('grey_car', track.computer_start_position, PATH)

    game_info = GameInfo(WIN, WIDTH, HEIGHT, MAIN_FONT)

    images = [(track.background_image, (0, 0)), (track.track_image, (0, 0)),
              (track.finish_image, track.finish_position), (track.border_image, (0, 0))]

    main_menu(run, clock, track, player_car, computer_car, game_info, images)
