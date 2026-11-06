import sys  # built-in module for system functions; needed for sys.exit()
import pygame  # library: code someone else wrote, used for the window and drawing
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # values stored in constants.py
from logger import log_state, log_event  # log_event writes to game_events.jsonl
from player import Player  # main.py must know the name Player to create one
from asteroid import Asteroid  # needed to set Asteroid.containers below
from asteroidfield import AsteroidField  # the spawner
from shot import Shot  # NEW: needed to set Shot.containers below


def main():  # def starts a function; the whole game runs inside main()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")  # f-string: {} is replaced by its value
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()  # starts pygame's internal parts; must come before other pygame calls

    clock = pygame.time.Clock()  # Clock object: a stopwatch that limits and measures frame time
    dt = 0.0  # delta time = seconds since last frame; 0.0 is a float (decimal number)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # opens the window; screen = a Surface (pixels you can draw on)

    updatable = pygame.sprite.Group()  # Group = container for many game objects; this one needs update()
    drawable = pygame.sprite.Group()  # this one needs draw(); an object can be in several groups
    asteroids = pygame.sprite.Group()  # only asteroids, so collisions can check them without the player
    shots = pygame.sprite.Group()  # T3: only bullets; keep the name `shots`, the lesson's test reads it from the log

    Player.containers = (updatable, drawable)  # groups every new Player auto-joins; set on the CLASS, before any Player exists
    Asteroid.containers = (asteroids, updatable, drawable)  # every Asteroid lands in all 3 groups
    AsteroidField.containers = (updatable,)  # only updatable; the comma makes a 1-item tuple
    Shot.containers = (shots, updatable, drawable)  # T4: static field (stored on the class); every bullet lands in all 3 groups; must be set BEFORE any Shot exists

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # instantiate = create an object; starts at the center
    asteroid_field = AsteroidField()  # the spawner

    while True:  # game loop: repeats forever; each trip is one frame (one picture)
        log_state()  # writes the game's state to the log file each frame

        for event in pygame.event.get():  # event = something that happened (key, click, window close)
            if event.type == pygame.QUIT:  # QUIT = the window's X button was clicked
                return  # ends main(), which exits the loop and closes the game

        updatable.update(dt)  # calls update(dt) on every member: player keys, asteroids, bullets, spawn timer

        for asteroid in asteroids:  # iterate = visit each asteroid one by one
            if asteroid.collides_with(player):  # True when the circles touch
                log_event("player_hit")  # records the hit in game_events.jsonl
                print("Game over!")  # must match exactly, capital G and the "!"
                sys.exit()  # stops the whole program right away

        screen.fill("black")  # paints every pixel black, wiping the last frame
        for obj in drawable:  # visit each drawable object one by one
            obj.draw(screen)  # draws the player, asteroids, and bullets
        pygame.display.flip()  # shows the finished picture in the window
        dt = clock.tick(60) / 1000  # waits so the game runs at most 60 FPS; ms / 1000 = seconds


if __name__ == "__main__":  # true only when run directly (uv run main.py)
    main()