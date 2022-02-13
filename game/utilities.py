import pygame


def scale_image(image, factor):
    """Scales an image by the passed in scale factor.

    Args:
        image -- the image file to be scaled.
        factor -- the scale factor.
    """
    # finds the new width and height of the image as tuple
    size = round(image.get_width() * factor), round(image.get_height() * factor)
    # returns the new image, scaled appropriately
    return pygame.transform.scale(image, size)


def blit_rotate_center(win, image, top_left, angle):
    """Rotates an image around its centre point, rather than around the top left corner.

    Args:
        win -- window, or surface, the image will be drawn on.
        image -- image to be rotated and drawn.
        top_left -- (x, y) co-ordinate of the top left corner.
        angle -- rotation angle.
    """
    # rotates the image about its top  left corner
    rotated_image = pygame.transform.rotate(image, angle)
    # new rect adjusting centre  to the centre of the image before rotation
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    # draws image onto new rect
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    """Prints text on the centre of the game window.

    Args:
        win -- window, or surface, the text will be printed on.
        font -- text font.
        text -- the text to be printed on the window.
    """
    # renders grey text  in passed in font
    render = font.render(text, 1, (0, 0, 0))
    # draws text onto the centre of the game window
    win.blit(
        render,
        (
            win.get_width() / 2 - render.get_width() / 2,
            win.get_height() / 2 - render.get_height() / 2,
        ),
    )


def draw_computer_path(click, computer_car, track, win):
    """Draws the computer car's path as a series of red dots. Prints new points if mouse click.

    Args:
        click -- boolean based on if the player clicked their mouse or not.
        computer_car -- current ComputerCar object.
        track -- current Track object.
        win -- the game window for dots to be drawn on.
    """

    if click:
        # gets the (x, y) co-ord of the mouse if the user clicks the mouse button.
        path_x, path_y = pygame.mouse.get_pos()

        # prints the mouse co-ords formatted such that they can be copied directly into the path.yaml database file.
        print(
            f"- model: path\n  track_id: {track.track_id}\n  path_x: {path_x}\n  path_y: {path_y}\n"
        )

    # draws the current car path points as red dots .
    computer_car.draw_points(win)


def censor_word(word):
    """Censors the given word using asterisk's for padding.

    Args:
        word -- string containing the word to be censored
    """
    if word:
        censored_word = str(word[0] + ("*" * len(word[1:-1])) + word[-1])
        return censored_word
    return ""
