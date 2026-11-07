import random
from pathlib import Path  # Path = a file location you can build safely
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def make_starfield(star_count=150):  # builds ONE picture of random stars (no image file needed)
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # a blank picture
    surface.fill("black")
    for _ in range(star_count):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        shade = random.randint(80, 255)  # dim to bright
        size = random.choice((1, 1, 2))  # mostly tiny, a few bigger
        pygame.draw.circle(surface, (shade,) * 3, (x, y), size)  # (shade,) * 3 repeats it: (shade, shade, shade) = gray
    return surface


def load_background(filename="background.png"):  # alternative: use a picture from an assets folder
    path = Path(__file__).parent / "assets" / filename  # this file's folder + assets + filename
    image = pygame.image.load(path).convert()  # convert() speeds up drawing; call it AFTER set_mode
    return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # resize to fit the window