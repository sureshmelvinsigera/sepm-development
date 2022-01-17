import pygame
from game.loops import main_game_loop
from db_build import build_db

build_db()

main_game_loop()

pygame.quit()
