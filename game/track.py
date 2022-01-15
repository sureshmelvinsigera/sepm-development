import pygame
from game.utilities import scale_image, blit_rotate_center, blit_text_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)