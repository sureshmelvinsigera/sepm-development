import pygame
from game.loops import main_game_loop
from db_build import build_db
from config import con, cur


build_db()

main_game_loop()

pygame.quit()
