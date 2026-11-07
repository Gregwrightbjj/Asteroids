import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_DRAG,
    PLAYER_MAX_SPEED,
    PLAYER_RESPAWN_INVULNERABLE_SECONDS,
    SHIELD_DURATION_SECONDS,
    SPEED_BOOST_DURATION_SECONDS,
    SPEED_BOOST_MULTIPLIER,
    WEAPONS,
    BOMB_START_COUNT,
)
from circleshape import CircleShape  # parent class
from shot import Shot  # shoot() creates bullets
from bomb import Bomb  # drop_bomb() creates bombs


# ---------- triangle collision helpers ----------
def point_segment_distance(p, a, b):  # shortest distance from point p to the line segment a-b
    ab = b - a  # the edge as an arrow
    length_sq = ab.length_squared()  # edge length squared
    if length_sq == 0:  # degenerate edge: a and b are the same point
        return p.distance_to(a)
    t = (p - a).dot(ab) / length_sq  # dot product: how far along the edge p's "shadow" falls (0 = at a, 1 = at b)
    t = max(0, min(1, t))  # clamp so the closest spot stays on the segment
    return p.distance_to(a + ab * t)  # distance to that closest spot


def side(p1, p2, p3):  # the sign says which side of an edge a point is on
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)


def point_in_triangle(p, a, b, c):  # inside = never on opposite sides of two edges
    d1, d2, d3 = side(p, a, b), side(p, b, c), side(p, c, a)
    has_negative = d1 < 0 or d2 < 0 or d3 < 0
    has_positive = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_negative and has_positive)


class Player(CircleShape):  # the ship; inherits position, velocity, radius, wrap
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # turn angle in degrees
        self.shoot_timer = 0  # seconds until the next shot is allowed (0 = ready)
        self.invulnerable_timer = 0.0  # seconds of respawn protection left
        self.shield_timer = 0.0  # seconds of shield left
        self.speed_boost_timer = 0.0  # seconds of speed boost left
        self.weapon = "single"  # key into the WEAPONS dictionary
        self.bombs_left = BOMB_START_COUNT

    def triangle(self) -> list[pygame.Vector2]:  # the ship's 3 corners (given by the lesson)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # tip
        b = self.position - forward * self.radius - right  # back-left
        c = self.position - forward * self.radius + right  # back-right
        return [a, b, c]

    def draw(self, screen):
        if self.shield_timer > 0:  # shield ring around the ship
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 6, LINE_WIDTH)
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            return  # skip drawing every other tenth of a second = blinking
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt  # degrees/second x seconds = degrees; -dt turns the other way

    def accelerate(self, dt):  # thrust: changes VELOCITY, not position
        boost = SPEED_BOOST_MULTIPLIER if self.speed_boost_timer > 0 else 1  # A if condition else B
        forward = pygame.Vector2(0, 1).rotate(self.rotation)  # direction the ship faces
        self.velocity += forward * PLAYER_ACCELERATION * boost * dt  # push velocity that way
        if self.velocity.length() > PLAYER_MAX_SPEED * boost:  # length() = current speed
            self.velocity.scale_to_length(PLAYER_MAX_SPEED * boost)  # shrink to the cap, same direction

    def respawn(self):  # back to the center, still, and protected for a while
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)  # stop drifting
        self.rotation = 0
        self.invulnerable_timer = PLAYER_RESPAWN_INVULNERABLE_SECONDS

    def is_protected(self):  # one place to ask "can the ship be hurt right now?"
        return self.invulnerable_timer > 0 or self.shield_timer > 0

    def apply_powerup(self, kind):  # sets the matching timer
        if kind == "shield":
            self.shield_timer = SHIELD_DURATION_SECONDS
        elif kind == "speed":
            self.speed_boost_timer = SPEED_BOOST_DURATION_SECONDS

    def collides_with(self, other):  # override: triangle vs circle instead of circle vs circle
        a, b, c = self.triangle()  # the ship's corners
        center = other.position
        if point_in_triangle(center, a, b, c):  # the other circle's center is inside the ship
            return True
        for start, end in ((a, b), (b, c), (c, a)):  # the three edges
            if point_segment_distance(center, start, end) <= other.radius:  # circle touches an edge
                return True
        return False

    def shoot(self):
        if self.shoot_timer > 0:  # still cooling down
            return  # end the method now; no bullet
        weapon = WEAPONS[self.weapon]  # this weapon's settings (a dictionary)
        self.shoot_timer = weapon["cooldown"]  # restart the cooldown
        for angle in weapon["angles"]:  # one bullet per angle
            shot = Shot(self.position.x, self.position.y, weapon["radius"], weapon["pierce"])
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle) * weapon["speed"]  # facing + angle, scaled by speed

    def drop_bomb(self):
        if self.bombs_left <= 0:  # none left
            return
        self.bombs_left -= 1
        Bomb(self.position.x, self.position.y)  # joins its groups automatically via Bomb.containers

    def update(self, dt: float) -> None:  # runs once per frame
        self.shoot_timer -= dt  # timers count down in real time (they may dip below 0; that's fine)
        self.invulnerable_timer -= dt
        self.shield_timer -= dt
        self.speed_boost_timer -= dt

        keys = pygame.key.get_pressed()  # which keys are held right now (polling)
        if keys[pygame.K_LEFT]:  # K_LEFT = pygame's name for the left arrow
            self.rotate(-dt)  # turn left
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)  # turn right
        if keys[pygame.K_UP]:
            self.accelerate(dt)  # thrust forward
        if keys[pygame.K_DOWN]:
            self.accelerate(-dt)  # negated dt = reverse thrust
        if keys[pygame.K_1]:
            self.weapon = "single"
        if keys[pygame.K_2]:
            self.weapon = "spread"
        if keys[pygame.K_3]:
            self.weapon = "rapid"
        if keys[pygame.K_4]:
            self.weapon = "heavy"
        if keys[pygame.K_SPACE]:
            self.shoot()  # the cooldown limits how often it fires

        self.velocity = self.velocity * max(0.0, 1 - PLAYER_DRAG * dt)  # drag; max() stops the factor going negative
        self.position += self.velocity * dt  # drift happens even with no keys held
        self.wrap()  # leaving one side = reappearing on the other