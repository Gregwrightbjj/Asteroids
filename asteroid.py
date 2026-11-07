import random  # NEW: Python's built-in random numbers; split() uses random.uniform
import pygame  # needed for pygame.draw.circle; each file needs its own imports
from logger import log_event  # NEW: split() records "asteroid_split" in game_events.jsonl
from circleshape import CircleShape  # the parent class we inherit from
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS  # ASTEROID_MIN_RADIUS is NEW: split() compares against it and subtracts it


class Asteroid(CircleShape):  # class = blueprint for objects; (CircleShape) = inherit position, radius, velocity
    def __init__(self, x: float, y: float, radius: float) -> None:  # constructor runs on creation; float = decimal number; -> None = returns nothing
        super().__init__(x, y, radius)  # super() = parent class; runs its setup

    def draw(self, screen):  # override = same name as parent's draw, so this version runs instead
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)  # surface, color, center, radius, outline width

    def update(self, dt: float) -> None:  # override: moves the asteroid; dt = seconds since last frame
        self.position += self.velocity * dt  # velocity = speed + direction (Vector2); x dt = same speed on any computer

    def split(self):  # NEW: destroys this asteroid and maybe spawns two smaller, faster ones. Sizes (radius): large 60, medium 40, small 20
        self.kill()  # T1: kill() removes it from all its groups; first, because it always happens. position and radius still work afterward

        if self.radius <= ASTEROID_MIN_RADIUS:  # T2: <= means "less than or equal to". Ex: 20 <= 20 is True = small asteroid
            return  # return = end the method now; small asteroids just disappear

        log_event("asteroid_split")  # T3.1: records the split; text must match exactly

        random_angle = random.uniform(20, 50)  # T3.2: random decimal between 20 and 50 degrees. Ex: 31.7

        first_velocity = self.velocity.rotate(random_angle)  # T3.3: rotate() turns an arrow and returns a NEW vector. Ex: (60, 0) rotated 30 = about (51.96, 30)
        second_velocity = self.velocity.rotate(-random_angle)  # T3.4: minus sign = opposite direction, so the pair fans out on either side

        new_radius = self.radius - ASTEROID_MIN_RADIUS  # T3.5: Ex: 60 - 20 = 40 (large becomes medium); 40 - 20 = 20 (medium becomes small)

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)  # T3.6: instantiate = create an object; joins its groups via Asteroid.containers
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)  # second one starts at the same spot

        first_asteroid.velocity = first_velocity * 1.2  # T3.7: number x vector stretches its length; 1.2 = 20% faster. Ex: speed 60 becomes 72
        second_asteroid.velocity = second_velocity * 1.2  # T3.8: same for the second one