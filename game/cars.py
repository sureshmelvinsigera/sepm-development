import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

RED_CAR = scale_image(pygame.image.load("./imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("./imgs/green-car.png"), 0.55)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0