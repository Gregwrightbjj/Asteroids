import pygame  # library: code someone else wrote, used for the window and drawing
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # values stored in constants.py
from logger import log_state  # function (named reusable code) that writes game_state.jsonl
from player import Player  # main.py must know the name Player to create one


def main():  # def starts a function; the whole game runs inside main()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")  # f-string: {} is replaced by its value
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()  # starts pygame's internal parts; must come before other pygame calls

    clock = pygame.time.Clock()  # Clock object: a stopwatch that limits and measures frame time
    dt = 0.0  # delta time = seconds since last frame; 0.0 is a float (decimal number)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # opens the window; screen = a Surface (pixels you can draw on)

    updatable = pygame.sprite.Group()  # T1: Group = a container that holds many game objects; this one holds things that need update()
    drawable = pygame.sprite.Group()  # T1: this one holds things that need draw(); one object can be in several groups

    Player.containers = (updatable, drawable)  # T2: containers = groups every new Player auto-joins; set on the CLASS (the blueprint), so it must come BEFORE Player(...) is created

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # instantiate = create an object; it joins both groups automatically

    while True:  # game loop: repeats forever; each trip is one frame (one picture)
        log_state()  # writes the game's state to the log file each frame

        for event in pygame.event.get():  # event = something that happened (key, click, window close)
            if event.type == pygame.QUIT:  # QUIT = the window's X button was clicked
                return  # ends main(), which exits the loop and closes the game

        updatable.update(dt)  # T3.1: calls .update(dt) on EVERY object in the group; replaces player.update(dt)

        screen.fill("black")  # paints every pixel black, wiping the last frame
        for obj in drawable:  # T3.2: iterate = visit each item in the group one by one; obj = the current one
            obj.draw(screen)  # draws each object; replaces player.draw(screen); after fill (else black covers it), before flip
        pygame.display.flip()  # shows the finished picture in the window
        dt = clock.tick(60) / 1000  # waits so the game runs at most 60 FPS; ms / 1000 = seconds


if __name__ == "__main__":  # true only when run directly (uv run main.py)
    main()