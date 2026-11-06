import pygame  # library: code someone else wrote; needed for Sprite, Group, Vector2, Surface


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):  # class = blueprint for objects; Sprite = pygame's base class for objects that can join groups; (Sprite) = inherit from it
    containers: tuple[pygame.sprite.Group, ...]  # type hint (a note, not enforced): a tuple (fixed list) of Groups; Player/Asteroid set this before creating objects

    def __init__(self, x: float, y: float, radius: float) -> None:  # constructor (__init__) runs on creation; self = this object; float = decimal number; -> None = returns nothing
        # we will be using this later
        if hasattr(self, "containers"):  # hasattr = "does this object have an attribute with this name?" (True if containers was set on the class)
            super().__init__(*self.containers)  # super() = parent class (Sprite); * unpacks the tuple into separate arguments, so the object joins every group in it
        else:
            super().__init__()  # no containers set: still runs the parent's setup, just joins no groups

        self.position: pygame.Vector2 = pygame.Vector2(x, y)  # attribute = variable on an object; Vector2 = an (x, y) point/arrow. Ex: (640.0, 360.0) = screen center
        self.velocity = pygame.Vector2(0, 0)  # velocity = speed + direction; starts at (0, 0) = not moving; Asteroid.update uses it
        self.radius = radius  # center-to-edge distance in pixels; also the hitbox (collision circle) size

    def draw(self, screen: pygame.Surface) -> None:  # Surface = rectangle of pixels you can draw on
        # must override
        pass  # pass = do nothing; empty default so every object has draw(). override = a child defines its own version, which runs instead

    def update(self, dt: float) -> None:  # dt = delta time, seconds since the last frame
        # must override
        pass  # empty default so updatable.update(dt) never crashes; Player and Asteroid override it