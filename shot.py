import pygame  # load Pygame so this file can draw each bullet as a circle on the game window
from circleshape import CircleShape  # look in circleshape.py and bring in the CircleShape class, a blueprint that gives each bullet its own position, speed/direction, size, and function for checking whether it touches another circle
from constants import SHOT_RADIUS, SHOT_LIFETIME_SECONDS, LINE_WIDTH  # look in constants.py and bring in three settings: the default bullet radius, its lifetime in seconds, and the thickness of its visible outline


class Shot(CircleShape):  # define Shot, a blueprint for bullets; (CircleShape) means start with that blueprint's position, motion values, and contact checks, then add the bullet-specific code below
    def __init__(self, x, y, radius=SHOT_RADIUS, pierce=False):  # create a bullet at x/y; if the caller omits size or piercing behavior, use the default radius and make the bullet disappear after a hit
        super().__init__(x, y, radius)  # run CircleShape's setup to store the bullet position and size, start its velocity at zero, and join its assigned collections; the ship then sets its firing velocity
        self.pierce = pierce  # remember whether this bullet survives hitting a rock; True allows continued travel, while False makes main.py remove it on impact
        self.age = 0.0  # start the bullet's age at zero seconds so update() can remove it after the configured lifetime

    def draw(self, screen):  # define the function main.py calls to draw this particular bullet; this replaces CircleShape's do-nothing draw function with the circle-drawing instruction below
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)  # draw a white circular bullet outline on screen; its center is self.position, its size is self.radius, and LINE_WIDTH sets the outline thickness

    def update(self, dt):  # advance the bullet once per active frame: increase its age, remove it if expired, otherwise move it along its firing direction
        self.age += dt  # increase this object's age by the seconds since the previous frame; += means add the value and save the result back
        if self.age >= SHOT_LIFETIME_SECONDS:  # check whether the bullet has been alive for at least 1.5 seconds; >= means equal to or greater than that lifetime
            self.kill()  # remove this object from all Pygame groups so the game stops updating, drawing, and checking it; the Python object can still be read
            return  # stop this update immediately after removing an expired bullet, preventing the rest of this method from moving it again
        self.position += self.velocity * dt  # move this object by its horizontal/vertical speed multiplied by elapsed seconds, keeping movement consistent at different frame rates
