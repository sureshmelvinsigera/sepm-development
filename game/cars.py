from math import atan, cos, degrees, pi, radians, sin

import pygame

from database import models
from game.utilities import blit_rotate_center, scale_image


class Car:
    def __init__(self, car_id, start_position):
        """
        Args:
              car_id -- car id string for database look up.
              start_position -- current track's relevant start position.
        """
        lookup_car = models.Car.get(models.Car.car_id == car_id)
        self.car_id = lookup_car.car_id
        self.car_name = lookup_car.car_name
        self.car_path = lookup_car.car_path
        self.max_vel = lookup_car.max_vel
        self.rotation_vel = lookup_car.rotation_vel
        self.acceleration = lookup_car.acceleration / 10

        self.car_image = pygame.image.load(self.car_path)

        self.vel = 0
        self.angle = 0

        self.start_position = start_position
        self.x, self.y = self.start_position

    def draw(self, win):
        """Draws the car and rotates it around its centre point as appropriate.

        Args:
            win -- game window to draw on.
        """
        # rotates the car to the appropriate angle around its centre point and draws it
        blit_rotate_center(win, self.car_image, (self.x, self.y), self.angle)

    def move(self):
        """Moves the car using the horizontal and vertical components of its velocity."""
        vertical = cos(radians(self.angle)) * self.vel
        horizontal = sin(radians(self.angle)) * self.vel

        # adjusts the x and y co-ords of the car
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        """Returns the point of intersection between the car and the passed in image mask.

        Args:
            mask -- mask to check for collision with.
            x -- x co-ord of the mask.
            y -- y co-ord of the mask.
        """
        # makes mask form car image
        car_mask = pygame.mask.from_surface(self.car_image)
        offset = (int(self.x - x), int(self.y - y))

        # checks for overlap between car and track masks
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        """Resets car to start position."""
        self.x, self.y = self.start_position
        self.angle = 0
        self.vel = 0


class PlayerCar(Car):
    def bounce(self):
        """Reverses direction if the car collides with the track."""
        self.vel = -self.vel / 2        # reverses velocity direction and halves
        self.move()     # moves car with new velocity

    def move_player(self):
        """Controls for player movement based on the key input."""
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT]:
            # rotates car to the left if the left arrow key if pressed.
            self.angle += self.rotation_vel
        if keys[pygame.K_RIGHT]:
            # rotates car to the right if the right arrow key if pressed.
            self.angle -= self.rotation_vel
        if keys[pygame.K_UP]:
            # moves forward if the up arrow key is pressed
            moved = True
            # accelerates if max velocity not reached
            self.vel = min(self.vel + self.acceleration, self.max_vel)
            self.move()
        if keys[pygame.K_DOWN]:
            # moves backwards if the down arrow key is pressed
            moved = True
            # decelerates if half max velocity not reached
            self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
            self.move()

        if not moved:
            # slows down the car if neither up nor down arrow pressed
            self.vel = max(self.vel - self.acceleration / 2, 0)
            self.move()


# Path_new is to be swapped with path when complete
class ComputerCar(Car):
    def __init__(self, car_id, start_position, path, track_record):
        """
        Args:
              car_id -- car id string for database look up.
              start_position -- current track's relevant start position.
              path -- the current track's computer path.
              track_record -- the current track's record.
        """
        super().__init__(car_id, start_position)
        self.path = path
        self.current_point = 0
        self.track_record = track_record
        self.vel = self.max_vel // 1.25

    def draw_points(self, win):
        """Draws the computer car's path as a series of red dots.

        Args:
            win -- game window to draw on.
        """
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), (point.path_x, point.path_y), 5)

    def calculate_angle(self):
        """Calculates the angle between the car's current vector and the next point on the car's path,
        and adjusts the car's rotation appropriately."""
        target_x = list(self.path)[self.current_point].path_x
        target_y = list(self.path)[self.current_point].path_y
        x_delta = target_x - self.x     # horizontal distance to travel
        y_delta = target_y - self.y     # vertical distance to travel

        if y_delta == 0:
            # if no vertical distance to travel then desired rotation is pi/2 rad
            desired_angle = pi / 2
        else:
            # arc tangent finds
            desired_angle = atan(x_delta / y_delta)

        if target_y > self.y:
            # if moving downwards, adding pi to desired angle is required as atan() range is -pi/2 < x < pi/2
            desired_angle += pi

        if desired_angle > 2 * pi:
            # angle and (angle - 2pi) are equivalent.
            desired_angle -= 2 * pi

        difference_in_angle = self.angle - degrees(desired_angle)
        # brings angle back between -180 and 180
        if difference_in_angle >= 180:
            difference_in_angle -= 360
        if difference_in_angle < -180:
            difference_in_angle += 360

        # rotates by the calculated angle or rotation vel, depending on which is smaller
        # -= or += depending on direction
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        """Increments the current point if the car collides with the current target point in the path."""
        # next point in car path
        target = list(self.path)[self.current_point]
        # car rectangle
        rect = pygame.Rect(
            self.x, self.y, self.car_image.get_width(), self.car_image.get_height()
        )

        # changes target to next point in path by incrementing current_point if car collides with current target
        if rect.collidepoint(target.path_x, target.path_y):
            self.current_point += 1

    def move(self):
        """Moves the computer car if the car hasn't reached the end of its path"""
        if self.current_point < len(self.path):
            self.calculate_angle()      # calculates angle and rotates car
            self.update_path_point()        # updates path if necessary
            super().move()      # moves car using move method from Car
