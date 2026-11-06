import pygame  # needed for Vector2, draw.polygon, and key.get_pressed; each file needs its own imports
from constants import (  # parentheses let one import span several lines
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,  # T2: "import it into player.py"; shoot() uses it
)
from circleshape import CircleShape  # a class can only inherit from a parent it can see
from shot import Shot  # shoot() creates Shot objects


class Player(CircleShape):  # class = blueprint for objects; (CircleShape) = inherit the parent's attributes/methods
    def __init__(self, x, y):  # constructor (__init__) runs when a Player is created; self = this object
        super().__init__(x, y, PLAYER_RADIUS)  # super() = parent class; runs its setup (position, radius)
        self.rotation = 0  # attribute = variable on an object; rotation = turn angle in degrees
        self.shoot_timer = 0  # T1: seconds left before the ship may fire again; 0 = ready (so the first shot is allowed)

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
        self.position += rotated_with_speed_vector  # adds the step to the position; this is where the ship moves

    def shoot(self):  # takes no parameters besides self (the player firing)
        if self.shoot_timer > 0:  # T3.1: timer above 0 = still cooling down. Ex: 0.2 > 0 is True
            return  # return = end the method right now; skips every line below, so no bullet is made

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS  # T3.2: ready, so restart the cooldown at 0.3; makes the NEXT call hit the check above

        shot = Shot(self.position.x, self.position.y)  # instantiate = create a Shot at the player's center; joins its groups automatically
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED  # same math as move(): turn (0, 1) to face forward, then scale it

    def update(self, dt: float) -> None:  # runs once per frame; float = decimal number; -> None = returns nothing
        self.shoot_timer -= dt  # T4: -= subtract and save back; counts the timer down in real time. Ex: 0.3 - 0.0167 = 0.2833. It may dip below 0, which is fine because shoot() only checks "> 0"

        keys = pygame.key.get_pressed()  # asks pygame which keys are held down right now

        if keys[pygame.K_a]:  # K_a = pygame's name for the A key; True while held
            self.rotate(-dt)  # minus reverses dt: turn left
        if keys[pygame.K_d]:
            self.rotate(dt)  # turn right
        if keys[pygame.K_w]:  # each `if` is checked separately, so W + A together turns AND moves
            self.move(dt)  # forward
        if keys[pygame.K_s]:
            self.move(-dt)  # negated dt = backward
        if keys[pygame.K_SPACE]:  # held space still calls shoot() every frame, but shoot() now refuses during the cooldown
            self.shoot()