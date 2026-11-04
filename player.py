import pygame  # needed for Vector2, draw.polygon, and key.get_pressed; each file needs its own imports
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED  # T2.3: move() uses PLAYER_SPEED, so import it
from circleshape import CircleShape  # a class can only inherit from a parent it can see


class Player(CircleShape):  # class = blueprint for objects; (CircleShape) = inherit the parent's attributes/methods
    def __init__(self, x, y):  # constructor (__init__) runs when a Player is created; self = this object
        super().__init__(x, y, PLAYER_RADIUS)  # super() = parent class; runs its setup (position, radius)
        self.rotation = 0  # attribute = variable on an object; rotation = turn angle in degrees

    def triangle(self) -> list[pygame.Vector2]:  # returns the ship's 3 corners (-> = return type hint)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)  # Vector2 = an arrow/point stored as (x, y)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # sideways arrow sets ship width
        a = self.position + forward * self.radius  # tip of the ship
        b = self.position - forward * self.radius - right  # back-left corner
        c = self.position - forward * self.radius + right  # back-right corner
        return [a, b, c]

    def draw(self, screen):  # override = same name as parent's draw, so this version is used instead
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)  # polygon = shape from points; width 2 = outline only

    def rotate(self, dt):  # method = function belonging to a class; dt = seconds since last frame
        self.rotation += PLAYER_TURN_SPEED * dt  # += add and save back. Ex: 300 * 0.0167 = 5.01 degrees

    def move(self, dt):  # T2: moves the ship a small step in the direction it faces
        unit_vector = pygame.Vector2(0, 1)  # T2.1: unit vector = arrow of length 1 (direction only); y grows DOWN in pygame, so (0, 1) = down
        rotated_vector = unit_vector.rotate(self.rotation)  # T2.2: .rotate() returns a NEW vector (doesn't change the original). Ex: 90 turns (0, 1) into about (-1, 0)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt  # T2.3: number x vector stretches its length. Ex: (0, 1) * 200 * 0.0167 = (0, 3.34), one frame's step
        self.position += rotated_with_speed_vector  # T2.4: adds the step to the position; this is where the ship actually moves

    def update(self, dt: float) -> None:  # runs once per frame; float = decimal number; -> None = returns nothing
        keys = pygame.key.get_pressed()  # asks pygame which keys are held down right now

        if keys[pygame.K_a]:  # K_a = pygame's name for the A key; True while held
            self.rotate(-dt)  # minus reverses dt: turn left
        if keys[pygame.K_d]:
            self.rotate(dt)  # turn right
        if keys[pygame.K_w]:  # T3: each `if` is checked separately, so W + A together turns AND moves
            self.move(dt)  # forward
        if keys[pygame.K_s]:
            self.move(-dt)  # T3: negated dt = backward