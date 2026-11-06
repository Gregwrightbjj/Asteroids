SCREEN_WIDTH = 1280  # constant = value that doesn't change while the program runs (ALL_CAPS is the habit)
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20  # center-to-edge distance of the ship's hitbox (collision circle)
LINE_WIDTH = 2  # thickness of the drawn outline, in pixels
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 200  # pixels per second
ASTEROID_MIN_RADIUS = 20  # radius of the smallest asteroid
ASTEROID_KINDS = 3  # how many asteroid sizes exist
ASTEROID_SPAWN_RATE_SECONDS = 0.8  # a new asteroid roughly every 0.8 seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # biggest radius, computed (20 * 3 = 60)
SHOT_RADIUS = 5  # T1: bullet radius in pixels (5 = about 10 pixels wide)
PLAYER_SHOOT_SPEED = 500  # T5: bullet speed in pixels per second; faster than the ship (200)