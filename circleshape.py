import pygame  # library: code someone else wrote; needed for Sprite, Group, Vector2, Surface


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):  # class = blueprint for objects; (Sprite) = inherit pygame's base class for objects that can join groups
    containers: tuple[pygame.sprite.Group, ...]  # type hint (a note, not enforced): a tuple (fixed list) of Groups set by Player/Asteroid

    def __init__(self, x: float, y: float, radius: float) -> None:  # constructor runs on creation; self = this object; float = decimal number
        # we will be using this later
        if hasattr(self, "containers"):  # hasattr = "does this object have an attribute with this name?"
            super().__init__(*self.containers)  # super() = parent class; * spreads the tuple so the object joins every group in it
        else:
            super().__init__()  # no containers set: joins no groups

        self.position: pygame.Vector2 = pygame.Vector2(x, y)  # attribute = variable on an object; Vector2 = an (x, y) point/arrow
        self.velocity = pygame.Vector2(0, 0)  # speed + direction; (0, 0) = not moving
        self.radius = radius  # center-to-edge distance in pixels; also the hitbox (collision circle) size

    def draw(self, screen: pygame.Surface) -> None:  # Surface = rectangle of pixels you can draw on
        # must override
        pass  # pass = do nothing; children override (define their own version that runs instead)

    def update(self, dt: float) -> None:  # dt = delta time, seconds since the last frame
        # must override
        pass

    def collides_with(self, other) -> bool:  # T1: other = the second shape; -> bool = returns True or False
        distance = self.position.distance_to(other.position)  # distance_to = straight-line distance between two centers
        return distance <= self.radius + other.radius  # touching if distance <= r1 + r2. Ex: ship r20 at (100,100), asteroid r40 at (150,100): 50 <= 60 = True