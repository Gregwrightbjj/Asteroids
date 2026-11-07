import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # look in constants.py and bring in the window width and height; wrap() below needs these numbers to move an object to the opposite screen edge


# Ships, rocks, bullets, bombs, bonus items, and effect dots all build on the blueprint below.
class CircleShape(pygame.sprite.Sprite):  # define a blueprint for the information these game objects have in common; Sprite is Pygame's existing blueprint that lets an object join collections for moving and drawing
    containers: tuple[pygame.sprite.Group, ...]  # describe containers as a tuple, an ordered collection, of Pygame groups; ... means it may contain any number of groups, and main.py supplies the actual groups

    def __init__(self, x: float, y: float, radius: float) -> None:  # define the setup for one new object; self means that particular object, x/y say where it starts, radius is its size, float describes decimal numbers, and -> None means no result is returned
        if hasattr(self, "containers"):  # hasattr asks whether this object has a value named containers; main.py puts the groups to join under this name before creating ships, rocks, and the other objects
            super().__init__(*self.containers)  # super() reaches the Sprite blueprint that CircleShape builds on; run its setup, using * to pass each group separately so this object joins all of them
        else:  # run this indented branch only when the preceding if condition was false
            super().__init__()  # run Pygame's Sprite setup without supplying groups when containers was never set; the object still exists but belongs to no update or drawing collection

        self.position: pygame.Vector2 = pygame.Vector2(x, y)  # store where this object is using a Vector2, Pygame's pair of horizontal/vertical numbers; the text after : describes the expected kind of value
        self.velocity = pygame.Vector2(0, 0)  # start horizontal and vertical speed at zero; velocity is the combination of how fast an object moves and the direction it moves
        self.radius = radius  # store the center-to-edge distance in pixels; circular objects use this size for drawing and for their invisible collision-checking area

    def draw(self, screen: pygame.Surface) -> None:  # provide a function name the drawing loop can call on every object; this version draws nothing, while Player, Asteroid, and the other blueprints define their own draw functions
        pass  # do nothing; Python requires something inside a function, and each kind of game object supplies its actual drawing instructions in its own file

    def update(self, dt: float) -> None:  # provide a function name the update collection can call on every object; dt is elapsed seconds, and each kind of object defines its own movement or countdown instructions
        pass  # do nothing in this version; the ship, rocks, bullets, and other objects define the update functions that actually change their stored values

    def collides_with(self, other) -> bool:  # check whether this object's circular collision area touches another object's circle; -> bool describes a True or False result
        distance = self.position.distance_to(other.position)  # measure the straight-line distance between this object's center and the other object's center using their x/y positions
        return distance <= self.radius + other.radius  # return True if the center distance is no greater than the two radii added together, meaning the circles touch or overlap

    def wrap(self, margin=None):  # move an object leaving one screen edge to the opposite edge; margin controls how far beyond the visible screen it travels before moving across
        if margin is None:  # check whether the caller omitted a margin value; None means no specific value was supplied, so the object's own radius will be used
            margin = self.radius  # use the object's radius as its off-screen allowance so its entire circular area leaves one edge before it reappears on the other
        if self.position.x < -margin:  # check whether the center has traveled farther than the allowed distance beyond the left edge, where horizontal coordinates become negative
            self.position.x = SCREEN_WIDTH + margin  # move the object just beyond the right edge while leaving its vertical position unchanged; it can then continue moving into view
        elif self.position.x > SCREEN_WIDTH + margin:  # otherwise check whether the object has traveled beyond the right edge plus its off-screen allowance
            self.position.x = -margin  # move the object just beyond the left edge while preserving its vertical position and current velocity
        if self.position.y < -margin:  # separately check whether the object has traveled beyond the top edge; vertical screen coordinates increase downward, so above the top is negative
            self.position.y = SCREEN_HEIGHT + margin  # move the object just below the bottom edge, preserving its horizontal position so top-to-bottom wrapping lines up
        elif self.position.y > SCREEN_HEIGHT + margin:  # otherwise check whether the object's center has traveled below the bottom edge plus its off-screen allowance
            self.position.y = -margin  # move the object just above the top edge while preserving its horizontal position and current velocity
