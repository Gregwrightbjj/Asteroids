import pygame  # needed for pygame.draw.circle; each file needs its own imports
from circleshape import CircleShape  # the parent class we inherit from
from constants import SHOT_RADIUS, LINE_WIDTH  # bullet size and outline thickness


class Shot(CircleShape):  # T2: class = blueprint for objects; (CircleShape) = inherit position, velocity, radius
    def __init__(self, x, y):  # T2: constructor runs on creation; self = this object; accepts only x and y
        super().__init__(x, y, SHOT_RADIUS)  # super() = parent class; every bullet is the same size, so the radius is filled in here

    def draw(self, screen):  # override = same name as parent's draw, so this version runs instead
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)  # surface, color, center, radius, outline width

    def update(self, dt):  # override: moves the bullet in a straight line; dt = seconds since last frame
        self.position += self.velocity * dt  # velocity = speed + direction (Vector2); x dt = same speed on any computer. Ex: (0, 500) * 0.0167 = (0, 8.35) per frame