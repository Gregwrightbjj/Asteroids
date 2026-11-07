import random  # bring in Python's random-number tools; make_starfield() below uses them to give stars different screen positions, brightness, and sizes
from pathlib import Path  # bring in Path from Python's pathlib tools; Path builds file locations so load_background() can find an image inside this project's assets folder
import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # look in constants.py and bring in the window width and height; both background functions use them to make an image that fits the window


def make_starfield(star_count=150):  # define the function that builds the star image; star_count is the number of dots to draw, and =150 supplies that number automatically when main.py calls make_starfield() without an argument
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # create an image-like drawing area matching the window width and height; stars are drawn into this image once and reused during the game
    surface.fill("black")  # paint every pixel of the new image black before drawing stars, creating the empty-space background
    for _ in range(star_count):  # repeat the star-drawing instructions star_count times; _ holds each unused loop number because only the number of repetitions matters
        x = random.randrange(SCREEN_WIDTH)  # choose a whole-number horizontal coordinate from zero up to one less than the window width so the star stays inside the image
        y = random.randrange(SCREEN_HEIGHT)  # choose a whole-number vertical coordinate from zero up to one less than the window height so the star stays inside the image
        shade = random.randint(80, 255)  # choose star brightness from 80 through 255 inclusive; using the same value for red/green/blue makes shades of gray through white
        size = random.choice((1, 1, 2))  # randomly choose a radius of one or two pixels; listing 1 twice makes small stars twice as likely as larger stars
        pygame.draw.circle(surface, (shade,) * 3, (x, y), size)  # draw one filled star at x/y; (shade,) is a one-item tuple and multiplying it by three produces equal red, green, and blue color values
    return surface  # return the completed star image to main.py, which stores it and copies it onto the window at the start of each drawn frame


def load_background(filename="background.png"):  # define an optional function for using an image file instead of random stars; main.py currently does not call it, and it would need assets/background.png unless another filename were supplied
    path = Path(__file__).parent / "assets" / filename  # start with this Python file's folder and join the assets folder and requested filename; / joins path parts here rather than dividing numbers
    image = pygame.image.load(path).convert()  # load the image file and convert its pixels to match the display for faster copying; a display must already be opened and the file must exist
    return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # resize the loaded image to exactly the window dimensions and return that resized drawing surface to the caller
