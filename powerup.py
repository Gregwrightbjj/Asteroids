import random
import pygame
from circleshape import CircleShape
from constants import POWERUP_RADIUS, POWERUP_LIFETIME_SECONDS, POWERUP_COLORS, POWERUP_DRIFT_SPEED, LINE_WIDTH


class PowerUp(CircleShape):  # a pickup the player collects by touching it
    def __init__(self, x, y, kind):  # kind = "shield" or "speed"
        super().__init__(x, y, POWERUP_RADIUS)
        self.kind = kind
        self.age = 0.0  # seconds alive
        self.velocity = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * POWERUP_DRIFT_SPEED  # slow drift in a random direction

    def update(self, dt):
        self.age += dt
        if self.age >= POWERUP_LIFETIME_SECONDS:  # uncollected: disappears
            self.kill()
            return
        self.position += self.velocity * dt
        self.wrap()  # leaves one side, returns on the other

    def draw(self, screen):
        pygame.draw.circle(screen, POWERUP_COLORS[self.kind], self.position, self.radius, LINE_WIDTH)  # dictionary lookup picks the color