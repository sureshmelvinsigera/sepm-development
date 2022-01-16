import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
from game.cars import AbstractCar, PlayerCar, ComputerCar, RED_CAR, GREEN_CAR
from game.track import GRASS, TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_POSITION, FINISH_MASK

