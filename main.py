import pygame  # library: code someone else wrote, used for the window and drawing
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # constants: values that don't change, stored in constants.py
from logger import log_state  # function (named reusable code) that writes game_state.jsonl


def main():  # def starts a function; the whole game runs inside main()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")  # f-string: {} is replaced by its value
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()  # starts pygame's internal parts; must come before other pygame calls

    clock = pygame.time.Clock()  # Clock object: a stopwatch that limits and measures frame time
    dt = 0.0  # delta time = seconds since last frame; 0.0 is a float (decimal number)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # opens the window; screen is a Surface (pixels you can draw on)

    while True:  # game loop: repeats forever; each trip is one frame (one picture)
        log_state()  # writes the game's state to the log file each frame

        for event in pygame.event.get():  # event = something that happened (key, click, window close)
            if event.type == pygame.QUIT:  # QUIT = the window's X button was clicked
                return  # ends main(), which exits the loop and closes the game

        screen.fill("black")  # paints every pixel black, wiping the last frame
        pygame.display.flip()  # shows the finished picture in the window; keep before tick

        # tick(60) waits so the game runs at most 60 frames per second (FPS),
        # and returns milliseconds since the last tick; / 1000 converts to seconds.
        # Example: 17 ms -> 0.017, so dt = 0.017
        dt = clock.tick(60) / 1000
     


if __name__ == "__main__":  # true only when run directly (uv run main.py)
    main()