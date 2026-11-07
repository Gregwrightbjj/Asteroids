import random  # built-in random numbers
import pygame
from circleshape import CircleShape


class Particle(CircleShape):  # particle = tiny short-lived object used for effects
    def __init__(self, x, y, radius, lifetime):
        super().__init__(x, y, radius)
        self.lifetime = lifetime  # seconds this particle lives
        self.age = 0.0  # seconds lived so far

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:  # expired
            self.kill()  # remove from all groups
            return
        self.position += self.velocity * dt  # drift along its velocity

    def draw(self, screen):
        fade = 1 - self.age / self.lifetime  # 1.0 when new, 0.0 when expiring
        shade = max(0, min(255, int(255 * fade)))  # keep the color value between 0 and 255 (max/min clamp it)
        pygame.draw.circle(screen, (shade, shade, shade), self.position, self.radius)  # no width = filled; gray fading to black


def spawn_explosion(position, count=12, max_speed=150):  # makes `count` particles at one spot
    for _ in range(count):  # _ = a loop variable we don't need
        particle = Particle(position.x, position.y, 2, random.uniform(0.3, 0.8))  # radius 2, lives 0.3 to 0.8 s
        direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))  # random direction (rotate returns a NEW vector)
        particle.velocity = direction * random.uniform(30, max_speed)  # number x arrow = random speed