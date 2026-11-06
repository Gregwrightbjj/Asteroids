SCREEN_WIDTH = 1280  # constant = value that doesn't change while the program runs (ALL_CAPS is the habit)
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20  # center-to-edge distance of the ship's hitbox (collision circle)
LINE_WIDTH = 2  # thickness of the drawn outline, in pixels
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 200  # pixels per second
ASTEROID_MIN_RADIUS = 20  # NEW: radius of the smallest asteroid (20 = about 40 pixels wide)
ASTEROID_KINDS = 3  # NEW: how many asteroid sizes exist (sizes 1, 2, 3)
ASTEROID_SPAWN_RATE_SECONDS = 0.8  # NEW: a new asteroid roughly every 0.8 seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # NEW: biggest radius, computed so it follows the others (20 * 3 = 60)
