# ---------- screen ----------
SCREEN_WIDTH = 1280  # set the game window width to 1280 pixels; a pixel is one dot on the screen, and uppercase names mark settings intended to stay constant
SCREEN_HEIGHT = 720  # set the game window height to 720 pixels; together with SCREEN_WIDTH this determines the drawing area and screen-edge positions

# ---------- player ----------
PLAYER_RADIUS = 20  # set the ship's size to 20 pixels from center to tip; the triangle is built from this value rather than drawn as a circle
LINE_WIDTH = 2  # draw shape outlines two pixels thick; this controls the visible thickness of ship, rock, bullet, and other outlined shapes
PLAYER_TURN_SPEED = 300  # turn the ship up to 300 degrees each second while a rotation key is held; a complete turn is 360 degrees
PLAYER_SPEED = 200  # keep the original course movement-speed setting for reference; current ship movement uses acceleration and PLAYER_MAX_SPEED instead
PLAYER_ACCELERATION = 400  # add 400 pixels-per-second of speed for each second thrust is held; acceleration changes velocity rather than directly moving the ship
PLAYER_DRAG = 1.0  # control how quickly the ship slows without thrust; player.py multiplies its speed by 1 - PLAYER_DRAG * dt each frame, so a larger value causes stronger slowdown
PLAYER_MAX_SPEED = 350  # limit normal ship speed to 350 pixels per second; the temporary speed bonus increases this limit
PLAYER_LIVES = 3  # start the game with three lives; each unprotected collision removes one, and reaching zero ends the game
PLAYER_RESPAWN_INVULNERABLE_SECONDS = 2.0  # protect the ship from collisions for two seconds after it reappears in the center following a lost life
PLAYER_SHOOT_SPEED = 500  # keep the original course bullet-speed setting for reference; current bullet speeds come from the selected entry in WEAPONS
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3  # keep the original course firing-delay setting for reference; current delays come from the selected entry in WEAPONS

# ---------- shots and weapons ----------
SHOT_RADIUS = 5  # use a five-pixel bullet radius when a Shot is created without a custom size; each weapon can supply its own size instead
SHOT_LIFETIME_SECONDS = 1.5  # remove bullets after 1.5 seconds so missed shots do not remain in the game forever or accumulate outside the window
WEAPONS = {  # create a dictionary, a collection that looks up values by names; WEAPONS["spread"], for example, gives the bullet settings saved under spread, which the ship reads when firing
    "single": {"cooldown": 0.3, "speed": 500, "radius": 5, "angles": [0], "pierce": False},  # single fires one straight bullet every 0.3 seconds at speed 500, radius 5; [0] means no angle offset and False means the bullet disappears on impact
    "spread": {"cooldown": 0.5, "speed": 450, "radius": 4, "angles": [-15, 0, 15], "pierce": False},  # spread fires three bullets every 0.5 seconds at speed 450, radius 4; the -15/0/15 degree angles create a fan and bullets disappear on impact
    "rapid": {"cooldown": 0.1, "speed": 650, "radius": 3, "angles": [0], "pierce": False},  # rapid fires a small straight bullet every 0.1 seconds at speed 650, radius 3; short cooldown means less waiting between shots
    "heavy": {"cooldown": 0.8, "speed": 400, "radius": 10, "angles": [0], "pierce": True},  # heavy fires a large straight bullet every 0.8 seconds at speed 400, radius 10; True lets the bullet survive a hit and potentially strike more rocks
}  # finish the WEAPONS dictionary; each inner dictionary groups the settings used together for one type of bullet

# ---------- asteroids ----------
ASTEROID_MIN_RADIUS = 20  # use 20 pixels as the smallest rock radius and as the step between sizes; splitting reduces a rock's radius by this amount
ASTEROID_KINDS = 3  # allow three rock sizes; multiplying the minimum radius by 1, 2, or 3 gives radii of 20, 40, or 60 pixels
ASTEROID_SPAWN_RATE_SECONDS = 0.8  # create another rock after about 0.8 seconds of active play; the asteroid creator accumulates elapsed time before creating one
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # calculate the largest rock radius as 20 times 3, or 60 pixels; also use this distance to place new rocks beyond the screen edges
ASTEROID_MIN_VERTICES = 9  # give each rock at least nine corners; vertices means the corner points connected to draw its irregular outline
ASTEROID_MAX_VERTICES = 14  # give each rock at most fourteen corners; the number is randomly selected between the minimum and this maximum
ASTEROID_LUMPINESS = 0.3  # allow each corner to sit up to 30% closer to the rock center than its full radius, creating an uneven outline inside its circular collision area
ASTEROID_MAX_SPIN = 45  # limit rock rotation to 45 degrees per second in either direction; a negative randomly chosen speed spins it the opposite way

# ---------- scoring and HUD ----------
SCORE_LARGE = 20  # award 20 points when a large rock is destroyed; both bullet hits and bomb explosions use this score value
SCORE_MEDIUM = 50  # award 50 points when a medium rock is destroyed, rewarding a smaller target more than a large rock
SCORE_SMALL = 100  # award 100 points when a small rock is destroyed; these are the smallest targets and disappear without splitting again
HUD_FONT_SIZE = 36  # use font size 36 for score, lives, bombs, and weapon text; HUD means heads-up display, the information shown while playing

# ---------- power-ups ----------
POWERUP_RADIUS = 12  # draw each collectible shield/speed item with a 12-pixel radius and use that circle when checking whether the ship touches it
POWERUP_LIFETIME_SECONDS = 8  # remove a collectible shield/speed item after eight seconds if the ship has not touched it; this is separate from how long its collected effect lasts
POWERUP_DROP_CHANCE = 0.15  # give each rock destroyed by a bullet a 0.15 probability, meaning a 15% chance, to leave a collectible shield or speed-boost item
POWERUP_DRIFT_SPEED = 20  # move collectible shield/speed items slowly at 20 pixels per second in a randomly chosen direction
SHIELD_DURATION_SECONDS = 5  # grant five seconds of collision protection after the ship touches a cyan shield item; collecting another refreshes this timer
SPEED_BOOST_DURATION_SECONDS = 5  # increase ship acceleration and maximum speed for five seconds after touching a yellow speed-boost item
SPEED_BOOST_MULTIPLIER = 1.5  # multiply normal acceleration and maximum speed by 1.5 while the speed bonus lasts, making both values 50% higher
POWERUP_COLORS = {"shield": "cyan", "speed": "yellow"}  # map item names to drawing colors in a dictionary: shield items are cyan and speed-boost items are yellow

# ---------- bombs ----------
BOMB_RADIUS = 8  # draw each dropped bomb with an eight-pixel radius; this is its visible size, not the much larger size of its explosion
BOMB_FUSE_SECONDS = 2.0  # wait two seconds after a bomb is dropped before it explodes; fuse means this countdown before detonation
BOMB_BLAST_RADIUS = 220  # destroy rocks touching the area within 220 pixels of an exploding bomb's center; rock size is also included in the overlap check
BOMB_START_COUNT = 3  # give the ship three bombs at the beginning of the game; each accepted B press spends one and the supply is not replenished
