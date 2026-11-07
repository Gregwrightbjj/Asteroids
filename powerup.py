import random  # bring in Python's random-number tools; this file uses them to choose which direction a shield or speed-bonus item slowly moves
import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from circleshape import CircleShape  # look in circleshape.py and bring in the CircleShape class, a blueprint that gives each bonus item a position, speed/direction, size, and a function to reappear across screen edges
from constants import POWERUP_RADIUS, POWERUP_LIFETIME_SECONDS, POWERUP_COLORS, POWERUP_DRIFT_SPEED, LINE_WIDTH  # look in constants.py and bring in settings for shield/speed items: radius, time allowed for collection, colors, slow movement speed, and outline thickness


class PowerUp(CircleShape):  # define PowerUp, a blueprint for shield/speed items the ship collects by touching; (CircleShape) supplies their position and movement values, and the code below adds the item's bonus type and time before disappearing
    def __init__(self, x, y, kind):  # create a collectible item at coordinates x/y; kind must identify its effect as shield or speed
        super().__init__(x, y, POWERUP_RADIUS)  # run shared setup to store this collectible's position and 12-pixel circular size, then join its item, update, and drawing collections
        self.kind = kind  # save whether this item grants shield protection or a speed boost; main.py reads this value when the ship touches the item
        self.age = 0.0  # start the item's age at zero seconds so it can disappear after eight seconds if the ship does not collect it
        self.velocity = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * POWERUP_DRIFT_SPEED  # choose a random direction around a full circle and multiply it by the slow movement speed, making this collectible drift across the screen

    def update(self, dt):  # define how this shield/speed item changes each active frame: add elapsed seconds to its age, remove it if too old, otherwise move it slowly and handle screen edges
        self.age += dt  # increase this object's age by the seconds since the previous frame; += means add the value and save the result back
        if self.age >= POWERUP_LIFETIME_SECONDS:  # check whether this uncollected shield/speed item has existed for eight seconds; if so, remove it rather than leaving old bonuses everywhere
            self.kill()  # remove this object from all Pygame groups so the game stops updating, drawing, and checking it; the Python object can still be read
            return  # stop updating this item immediately after removing it, so an expired collectible is not moved again
        self.position += self.velocity * dt  # move this object by its horizontal/vertical speed multiplied by elapsed seconds, keeping movement consistent at different frame rates
        self.wrap()  # use CircleShape's edge helper so this collectible reappears on the opposite side if its slow movement carries it outside the window

    def draw(self, screen):  # define how this bonus item appears on the window; its stored kind chooses cyan for a shield or yellow for a speed boost
        pygame.draw.circle(screen, POWERUP_COLORS[self.kind], self.position, self.radius, LINE_WIDTH)  # draw this item's circular outline; look up its saved kind in POWERUP_COLORS so shield items appear cyan and speed-boost items appear yellow
