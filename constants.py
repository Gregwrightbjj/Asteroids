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
SHOT_RADIUS = 5  # bullet radius in pixels
PLAYER_SHOOT_SPEED = 500  # bullet speed in pixels per second
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3  # T2: cooldown = wait time between actions; 0.3 s = about 3 shots per second max