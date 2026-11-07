import pygame  # needed for pygame.draw.circle
from circleshape import CircleShape  # parent class
from constants import SHOT_RADIUS, SHOT_LIFETIME_SECONDS, LINE_WIDTH


class Shot(CircleShape):  # a bullet: a small circle flying in a straight line
    def __init__(self, x, y, radius=SHOT_RADIUS, pierce=False):  # default parameters: old calls like Shot(x, y) still work
        super().__init__(x, y, radius)  # runs the parent's setup
        self.pierce = pierce  # True = survives hitting an asteroid
        self.age = 0.0  # seconds lived so far

    def draw(self, screen):  # override = this version runs instead of the parent's
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)  # surface, color, center, radius, outline width

    def update(self, dt):  # runs once per frame
        self.age += dt  # += add and save back
        if self.age >= SHOT_LIFETIME_SECONDS:  # too old?
            self.kill()  # kill() = remove from all groups, so it vanishes
            return  # stop here; skip the move
        self.position += self.velocity * dt  # velocity x dt = same speed on any computer