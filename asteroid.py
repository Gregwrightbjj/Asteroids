import random  # built-in random numbers
import pygame
from logger import log_event  # records events in game_events.jsonl
from circleshape import CircleShape  # parent class
from particle import spawn_explosion  # the explosion effect
from constants import (  # parentheses let one import span several lines
    LINE_WIDTH,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_VERTICES,
    ASTEROID_MAX_VERTICES,
    ASTEROID_LUMPINESS,
    ASTEROID_MAX_SPIN,
    SCORE_LARGE,
    SCORE_MEDIUM,
    SCORE_SMALL,
)


class Asteroid(CircleShape):  # (CircleShape) = inherit position, velocity, radius, wrap, collides_with
    def __init__(self, x: float, y: float, radius: float) -> None:  # float = decimal number; -> None = returns nothing
        super().__init__(x, y, radius)  # parent setup first
        self.angle = 0.0  # current spin angle in degrees
        self.spin = random.uniform(-ASTEROID_MAX_SPIN, ASTEROID_MAX_SPIN)  # degrees per second
        count = random.randint(ASTEROID_MIN_VERTICES, ASTEROID_MAX_VERTICES)  # number of corners
        self.offsets = []  # offset = a corner's position relative to the center
        for i in range(count):
            corner_angle = i * 360 / count  # spread corners evenly around the circle
            distance = radius * random.uniform(1 - ASTEROID_LUMPINESS, 1)  # pulled inward: shape never pokes outside the hitbox
            self.offsets.append(pygame.Vector2(distance, 0).rotate(corner_angle))  # rotate returns a NEW vector

    def draw(self, screen):  # override: lumpy polygon instead of a circle (the HITBOX is still a circle)
        points = [self.position + offset.rotate(self.angle) for offset in self.offsets]  # list comprehension: for each offset, spin it, then add the center
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)  # polygon = shape from points; width 2 = outline

    def update(self, dt: float) -> None:  # override
        self.angle += self.spin * dt  # tumble
        self.position += self.velocity * dt  # drift in a straight line
        self.wrap(ASTEROID_MAX_RADIUS)  # margin = spawn distance, so fresh spawns aren't teleported

    def points(self):  # asteroid knows its own size, so it says what it's worth
        if self.radius <= ASTEROID_MIN_RADIUS:  # small
            return SCORE_SMALL
        elif self.radius <= ASTEROID_MIN_RADIUS * 2:  # medium
            return SCORE_MEDIUM
        return SCORE_LARGE  # otherwise large

    def split(self):  # destroys this asteroid; big ones leave two smaller, faster ones
        spawn_explosion(self.position, count=int(self.radius / 2))  # radius 40 = 20 particles
        self.kill()  # always destroyed; position and radius still readable afterward

        if self.radius <= ASTEROID_MIN_RADIUS:  # small asteroid: just disappears
            return  # return = end the method now

        log_event("asteroid_split")  # text must match what the lesson tests expect

        random_angle = random.uniform(20, 50)  # random decimal between 20 and 50 degrees
        first_velocity = self.velocity.rotate(random_angle)  # new arrow, turned one way
        second_velocity = self.velocity.rotate(-random_angle)  # minus = the opposite way
        new_radius = self.radius - ASTEROID_MIN_RADIUS  # 60 -> 40, 40 -> 20

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)  # instantiate = create an object; joins groups via containers
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_velocity * 1.2  # number x arrow stretches it: 20% faster
        second_asteroid.velocity = second_velocity * 1.2