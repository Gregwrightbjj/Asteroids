import random  # built-in random numbers (power-up drops)
import sys  # sys.exit() ends the program
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_LIVES,
    HUD_FONT_SIZE,
    POWERUP_DROP_CHANCE,
    BOMB_BLAST_RADIUS,
)
from logger import log_state, log_event  # course logging helpers
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle, spawn_explosion
from powerup import PowerUp
from bomb import Bomb
from background import make_starfield


def main():  # the whole game runs inside main()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")  # f-string: {} becomes its value
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()  # start pygame (also starts the font system)
    clock = pygame.time.Clock()  # stopwatch that caps and measures frame time
    dt = 0.0  # seconds since the last frame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # opens the window; screen = a Surface
    background = make_starfield()  # built ONCE, then copied every frame
    font = pygame.font.Font(None, HUD_FONT_SIZE)  # None = pygame's built-in font; created once, not every frame

    updatable = pygame.sprite.Group()  # Group = container for game objects
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    Player.containers = (updatable, drawable)  # groups every new object of that class auto-joins; set BEFORE creating any
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  # comma = a 1-item tuple
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)  # NOT in asteroids/shots, so particles never collide
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # starts at the center
    asteroid_field = AsteroidField()  # the spawner

    score = 0  # game state lives here, not on the ship
    lives = PLAYER_LIVES

    while True:  # game loop: one trip = one frame
        log_state()

        for event in pygame.event.get():  # ONE event loop per frame (get() empties the queue)
            if event.type == pygame.QUIT:  # window's X button
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:  # KEYDOWN = fires once per press (not while held)
                player.drop_bomb()

        updatable.update(dt)  # everything moves/counts down first, so collisions use fresh positions

        for bomb in bombs:  # bombs: did any fuse run out?
            if bomb.detonated:
                for asteroid in asteroids:
                    if bomb.position.distance_to(asteroid.position) <= BOMB_BLAST_RADIUS + asteroid.radius:  # inside the blast
                        score += asteroid.points()
                        spawn_explosion(asteroid.position, count=int(asteroid.radius / 2))
                        asteroid.kill()  # bombs obliterate: no splitting
                spawn_explosion(bomb.position, count=60, max_speed=300)  # big boom
                bomb.kill()

        for powerup in powerups:  # pickups
            if player.collides_with(powerup):  # player FIRST, so the triangle hitbox is used
                player.apply_powerup(powerup.kind)  # read kind before kill (it stays readable anyway)
                powerup.kill()

        for asteroid in asteroids:
            if not player.is_protected() and player.collides_with(asteroid):  # ship hit?
                log_event("player_hit")
                lives -= 1
                asteroid.split()  # remove the asteroid that hit us
                if lives <= 0:
                    print("Game over!")
                    sys.exit()
                player.respawn()
                continue  # this asteroid is gone; skip the bullet checks for it

            for shot in shots:  # nested loop: every bullet vs THIS asteroid
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += asteroid.points()  # points first, then split
                    asteroid.split()
                    if random.random() < POWERUP_DROP_CHANCE:  # random.random() = decimal from 0 to 1; True ~15% of the time
                        PowerUp(asteroid.position.x, asteroid.position.y, random.choice(["shield", "speed"]))
                    if not shot.pierce:  # piercing bullets keep flying
                        shot.kill()
                    break  # asteroid is dead; stop testing it against more bullets

        screen.blit(background, (0, 0))  # blit = copy a Surface onto another; covers every pixel, so it also erases the last frame
        for obj in drawable:
            obj.draw(screen)  # each object draws itself (polymorphism)

        hud_lines = [  # HUD drawn last so it sits on top
            f"Score: {score}",
            f"Lives: {lives}",
            f"Bombs: {player.bombs_left}",
            f"Weapon: {player.weapon}",
        ]
        for i, line in enumerate(hud_lines):  # enumerate gives a counter i (0, 1, 2, ...) with each line
            text = font.render(line, True, "white")  # render = turn text into a Surface; True = smooth edges
            screen.blit(text, (10, 10 + i * 40))  # stack lines 40 pixels apart

        pygame.display.flip()  # show the finished picture
        dt = clock.tick(60) / 1000  # cap at 60 FPS; milliseconds / 1000 = seconds


if __name__ == "__main__":  # true only when run directly (uv run main.py)
    main()