import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from constants import (  # import the named settings below from constants.py; parentheses allow this one import statement to span several lines
    SCREEN_WIDTH,  # read the window width setting from constants.py; respawn() divides it by two to put the ship halfway across the window after losing a life
    SCREEN_HEIGHT,  # read the window height setting from constants.py; respawn() divides it by two to put the ship halfway down the window
    PLAYER_RADIUS,  # read the ship size from constants.py; triangle() uses this center-to-tip distance to calculate the three points making up the ship
    LINE_WIDTH,  # read how many pixels thick an outline should be; draw() uses it for the ship's triangle and cyan shield ring
    PLAYER_TURN_SPEED,  # read how many degrees the ship turns in one second; rotate() multiplies it by elapsed time to calculate this frame's turn
    PLAYER_ACCELERATION,  # read how strongly the engine changes the ship's movement; accelerate() uses it to add forward or backward speed while a thrust key is held
    PLAYER_DRAG,  # read how strongly the ship slows while drifting; update() uses it to reduce the horizontal and vertical movement speeds each frame
    PLAYER_MAX_SPEED,  # read the normal speed limit; accelerate() checks the ship's total speed against this limit and reduces it if necessary
    PLAYER_RESPAWN_INVULNERABLE_SECONDS,  # read the protection duration after losing a life; invulnerable means another rock cannot remove a life while that countdown is positive
    SHIELD_DURATION_SECONDS,  # read how long touching a cyan shield item protects the ship; apply_powerup() starts or resets the shield countdown to this duration
    SPEED_BOOST_DURATION_SECONDS,  # read how long touching a yellow item makes the ship faster; apply_powerup() starts or resets the speed-bonus countdown
    SPEED_BOOST_MULTIPLIER,  # read the factor that increases engine strength and the speed limit during a speed bonus; multiplying by 1.5 means 50% more than normal
    WEAPONS,  # bring in the named weapon-settings collection from constants.py; shoot() looks up the selected name to get its bullet size, speed, angles, delay, and whether bullets survive hits
    BOMB_START_COUNT,  # read how many bombs a new ship receives; the ship stores this in bombs_left and subtracts one for each successful drop
)
from circleshape import CircleShape  # look in circleshape.py and bring in the CircleShape class, a blueprint that stores position, speed/direction, and size and supplies functions for checking contact and reappearing across screen edges
from shot import Shot  # look in shot.py and bring in the Shot class, a blueprint for bullets; shoot() below calls Shot(...) to create an actual bullet at the ship's position
from bomb import Bomb  # look in bomb.py and bring in the Bomb class, a blueprint for bombs; drop_bomb() below calls Bomb(...) to create one where the ship is


# ---------- triangle collision helpers ----------
def point_segment_distance(p, a, b):  # define a function that finds how close point p is to the straight edge from a to b; the ship uses it to check whether a rock or bonus item touches one of its sides
    ab = b - a  # subtract a's x/y coordinates from b's to get an arrow from a to b; Pygame calls this pair of horizontal/vertical numbers a Vector2
    length_sq = ab.length_squared()  # calculate the edge length squared: horizontal change times itself plus vertical change times itself; the next calculation uses this to find a position along the edge
    if length_sq == 0:  # check whether a and b are the same point; an edge with zero length would cause division by zero in the normal calculation
        return p.distance_to(a)  # for a zero-length edge, return the ordinary straight-line distance from p to its single endpoint instead of dividing by zero
    t = (p - a).dot(ab) / length_sq  # find how far along the edge p would line up: 0 means a and 1 means b; dot multiplies the horizontal parts together and the vertical parts together, then adds them
    t = max(0, min(1, t))  # restrict t to 0 through 1, where 0 is endpoint a and 1 is endpoint b; the nearest point must stay on this finite edge
    return p.distance_to(a + ab * t)  # calculate the nearest point on the edge by starting at a and traveling fraction t toward b, then return the distance from p to that point


def side(p1, p2, p3):  # define a math helper whose result is negative, positive, or zero depending on which side of the directed line from p2 to p3 contains p1
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)  # use the points' x/y coordinates to calculate a side-of-line test: positive means one side, negative means the other, and zero means p1 lies on the line through p2 and p3


def point_in_triangle(p, a, b, c):  # define a helper that checks whether point p is inside or on the boundary of the triangle whose three corners are a, b, and c
    d1, d2, d3 = side(p, a, b), side(p, b, c), side(p, c, a)  # check p against all three edges and assign the three signed results to d1, d2, and d3 in one statement
    has_negative = d1 < 0 or d2 < 0 or d3 < 0  # store True if at least one edge result is negative; or requires only one of these comparisons to be true
    has_positive = d1 > 0 or d2 > 0 or d3 > 0  # store True if at least one edge result is positive; together these two flags reveal whether the point lies on conflicting sides
    return not (has_negative and has_positive)  # mixed positive and negative signs mean outside the triangle; not reverses that result so inside/on-edge returns True


class Player(CircleShape):  # define Player, a blueprint for making ships; (CircleShape) means build on that existing blueprint's position, motion, and screen-edge functions, then add the ship-specific code below
    def __init__(self, x, y, sounds=None):  # define setup for one ship; x/y place it, and optional sounds supplies the game's audio manager while allowing simple examples to create a silent ship
        super().__init__(x, y, PLAYER_RADIUS)  # run CircleShape's setup to store the ship's position and size, start its velocity at zero, and join the groups assigned in main.py
        self.rotation = 0  # set the ship's facing angle to zero degrees; the triangle-building formula points the initial ship downward because screen y increases downward
        self.shoot_timer = 0  # start with no firing delay remaining; shoot() can fire immediately and then sets this timer to the selected weapon's delay
        self.invulnerable_timer = 0.0  # start with zero seconds of respawn protection; invulnerable means collisions cannot remove a life while this timer is positive
        self.shield_timer = 0.0  # start with no active shield; touching a cyan shield item gives this countdown a positive number of seconds
        self.speed_boost_timer = 0.0  # start with no speed bonus; touching a yellow speed item starts this timer and temporarily raises acceleration and maximum speed
        self.weapon = "single"  # store single as the selected weapon name; this string chooses the matching settings dictionary inside WEAPONS
        self.bombs_left = BOMB_START_COUNT  # give this ship the starting supply of three bombs; the value decreases whenever a bomb is successfully dropped
        self.sounds = sounds  # remember the supplied audio manager so firing and bomb-drop methods can request a sound after an action succeeds

    def triangle(self) -> list[pygame.Vector2]:  # define a function that gives back the ship's three corner positions; -> list[pygame.Vector2] is a note saying the result is a list of x/y pairs
        forward = pygame.Vector2(0, 1).rotate(self.rotation)  # start with an arrow one unit long pointing downward, then turn it by the ship's current angle; this gives the nose direction before multiplying by the ship's size
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # make a sideways arrow at a 90-degree angle to the nose direction; multiplying by radius / 1.5 sets how wide the triangle's two back corners will be
        a = self.position + forward * self.radius  # place corner a, the ship's nose, one radius ahead of its center along the facing direction
        b = self.position - forward * self.radius - right  # place one rear corner by moving behind the ship's center and subtracting the sideways offset
        c = self.position - forward * self.radius + right  # place the other rear corner behind the center with the opposite sideways offset, completing the triangular ship
        return [a, b, c]  # give the three corner vectors back in a list; both drawing and collision checks call this same function so they use the same triangle

    def draw(self, screen):  # define how this ship is drawn: show a cyan shield ring when protected by a shield, blink the ship after losing a life, and otherwise draw its white triangle
        if self.shield_timer > 0:  # draw the shield ring only while positive shield time remains, so the player can see that the collected protection is active
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 6, LINE_WIDTH)  # draw a cyan outline around the ship's center, six pixels beyond its normal radius, using the shared outline thickness
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:  # while respawn protection is active, convert the timer to tenths of a second and test whether it is even; % gives a remainder, creating alternating blink intervals
            return  # stop drawing the ship for this blink interval; alternating visible and invisible intervals show that respawn protection is active
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)  # get the ship's three corner positions and connect them with a white outline, drawing the actual triangle used by collision checks

    def rotate(self, dt):  # define how the ship turns; the caller supplies positive elapsed time for one direction or negative elapsed time for the other
        self.rotation += PLAYER_TURN_SPEED * dt  # change the facing angle by degrees-per-second times elapsed seconds; negative dt subtracts angle instead of adding it

    def accelerate(self, dt):  # define how engine thrust changes speed and direction; positive dt pushes toward the nose, negative dt pushes the opposite way, and velocity stores the resulting horizontal/vertical speeds
        boost = SPEED_BOOST_MULTIPLIER if self.speed_boost_timer > 0 else 1  # use multiplier 1.5 while speed-bonus time remains, otherwise 1; this if/else expression selects one value to store in boost
        forward = pygame.Vector2(0, 1).rotate(self.rotation)  # create an arrow of length one pointing downward, then turn it by the ship's current angle; this gives the direction the ship's nose faces
        self.velocity += forward * PLAYER_ACCELERATION * boost * dt  # add thrust to the current motion using facing direction, acceleration, any speed bonus, and elapsed seconds; existing movement is retained
        if self.velocity.length() > PLAYER_MAX_SPEED * boost:  # calculate the total speed from the horizontal/vertical velocity and check whether it exceeds the current normal or boosted speed limit
            self.velocity.scale_to_length(PLAYER_MAX_SPEED * boost)  # shrink the velocity arrow to the allowed maximum speed without changing its direction, preventing unlimited acceleration

    def respawn(self):  # define what happens after the ship loses a life: return to the center, stop moving, reset its angle, and start temporary protection
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # replace the ship's position with the window's horizontal and vertical halfway points, putting it back in the center
        self.velocity = pygame.Vector2(0, 0)  # set both horizontal and vertical speed to zero so the ship stops drifting after it reappears
        self.rotation = 0  # set the ship's facing angle to zero degrees; the triangle-building formula points the initial ship downward because screen y increases downward
        self.invulnerable_timer = PLAYER_RESPAWN_INVULNERABLE_SECONDS  # start the two-second period in which collisions cannot remove another life immediately after the ship reappears

    def is_protected(self):  # provide a single yes/no check that main.py can use to decide whether the ship is currently immune to asteroid damage
        return self.invulnerable_timer > 0 or self.shield_timer > 0  # return True when either respawn protection or a collected shield still has time left; the ship can take damage only when both have expired

    def apply_powerup(self, kind):  # apply a collected item's effect; kind is the text shield or speed, identifying the bonus the ship receives when it touches that item
        if kind == "shield":  # check whether the collected item's name is shield; == compares values rather than assigning a new value
            self.shield_timer = SHIELD_DURATION_SECONDS  # set shield time to five seconds, starting protection or refreshing an existing shield instead of adding more time to it
        elif kind == "speed":  # if the item was not a shield, check whether its name is speed and therefore should grant faster movement
            self.speed_boost_timer = SPEED_BOOST_DURATION_SECONDS  # set speed-bonus time to five seconds; accelerate() reads this timer to increase thrust and the maximum speed

    def collides_with(self, other):  # replace CircleShape's circle-to-circle check with a triangle-to-circle check; self is the ship and other is the rock or collectible being tested
        a, b, c = self.triangle()  # get the ship's current triangle corners and unpack the three returned points into separate variables a, b, and c
        center = other.position  # read the other object's center point, which is needed to test whether its circular area overlaps the ship's triangle
        if point_in_triangle(center, a, b, c):  # first check whether the other object's center is already inside the ship triangle; if it is, the two objects definitely overlap
            return True  # return the yes/no value True to tell the caller that the ship touches this object
        for start, end in ((a, b), (b, c), (c, a)):  # check the three triangle edges in turn, unpacking each endpoint pair into start and end for the distance calculation
            if point_segment_distance(center, start, end) <= other.radius:  # if the circle's center is no farther from this edge than its radius, the circle reaches the edge and therefore touches the ship
                return True  # return the yes/no value True to tell the caller that the ship touches this object
        return False  # return the yes/no value False because none of the triangle-versus-circle checks found contact

    def shoot(self):  # define how the selected weapon fires: check its delay, restart the delay, then create one bullet for every configured firing angle
        if self.shoot_timer > 0:  # refuse to fire while positive firing-delay time remains; this limits shot frequency even when Space is held continuously
            return  # leave shoot() without making bullets because the selected weapon's waiting time has not finished yet
        weapon = WEAPONS[self.weapon]  # look up the selected weapon name in WEAPONS and save its settings dictionary, including bullet speed, size, delay, and firing angles
        self.shoot_timer = weapon["cooldown"]  # restart the firing-delay countdown using this weapon's cooldown, meaning the seconds the ship must wait before it can fire again
        for angle in weapon["angles"]:  # create one bullet for each angle in this weapon's list; [0] makes one straight bullet, while [-15, 0, 15] makes three spread bullets
            shot = Shot(self.position.x, self.position.y, weapon["radius"], weapon["pierce"])  # create a bullet at the ship's current x/y position using the selected bullet size and whether it can continue after hitting a rock
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle) * weapon["speed"]  # aim the bullet along the ship's facing angle plus its spread offset, then multiply the direction arrow by the weapon's bullet speed
        if self.sounds is not None:  # request audio only when this ship has been connected to a sound manager
            self.sounds.play("shoot_" + self.weapon)  # play one weapon-specific sound after the successful volley, so spread shots do not make three overlapping copies

    def drop_bomb(self):  # define how B places a stationary bomb at the ship's position; the method must first check that the limited supply has not run out
        if self.bombs_left <= 0:  # stop if zero bombs remain; <= also prevents accidental negative supplies from allowing another bomb
            return  # leave drop_bomb() without creating anything because the ship has already used its entire bomb supply
        self.bombs_left -= 1  # subtract one from this ship's remaining bomb supply before creating the bomb so each accepted drop spends exactly one
        Bomb(self.position.x, self.position.y)  # create a bomb at the ship's current coordinates; its inherited setup joins the groups assigned to Bomb.containers in main.py
        if self.sounds is not None:  # keep a ship created without audio usable in isolated examples and checks
            self.sounds.play("bomb_drop")  # confirm the successful drop; the early return for an empty supply prevents a misleading confirmation sound

    def update(self, dt: float) -> None:  # run the ship's timers, held-key controls, slowdown, movement, and edge wrapping each active frame; dt is elapsed seconds and no result is returned
        self.shoot_timer -= dt  # subtract elapsed seconds from the firing delay so the ship can shoot again when the timer reaches zero or becomes negative
        self.invulnerable_timer -= dt  # subtract elapsed seconds from respawn protection; damage becomes possible again when both this timer and the shield timer have expired
        self.shield_timer -= dt  # subtract elapsed seconds from the protection granted by a cyan shield item; zero or less means the shield has expired
        self.speed_boost_timer -= dt  # subtract elapsed seconds from the yellow item's speed bonus; zero or less makes acceleration and maximum speed return to normal

        keys = pygame.key.get_pressed()  # ask Pygame which keys are held right now; keys[pygame.K_LEFT], for example, gives True if the left arrow is held and False if it is not
        if keys[pygame.K_LEFT]:  # check whether the left-arrow key is currently held; if so, run the indented turning instruction every active frame
            self.rotate(-dt)  # turn using negative elapsed time, which subtracts from the facing angle and rotates the ship to the left
        if keys[pygame.K_RIGHT]:  # check whether the right-arrow key is held, allowing the ship to turn right continuously rather than only once per press
            self.rotate(dt)  # turn using positive elapsed time, which increases the facing angle and rotates the ship to the right
        if keys[pygame.K_UP]:  # check whether the up-arrow key is held; this key adds thrust along the direction the ship currently faces
            self.accelerate(dt)  # apply forward thrust for this frame; the ship gains velocity along its current facing direction rather than instantly changing position
        if keys[pygame.K_DOWN]:  # check whether the down-arrow key is held; this applies thrust opposite the ship's facing direction and can slow it or move it backward
            self.accelerate(-dt)  # apply reverse thrust by passing negative elapsed time, making the acceleration contribution point opposite the ship's nose
        if keys[pygame.K_1]:  # check whether number key 1 is held; the next assignment selects the standard single-bullet weapon
            self.weapon = "single"  # store single as the selected weapon name; this string chooses the matching settings dictionary inside WEAPONS
        if keys[pygame.K_2]:  # check whether number key 2 is held; the next assignment selects a three-bullet spread weapon
            self.weapon = "spread"  # select the spread entry in WEAPONS so future shots create three bullets at slightly different angles
        if keys[pygame.K_3]:  # check whether number key 3 is held; the next assignment selects small bullets with a short firing delay
            self.weapon = "rapid"  # select the rapid entry in WEAPONS so future bullets fire more frequently than the standard weapon
        if keys[pygame.K_4]:  # check whether number key 4 is held; the next assignment selects large bullets that can survive collisions with rocks
            self.weapon = "heavy"  # select the heavy entry in WEAPONS so future bullets are larger, fire less often, and continue after hitting a rock
        if keys[pygame.K_SPACE]:  # check whether Space is held; try to fire on every active frame, with shoot() preventing shots until the selected firing delay has expired
            self.shoot()  # call the firing method, which either waits for its countdown or creates the selected weapon's next bullet or group of bullets

        self.velocity = self.velocity * max(0.0, 1 - PLAYER_DRAG * dt)  # multiply velocity by a factor slightly below one to gradually slow drifting; max prevents a long frame from making the factor negative and reversing direction
        self.position += self.velocity * dt  # advance the ship using its current velocity and elapsed seconds; this still happens with no thrust key held, which creates drifting movement
        self.wrap()  # call the inherited screen-edge helper so leaving the window on one side makes the ship reappear on the opposite side
