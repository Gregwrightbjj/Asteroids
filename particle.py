import random  # bring in Python's random-number tools; this file uses them to give explosion dots different lifetimes, travel directions, and speeds
import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from circleshape import CircleShape  # look in circleshape.py and bring in the CircleShape class, a blueprint that gives each explosion dot its own position, speed/direction, size, and membership in the drawing/update collections


class Particle(CircleShape):  # define Particle, a blueprint for one tiny explosion dot; (CircleShape) provides position and movement values, and the code below makes the dot fade and disappear over time
    def __init__(self, x, y, radius, lifetime):  # create one effect dot at coordinates x/y with a visible radius and a lifetime measured in seconds
        super().__init__(x, y, radius)  # run CircleShape's setup first so this object gets its position, zero starting velocity, radius, and membership in its assigned groups
        self.lifetime = lifetime  # store how many seconds this particular dot should remain visible before update() removes it from the game
        self.age = 0.0  # start this dot's age at zero seconds; its age is compared with its lifetime to decide both brightness and when to remove it

    def update(self, dt):  # define the function that ages and moves this particular explosion dot each frame; dt is the number of seconds that passed since the previous frame
        self.age += dt  # increase this object's age by the seconds since the previous frame; += means add the value and save the result back
        if self.age >= self.lifetime:  # check whether this dot has reached or passed its allowed lifetime, meaning it should now disappear from the effect
            self.kill()  # remove this object from all Pygame groups so the game stops updating, drawing, and checking it; the Python object can still be read
            return  # leave update() after removing an expired dot so the method does not keep moving it
        self.position += self.velocity * dt  # move this object by its horizontal/vertical speed multiplied by elapsed seconds, keeping movement consistent at different frame rates

    def draw(self, screen):  # define how this dot is drawn on the game window; calculate its brightness from its remaining lifetime so it gets darker before disappearing
        fade = 1 - self.age / self.lifetime  # calculate how much of the lifetime remains as a fraction: 1 means newly created and bright, while 0 means expired and dark
        shade = max(0, min(255, int(255 * fade)))  # turn the remaining-life fraction into a whole-number brightness and keep it between 0 and 255, the allowed range for each color channel
        pygame.draw.circle(screen, (shade, shade, shade), self.position, self.radius)  # draw a filled dot using equal red/green/blue values, producing gray that fades toward black as its remaining lifetime decreases


def spawn_explosion(position, count=12, max_speed=150):  # define the explosion-effect helper; create dots at position, using 12 dots and a 150-pixels-per-second maximum speed unless other values are supplied
    for _ in range(count):  # repeat the dot-creation instructions count times; _ is a variable name used because the loop number itself is not needed
        particle = Particle(position.x, position.y, 2, random.uniform(0.3, 0.8))  # create one dot at the explosion center with radius two pixels and a randomly chosen lifetime between 0.3 and 0.8 seconds
        direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))  # start with an arrow one unit long pointing right, then turn it by a random angle from 0 to 360 degrees; the next line gives this direction an actual travel speed
        particle.velocity = direction * random.uniform(30, max_speed)  # multiply the chosen direction by a random speed from 30 to max_speed pixels per second, making explosion dots spread at different rates
