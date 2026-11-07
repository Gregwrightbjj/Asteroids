# ---------- screen ----------
SCREEN_WIDTH = 1280  # constant = value that never changes while running (ALL_CAPS is the habit)
SCREEN_HEIGHT = 720

# ---------- player ----------
PLAYER_RADIUS = 20  # ship hitbox radius in pixels (a pixel = one screen dot)
LINE_WIDTH = 2  # outline thickness for drawn shapes
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 200  # from the course; unused now (acceleration replaced move())
PLAYER_ACCELERATION = 400  # pixels/second gained every second while thrusting
PLAYER_DRAG = 1.0  # fraction of speed lost per second (friction)
PLAYER_MAX_SPEED = 350  # speed cap in pixels per second
PLAYER_LIVES = 3  # hits you can take
PLAYER_RESPAWN_INVULNERABLE_SECONDS = 2.0  # protection time after a respawn
PLAYER_SHOOT_SPEED = 500  # from the course; unused now (WEAPONS sets bullet speed)
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3  # from the course; unused now (WEAPONS sets cooldowns)

# ---------- shots and weapons ----------
SHOT_RADIUS = 5  # default bullet radius
SHOT_LIFETIME_SECONDS = 1.5  # bullets remove themselves after this long
WEAPONS = {  # dictionary = lookup table of key: value pairs; WEAPONS["spread"] = that weapon's settings
    "single": {"cooldown": 0.3, "speed": 500, "radius": 5, "angles": [0], "pierce": False},
    "spread": {"cooldown": 0.5, "speed": 450, "radius": 4, "angles": [-15, 0, 15], "pierce": False},
    "rapid": {"cooldown": 0.1, "speed": 650, "radius": 3, "angles": [0], "pierce": False},
    "heavy": {"cooldown": 0.8, "speed": 400, "radius": 10, "angles": [0], "pierce": True},
}  # angles = degrees each bullet is turned from straight ahead; pierce = survives hitting an asteroid

# ---------- asteroids ----------
ASTEROID_MIN_RADIUS = 20  # smallest asteroid radius
ASTEROID_KINDS = 3  # number of sizes
ASTEROID_SPAWN_RATE_SECONDS = 0.8  # seconds between spawns
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # biggest radius (20 * 3 = 60)
ASTEROID_MIN_VERTICES = 9  # fewest corners on a lumpy asteroid
ASTEROID_MAX_VERTICES = 14  # most corners
ASTEROID_LUMPINESS = 0.3  # each corner may sit up to 30% closer to the center
ASTEROID_MAX_SPIN = 45  # degrees per second, either direction

# ---------- scoring and HUD ----------
SCORE_LARGE = 20  # points per large asteroid
SCORE_MEDIUM = 50
SCORE_SMALL = 100  # smaller = harder to hit = more points
HUD_FONT_SIZE = 36  # HUD = heads-up display (on-screen text)

# ---------- power-ups ----------
POWERUP_RADIUS = 12
POWERUP_LIFETIME_SECONDS = 8  # uncollected pickups vanish after this
POWERUP_DROP_CHANCE = 0.15  # 15% chance when a bullet destroys an asteroid
POWERUP_DRIFT_SPEED = 20  # pixels per second
SHIELD_DURATION_SECONDS = 5
SPEED_BOOST_DURATION_SECONDS = 5
SPEED_BOOST_MULTIPLIER = 1.5  # scales thrust and the speed cap
POWERUP_COLORS = {"shield": "cyan", "speed": "yellow"}

# ---------- bombs ----------
BOMB_RADIUS = 8
BOMB_FUSE_SECONDS = 2.0  # time before it explodes
BOMB_BLAST_RADIUS = 220  # distance within which asteroids are destroyed
BOMB_START_COUNT = 3