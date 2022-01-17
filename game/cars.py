import pygame
import time
import math
from game.utilities import scale_image, blit_rotate_center, blit_text_center
from config import con, cur


pygame.font.init()


class AbstractCar:

    def __init__(self, car_id, start_position):
        self.car_id = car_id
        self.car_name = cur.execute("""SELECT car_name FROM cars WHERE car_id = ?""",
                                    (self.car_id,)).fetchone()[0]
        self.car_path = cur.execute("""SELECT car_path FROM cars WHERE car_id = ?""",
                                    (self.car_id,)).fetchone()[0]
        self.max_vel = cur.execute("""SELECT max_vel FROM cars WHERE car_id = ?""",
                                    (self.car_id,)).fetchone()[0]
        self.rotation_vel = cur.execute("""SELECT rotation_vel FROM cars WHERE car_id = ?""",
                                    (self.car_id,)).fetchone()[0]
        self.acceleration = cur.execute("""SELECT acceleration FROM cars WHERE car_id = ?""",
                                    (self.car_id,)).fetchone()[0] / 10

        self.img = scale_image(pygame.image.load(self.car_path), 0.55)

        self.vel = 0
        self.angle = 0

        self.start_position = start_position
        self.x, self.y = self.start_position

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
        self.x, self.y = self.start_position
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def move_player(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT]:
            self.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            self.rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            self.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            self.move_backward()

        if not moved:
            self.reduce_speed()


class ComputerCar(AbstractCar):

    def __init__(self, car_id, start_position, path=[]):
        super().__init__(car_id, start_position)
        self.path = path
        self.current_point = 0
        self.vel = self.max_vel // 1.25

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
