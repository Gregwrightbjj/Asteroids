import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from circleshape import CircleShape  # look in circleshape.py and bring in the CircleShape class, a blueprint that stores this bomb's position and size and adds it to the collections chosen in main.py
from constants import BOMB_RADIUS, BOMB_FUSE_SECONDS, LINE_WIDTH  # look in constants.py and bring in the bomb's visible radius, the seconds to wait before exploding, and the thickness of its outline


class Bomb(CircleShape):  # define Bomb, a blueprint for creating bombs; (CircleShape) supplies position and size, while the code below adds the explosion countdown and flashing appearance
    def __init__(self, x, y):  # define the setup Python runs when Bomb(x, y) creates a bomb; self refers to that particular bomb and x/y are the ship's coordinates when it was dropped
        super().__init__(x, y, BOMB_RADIUS)  # run the shared setup to place the bomb at x/y, give it an eight-pixel radius, and join its update, drawing, and bomb collections
        self.fuse = BOMB_FUSE_SECONDS  # start the two-second countdown before explosion; a fuse is the delay between dropping this bomb and setting it off
        self.detonated = False  # start with the explosion signal turned off; main.py checks this True/False value to know when to apply damage to nearby rocks

    def update(self, dt):  # define the function the update collection calls for this bomb each frame; dt is the elapsed seconds to subtract from its explosion countdown
        self.fuse -= dt  # subtract the elapsed frame time from the seconds remaining before explosion; -= means subtract and store the updated value
        if self.fuse <= 0:  # check whether the bomb's waiting time has run out, including a timer that passed slightly below zero during the last frame
            self.detonated = True  # turn on the explosion signal; main.py then destroys rocks inside the blast radius, creates the visual effect, and removes this bomb

    def draw(self, screen):  # define how this particular bomb appears on the game window; screen is the place to draw, and the next lines alternate its outline between red and white
        color = "red" if int(self.fuse * 6) % 2 == 0 else "white"  # switch between red and white as the countdown changes; int makes a whole number and % 2 checks whether it is even, producing the flashing effect
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)  # draw the bomb's circular outline at its stored position using the selected flashing color, its visible radius, and the shared line thickness
