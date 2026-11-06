import pygame  # needed for Vector2, draw.polygon, and key.get_pressed; each file needs its own imports
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED  # shoot() uses PLAYER_SHOOT_SPEED
from circleshape import CircleShape  # a class can only inherit from a parent it can see
from shot import Shot  # NEW: shoot() creates Shot objects, so this file must know the name


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

    def move(self, dt):  # moves the ship a small step in the direction it faces
        unit_vector = pygame.Vector2(0, 1)  # unit vector = arrow of length 1 (direction only); (0, 1) = down
        rotated_vector = unit_vector.rotate(self.rotation)  # .rotate() returns a NEW vector, turned by rotation degrees
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt  # number x vector stretches its length. Ex: (0, 1) * 200 * 0.0167 = (0, 3.34)
        self.position += rotated_with_speed_vector  # adds the step to the position; this is where the ship actually moves

    def shoot(self):  # T6: takes no parameters besides self (the player firing)
        shot = Shot(self.position.x, self.position.y)  # T6.1: instantiate = create a Shot at the player's center; Shot.containers adds it to the groups automatically
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED  # T6.2: same math as move(): (0, 1) turned to face forward, then scaled. Ex: rotation 0 = (0, 500), straight down

    def update(self, dt: float) -> None:  # runs once per frame; float = decimal number; -> None = returns nothing
        keys = pygame.key.get_pressed()  # asks pygame which keys are held down right now

        if keys[pygame.K_a]:  # K_a = pygame's name for the A key; True while held
            self.rotate(-dt)  # minus reverses dt: turn left
        if keys[pygame.K_d]:
            self.rotate(dt)  # turn right
        if keys[pygame.K_w]:  # each `if` is checked separately, so W + A together turns AND moves
            self.move(dt)  # forward
        if keys[pygame.K_s]:
            self.move(-dt)  # negated dt = backward
        if keys[pygame.K_SPACE]:  # T7: True while the spacebar is held; runs every frame, so holding it makes a stream of bullets (expected for now)
            self.shoot()