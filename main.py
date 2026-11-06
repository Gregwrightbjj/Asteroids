import pygame  # library: code someone else wrote, used for the window and drawing
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # values stored in constants.py
from logger import log_state  # function (named reusable code) that writes game_state.jsonl
from player import Player  # main.py must know the name Player to create one
from asteroid import Asteroid  # NEW: needed to set Asteroid.containers below
from asteroidfield import AsteroidField  # NEW: the task says to import it


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
    asteroids = pygame.sprite.Group()  # NEW: holds only asteroids, so later lessons can check "every asteroid" without the player

    Player.containers = (updatable, drawable)  # containers = groups every new Player auto-joins; set on the CLASS, before any Player exists
    Asteroid.containers = (asteroids, updatable, drawable)  # NEW: static field (stored on the class, shared by all objects); every Asteroid lands in all 3 groups
    AsteroidField.containers = (updatable,)  # NEW: only updatable (needs update for its timer, draws nothing, isn't an asteroid); the comma makes a 1-item tuple

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # instantiate = create an object; starts at the center
    asteroid_field = AsteroidField()  # NEW: creates the spawner; after containers is set, as the task says

    while True:  # game loop: repeats forever; each trip is one frame (one picture)
        log_state()  # writes the game's state to the log file each frame

        for event in pygame.event.get():  # event = something that happened (key, click, window close)
            if event.type == pygame.QUIT:  # QUIT = the window's X button was clicked
                return  # ends main(), which exits the loop and closes the game

        updatable.update(dt)  # calls update(dt) on every member: player keys, asteroid movement, spawn timer

        screen.fill("black")  # paints every pixel black, wiping the last frame
        for obj in drawable:  # visit each drawable object one by one
            obj.draw(screen)  # draws the player and every asteroid
        pygame.display.flip()  # shows the finished picture in the window
        dt = clock.tick(60) / 1000  # waits so the game runs at most 60 FPS; ms / 1000 = seconds


if __name__ == "__main__":  # true only when run directly (uv run main.py)
    main()