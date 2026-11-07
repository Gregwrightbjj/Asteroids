import pygame  # library: code someone else wrote
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # wrap() needs the screen size


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):  # class = blueprint; (Sprite) = inherit pygame's base for objects that join groups
    containers: tuple[pygame.sprite.Group, ...]  # type hint (a note, not enforced): groups set by each subclass

    def __init__(self, x: float, y: float, radius: float) -> None:  # constructor runs on creation; self = this object
        if hasattr(self, "containers"):  # hasattr = "does this object have this attribute?"
            super().__init__(*self.containers)  # super() = parent class; * spreads the tuple, so the object joins every group
        else:
            super().__init__()  # no containers set: joins no groups

        self.position: pygame.Vector2 = pygame.Vector2(x, y)  # Vector2 = an (x, y) point/arrow; a NEW one per object
        self.velocity = pygame.Vector2(0, 0)  # speed + direction; (0, 0) = still
        self.radius = radius  # center-to-edge distance in pixels; also the hitbox size

    def draw(self, screen: pygame.Surface) -> None:  # Surface = rectangle of pixels you can draw on
        pass  # empty default; children override (define their own version that runs instead)

    def update(self, dt: float) -> None:  # dt = delta time, seconds since the last frame
        pass  # empty default

    def collides_with(self, other) -> bool:  # circle vs circle
        distance = self.position.distance_to(other.position)  # center-to-center distance
        return distance <= self.radius + other.radius  # touching if distance <= r1 + r2

    def wrap(self, margin=None):  # object leaving one side reappears on the opposite side
        if margin is None:  # default parameter: used when the caller gives none
            margin = self.radius  # wrap once the whole circle is off-screen
        if self.position.x < -margin:  # past the left edge
            self.position.x = SCREEN_WIDTH + margin  # reappear beyond the right edge
        elif self.position.x > SCREEN_WIDTH + margin:  # past the right edge
            self.position.x = -margin
        if self.position.y < -margin:  # past the top
            self.position.y = SCREEN_HEIGHT + margin
        elif self.position.y > SCREEN_HEIGHT + margin:  # past the bottom
            self.position.y = -margin