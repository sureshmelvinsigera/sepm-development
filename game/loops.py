import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
from game.cars import PlayerCar, ComputerCar
from game.track import Track

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
        return round(time.time() - self.level_start_time)


def menu_button_text(game_info, button_text, x, y):
    text = game_info.main_font.render(button_text, 1, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    game_info.win.blit(text, text_rect)


def menu_title(game_info, menu_name):
    text = game_info.main_font.render(menu_name, 1, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (300, 50)
    game_info.win.blit(text, text_rect)


def draw_main(images, player_car, computer_car, game_info):
    for img, pos in images:
        game_info.win.blit(img, pos)

    time_text = game_info.main_font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    game_info.win.blit(time_text, (10, game_info.height - time_text.get_height() - 40))

    computer_car.draw(game_info.win)
    player_car.draw(game_info.win)
    pygame.display.update()


def handle_collision(track, player_car, computer_car, game_info):
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
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        track.finish_mask, *track.finish_position)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            blit_text_center(game_info.win, game_info.main_font, "You Win!")
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.reset()


def game_loop(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        for img, pos in images:
            game_info.win.blit(img, pos)

        time_text = game_info.main_font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
        game_info.win.blit(time_text, (10, game_info.height - time_text.get_height() - 40))

        computer_car.draw(game_info.win)
        player_car.draw(game_info.win)
        main_menu_button = pygame.Rect(10, 10, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), main_menu_button)
        menu_button_text(game_info, 'Menu', 10, 10)

        pygame.display.update()

        while not game_info.started:
            blit_text_center(game_info.win, game_info.main_font, "Press any key to start!")
            pygame.display.update()

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

                if main_menu_button.collidepoint(pygame.mouse.get_pos()):
                    if click:
                        main_menu(run, clock, track, player_car, computer_car, game_info, images)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if main_menu_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                main_menu(run, clock, track, player_car, computer_car, game_info, images)

        player_car.move_player()
        computer_car.move()

        handle_collision(track, player_car, computer_car, game_info)


def settings_loop(run, clock, track, player_car, computer_car, game_info, images):

    while run:
        clock.tick(FPS)

        game_info.win.fill((0, 0, 0))

        back_button = pygame.Rect(50, 50, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), back_button)
        menu_button_text(game_info, 'Back', 50, 50)

        menu_title(game_info, "Settings")

        car_button = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), car_button)
        menu_button_text(game_info, 'Car', 300, 200)

        track_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), track_button)
        menu_button_text(game_info, 'Track', 300, 300)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                main_menu(run, clock, track, player_car, computer_car, game_info, images)

        if car_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                car_settings(run, clock, track, player_car, computer_car, game_info, images)

        if track_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                track_settings(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def car_settings(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        game_info.win.fill((0, 0, 0))

        back_button = pygame.Rect(50, 50, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), back_button)
        menu_button_text(game_info, 'Back', 50, 50)

        menu_title(game_info, "Cars")

        green_button = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), green_button)
        menu_button_text(game_info, 'Green', 300, 200)

        purple_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), purple_button)
        menu_button_text(game_info, 'Purple', 300, 300)

        red_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), red_button)
        menu_button_text(game_info, 'Red', 300, 400)

        white_button = pygame.Rect(300, 500, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), white_button)
        menu_button_text(game_info, 'White', 300, 500)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if green_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                player_car = PlayerCar('green_car', track.player_start_position)
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if purple_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                player_car = PlayerCar('purple_car', track.player_start_position)
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if red_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                player_car = PlayerCar('red_car', track.player_start_position)
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if white_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                player_car = PlayerCar('white_car', track.player_start_position)
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def track_settings(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        game_info.win.fill((0, 0, 0))

        back_button = pygame.Rect(50, 50, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), back_button)
        menu_button_text(game_info, 'Back', 50, 50)

        menu_title(game_info, "Tracks")

        track_1_button = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), track_1_button)
        menu_button_text(game_info, 'Track 1', 300, 200)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        if track_1_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                track = Track('track_1')
                player_car.start_position = track.player_start_position
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

        pygame.display.update()


def main_menu(run, clock, track, player_car, computer_car, game_info, images):
    while run:
        clock.tick(FPS)

        game_info.win.fill((0, 0, 0))

        menu_title(game_info, 'Main Menu')

        play_button = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), play_button)
        menu_button_text(game_info, 'Play', 300, 200)

        settings_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(game_info.win, (255, 0, 0), settings_button)
        menu_button_text(game_info, 'Settings', 300, 300)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if play_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                game_loop(run, clock, track, player_car, computer_car, game_info, images)

        if settings_button.collidepoint(pygame.mouse.get_pos()):
            if click:
                settings_loop(run, clock, track, player_car, computer_car, game_info, images)

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
