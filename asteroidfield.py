import random  # bring in Python's random-number tools; this file uses them to choose each new rock's starting edge, position, size, speed, and travel angle
from collections.abc import Callable  # bring in Callable from Python's collections.abc tools; it lets the next type description say that part of each edge definition is a function

import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from asteroid import Asteroid  # look in asteroid.py and bring in the Asteroid class, a blueprint for rocks; spawn() below calls Asteroid(...) to create each actual rock
from constants import *  # look in constants.py and bring in all its public setting names; * means all, so screen dimensions, rock sizes, and the creation interval can be used here

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]  # describe what one edge entry contains: a two-number direction arrow and a function taking a decimal fraction and returning an x/y position; this description does not create an edge or enforce its contents


class AsteroidField(pygame.sprite.Sprite):  # define a blueprint for the invisible rock creator; Sprite is Pygame's blueprint for objects that can join a collection, allowing main.py to update this creator along with the visible objects
    containers: pygame.sprite.Group  # give a type description for the groups to join; this line supplies no group by itself, and main.py later stores its one-item collection of update groups here

    edges: list[Edge] = [  # store four edge definitions in a list; each pairs a direction pointing into the window with a function selecting a starting point just outside that edge
        (
            pygame.Vector2(1, 0),  # for the left edge, use a direction arrow pointing right: positive horizontal movement and no vertical movement
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),  # create a small unnamed function: its 0-to-1 y argument chooses a vertical fraction of the window, while x places the rock just left of the visible screen
        ),
        (
            pygame.Vector2(-1, 0),  # for the right edge, use a direction arrow pointing left: negative horizontal movement and no vertical movement
            lambda y: pygame.Vector2(  # start a small unnamed function taking a vertical fraction y and returning the right-edge position vector completed on the next line
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT  # set x just beyond the right side by adding the maximum rock radius, and turn the y fraction into an actual vertical screen coordinate
            ),
        ),
        (
            pygame.Vector2(0, 1),  # for the top edge, point downward into the window: no horizontal movement and positive vertical movement because screen y increases downward
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),  # create a function choosing a horizontal fraction across the window and a vertical coordinate just above its top edge
        ),
        (
            pygame.Vector2(0, -1),  # for the bottom edge, point upward into the window using negative vertical movement and no horizontal movement
            lambda x: pygame.Vector2(  # start a small unnamed function taking a horizontal fraction x and returning the bottom-edge position vector completed on the next line
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS  # turn the x fraction into a horizontal coordinate and set y just below the screen by adding the maximum rock radius to the height
            ),
        ),
    ]

    def __init__(self) -> None:  # initialize this rock-producing object once when AsteroidField() is called; -> None means the setup method does not return a result value
        pygame.sprite.Sprite.__init__(self, self.containers)  # run Pygame's Sprite setup and add this invisible object to the group supplied in containers so its update method is called during play
        self.spawn_timer = 0.0  # start the elapsed time since the previous rock creation at zero; spawn means create and add a new object to the game

    def spawn(  # define a helper that creates one rock with a chosen radius, starting position, and movement; the argument list continues on the next line
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2  # self is this rock creator; radius is a decimal size, position holds x/y coordinates, and velocity holds horizontal/vertical speed
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)  # create one rock using the supplied coordinates and size; creating the object also joins the groups previously assigned to Asteroid.containers
        asteroid.velocity = velocity  # set this new rock's speed and direction to the vector supplied by the caller so it starts traveling into the window

    def update(self, dt: float) -> None:  # advance the rock-creation timer once per active frame; dt is elapsed seconds, and this method creates a rock when enough time has accumulated
        self.spawn_timer += dt  # add this frame's elapsed seconds to the time since the last rock was created; += saves the increased timer value
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:  # check whether more than the configured 0.8 seconds has passed, meaning another rock should now be created
            self.spawn_timer = 0  # reset elapsed creation time to zero so the next rock waits for another full interval

            # Create one rock; the next lines choose its starting place and how it moves.
            edge = random.choice(self.edges)  # choose one of the four stored edge pairs, which determines both where the new rock starts and its basic inward direction
            speed = random.randint(40, 100)  # choose a whole-number travel speed from 40 through 100 pixels per second, inclusive, so rocks do not all move equally fast
            velocity = edge[0] * speed  # take the edge's first item, a length-one arrow pointing into the window, and multiply by speed; [0] selects the first item because Python counts positions from zero
            velocity = velocity.rotate(random.randint(-30, 30))  # turn the movement arrow by a randomly chosen whole-number angle between -30 and 30 degrees so rocks enter at varied angles
            position = edge[1](random.uniform(0, 1))  # read the pair's position-making function using index 1 and call it with a random 0-to-1 fraction, choosing a point along that screen edge
            kind = random.randint(1, ASTEROID_KINDS)  # choose a size multiplier of 1, 2, or 3, corresponding to the three allowed rock sizes
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)  # call the creation helper with radius 20, 40, or 60 pixels and the randomly calculated starting position and movement vector
