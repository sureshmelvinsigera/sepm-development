import pygame
from game.loops import main_game_loop, clock
from db_build import build_db

build_db()

main_game_loop(clock)

pygame.quit()
