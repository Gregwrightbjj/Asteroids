import pygame  # needed for pygame.draw.circle; each file needs its own imports
from constants import LINE_WIDTH  # outline thickness the task asks for
from circleshape import CircleShape  # the parent class we inherit from


class Asteroid(CircleShape):  # class = blueprint for objects; (CircleShape) = inherit position, radius, velocity
    def __init__(self, x: float, y: float, radius: float) -> None:  # constructor runs on creation; float = decimal number; -> None = returns nothing
        super().__init__(x, y, radius)  # super() = parent class; runs its setup so the sprite is initialized

    def draw(self, screen):  # override = same name as parent's draw, so this version runs instead
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)  # surface, color, center, radius, outline width. Ex: radius 40 = circle 80 pixels across

    def update(self, dt: float) -> None:  # runs once per frame; dt = seconds since last frame
        self.position += self.velocity * dt  # velocity = speed + direction (a Vector2); x dt = same speed on any computer. Ex: (60, 0) * 0.0167 = 1 pixel right per frame