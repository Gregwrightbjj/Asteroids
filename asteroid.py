import random  # bring in Python's random-number tools; this file uses them to vary each rock's outline, spin speed, and the directions of the smaller rocks created when it splits
import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from logger import log_event  # look in logger.py and bring in log_event, a function that writes actions to game_events.jsonl; this file records when a rock splits into smaller rocks
from circleshape import CircleShape  # look in circleshape.py and bring in the CircleShape class, a blueprint that stores position, speed/direction, and size and supplies functions for checking contact and reappearing across screen edges
from particle import spawn_explosion  # look in particle.py and bring in spawn_explosion, a function that creates small moving dots; this file calls it when a rock is destroyed
from constants import (  # import the named settings below from constants.py; parentheses allow this one import statement to span several lines
    LINE_WIDTH,  # read the outline thickness from constants.py; draw() uses it when connecting the corner points of the visible rock
    ASTEROID_MIN_RADIUS,  # read the smallest allowed center-to-edge size; split() subtracts this amount when creating smaller rocks and stops splitting once this size is reached
    ASTEROID_MAX_RADIUS,  # read the largest rock size; update() uses this as the distance beyond a screen edge that a rock may travel before reappearing across the window
    ASTEROID_MIN_VERTICES,  # read the lowest allowed number of outline corners; vertices is the math word for these corner points
    ASTEROID_MAX_VERTICES,  # read the highest allowed number of outline corners; each new rock randomly chooses a count between the minimum and maximum
    ASTEROID_LUMPINESS,  # read how far outline corners may be pulled toward the center; varying these distances makes rocks uneven instead of perfectly round
    ASTEROID_MAX_SPIN,  # read the greatest turning speed allowed in degrees per second; each rock chooses a speed between this negative and positive limit
    SCORE_LARGE,  # bring in the points awarded for a large rock; points() returns this amount when the rock is bigger than the medium-size cutoff
    SCORE_MEDIUM,  # bring in the points awarded for a medium rock; points() returns this amount for a rock bigger than small but no bigger than twice the minimum radius
    SCORE_SMALL,  # bring in the points awarded for a small rock; points() returns this amount for the smallest size, which is worth the most points
)


class Asteroid(CircleShape):  # define Asteroid, a blueprint for making rocks; (CircleShape) means use that existing blueprint's position, motion values, and contact checks, then add rock shape, spinning, and splitting below
    def __init__(self, x: float, y: float, radius: float) -> None:  # set up each new rock at coordinates x/y with the supplied radius; float describes decimal-number arguments and -> None means no returned result
        super().__init__(x, y, radius)  # run CircleShape's setup first so this object gets its position, zero starting velocity, radius, and membership in its assigned groups
        self.angle = 0.0  # start the visible rock outline at zero degrees of rotation; this angle changes over time to make the rock appear to tumble
        self.spin = random.uniform(-ASTEROID_MAX_SPIN, ASTEROID_MAX_SPIN)  # choose a decimal rotation speed between -45 and 45 degrees per second; the sign determines which way this particular rock spins
        count = random.randint(ASTEROID_MIN_VERTICES, ASTEROID_MAX_VERTICES)  # choose a whole number of corners between 9 and 14 inclusive, giving each rock a different number of outline points
        self.offsets = []  # start an empty list of corner offsets; each offset is a point measured relative to the rock's center rather than an absolute screen location
        for i in range(count):  # repeat once for each corner, using i values from zero through count minus one to calculate positions around a full circle
            corner_angle = i * 360 / count  # divide the full 360-degree circle into equal angular steps, giving this corner its direction around the center
            distance = radius * random.uniform(1 - ASTEROID_LUMPINESS, 1)  # choose this corner's distance between 70% and 100% of the radius, making a lumpy outline that remains inside the circular collision area
            self.offsets.append(pygame.Vector2(distance, 0).rotate(corner_angle))  # make a sideways arrow of the chosen length, rotate it to this corner's angle, and append it to the list of relative corner positions

    def draw(self, screen):  # define what to draw when main.py calls this rock's draw function; connect its corners into an uneven outline, while contact checks continue to use a circle covering the rock
        points = [self.position + offset.rotate(self.angle) for offset in self.offsets]  # build a list of screen corner positions by rotating each stored offset to the current spin angle and adding the rock center; this compact loop is a list comprehension
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)  # connect the calculated corner positions to draw the rock's white outline; LINE_WIDTH controls how thick that outline appears

    def update(self, dt: float) -> None:  # define what changes for this rock each active frame: turn its outline, move its center, and reappear across the window if it has gone beyond an edge; dt is elapsed seconds
        self.angle += self.spin * dt  # advance the visible rotation by degrees-per-second times elapsed seconds, making this rock spin smoothly at its own randomly chosen rate
        self.position += self.velocity * dt  # move this object by its horizontal/vertical speed multiplied by elapsed seconds, keeping movement consistent at different frame rates
        self.wrap(ASTEROID_MAX_RADIUS)  # reappear across the screen only after traveling a full maximum-rock radius beyond an edge, matching where new rocks are created so they are not moved across immediately

    def points(self):  # define how many points this rock is worth; the code that handles a bullet or bomb hit calls this function and adds the returned number to the score
        if self.radius <= ASTEROID_MIN_RADIUS:  # check whether the rock's radius is 20 pixels or less; this selects the small-rock reward returned on the next line
            return SCORE_SMALL  # return the small-rock reward of 100 points and leave this method immediately
        elif self.radius <= ASTEROID_MIN_RADIUS * 2:  # if it was not small, check whether its radius is at most 40 pixels, which identifies a medium rock
            return SCORE_MEDIUM  # return the medium-rock reward of 50 points and leave this method immediately
        return SCORE_LARGE  # if neither smaller-size condition matched, return the large-rock reward of 20 points

    def split(self):  # destroy this rock and create its explosion; if it is larger than the minimum size, replace it with two smaller rocks traveling in different directions
        spawn_explosion(self.position, count=int(self.radius / 2))  # create moving effect dots at this rock's center; dividing the radius by two makes larger rocks produce more dots, and int ensures a whole-number count
        self.kill()  # remove this object from all Pygame groups so the game stops updating, drawing, and checking it; the Python object can still be read

        if self.radius <= ASTEROID_MIN_RADIUS:  # check whether this rock is already the minimum size; if so, stop after its explosion because it must not create even smaller rocks
            return  # stop running this function now and return control to the code that called it; no result value is supplied

        log_event("asteroid_split")  # record the exact event name asteroid_split in the course log when a medium or large rock produces smaller rocks

        random_angle = random.uniform(20, 50)  # choose a decimal angle between 20 and 50 degrees to separate the two replacement rocks' travel directions
        first_velocity = self.velocity.rotate(random_angle)  # copy the original movement vector and turn it by the chosen positive angle to aim the first replacement rock
        second_velocity = self.velocity.rotate(-random_angle)  # copy the original movement vector and turn it by the opposite angle so the second replacement rock travels away from the first
        new_radius = self.radius - ASTEROID_MIN_RADIUS  # reduce the replacement rocks' radius by 20 pixels, turning radius 60 into 40 or radius 40 into 20

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)  # create the first smaller rock at the destroyed rock's center; its inherited setup automatically joins the rock, update, and drawing groups
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)  # create a second independent smaller rock at the same center with the same new radius; it will receive a different movement direction
        first_asteroid.velocity = first_velocity * 1.2  # give the first replacement rock its turned movement vector multiplied by 1.2, making it move 20% faster than the original rock
        second_asteroid.velocity = second_velocity * 1.2  # give the second replacement rock the opposite turned vector and the same 20% speed increase
