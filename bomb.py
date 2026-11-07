import pygame
from circleshape import CircleShape
from constants import BOMB_RADIUS, BOMB_FUSE_SECONDS, LINE_WIDTH


class Bomb(CircleShape):  # sits where it was dropped, then explodes
    def __init__(self, x, y):
        super().__init__(x, y, BOMB_RADIUS)
        self.fuse = BOMB_FUSE_SECONDS  # fuse = countdown timer
        self.detonated = False  # flag = True/False signal; main.py watches it

    def update(self, dt):
        self.fuse -= dt  # -= subtract and save back
        if self.fuse <= 0:
            self.detonated = True  # main.py sees this, blows up asteroids, and kills the bomb

    def draw(self, screen):
        color = "red" if int(self.fuse * 6) % 2 == 0 else "white"  # A if condition else B; blinks between red and white
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)