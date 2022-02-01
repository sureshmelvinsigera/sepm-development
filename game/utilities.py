import pygame


def scale_image(image, factor):
    """Scales an image by the passed in scale factor.

    Args:
        image -- the image file to be scaled.
        factor -- the scale factor.
    """
    size = round(image.get_width() * factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, size)


def blit_rotate_center(win, image, top_left, angle):
    """Rotates an image around its centre point, rather than around the top left corner.

    Args:
        win -- window, or surface, the image will be drawn on.
        image -- image to be rotated and drawn.
        top_left -- (x, y) co-ordinate of the top left corner.
        angle -- rotation angle.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    """Prints text on the centre of the game window.

    Args:
        win -- window, or surface, the text will be printed on.
        font -- text font.
        text -- the text to be printed on the window.
    """
    render = font.render(text, 1, (200, 200, 200))
    win.blit(
        render,
        (
            win.get_width() / 2 - render.get_width() / 2,
            win.get_height() / 2 - render.get_height() / 2,
        ),
    )


def draw_computer_path(click, computer_car, track, win):
    """Draws the computer car's path as a series of red dots.

    Args:
        click -- boolean based on if the player clicked their mouse or not.
        computer_car -- current ComputerCar object.
        track -- current Track object.
        win -- the game window for dots to be drawn on.
    """
    if click:
        new_path_point = pygame.mouse.get_pos()
        path_x, path_y = new_path_point
        print(
            f"- model: path\n  track_id: {track.track_id}\n  path_x: {path_x}\n  path_y: {path_y}\n"
        )
    computer_car.draw_points(win)


def censor_word(word):
    if word:
        censored_word = str(word[0] + ("*" * len(word[1:-1])) + word[-1])
        return censored_word
    return ""
