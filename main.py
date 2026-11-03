# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------

# WHAT: loads the Pygame library so you can write pygame.something.
# WHY: the assignment says the game uses Pygame to open a window and draw.
# TERMS:
# - library: code someone else wrote that you reuse.
# - module: a single .py file (or a folder of them) you can import.
# EXAMPLE: after this line, pygame.init() is a valid thing to write.
import pygame

# WHAT: copies SCREEN_WIDTH and SCREEN_HEIGHT from your constants.py file.
# WHY: "Import SCREEN_WIDTH and SCREEN_HEIGHT from the constants.py file
# into main.py." The numbers live in one place, so changing them later
# means editing one file.
# TERM: constant = a variable not meant to change while the program runs
# (ALL_CAPS is the habit that signals this; Python doesn't enforce it).
# EXAMPLE: constants.py has SCREEN_WIDTH = 1280, so here SCREEN_WIDTH is 1280.
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# WHAT: copies the log_state function from your logger.py file.
# WHY: "import the log_state function from the logger module".
# TERM: function = a named, reusable block of code you run by writing its
# name followed by parentheses.
# EXAMPLE: log_state() runs the code inside it (it writes game_state.jsonl).
from logger import log_state


# ---------------------------------------------------------------------------
# THE MAIN FUNCTION
# ---------------------------------------------------------------------------

# WHAT: `def` starts a function definition named main. Everything indented
# 4 spaces under it is the function's body.
# WHY: the assignment says to put the setup "Within the main() function".
def main():
    # WHAT: print() shows text in the terminal. The f before the opening
    # quote makes an f-string, where {...} is replaced by the value inside.
    # WHY: your earlier tasks asked for startup messages and the screen size.
    # TERM: string = a piece of text in quotes.
    # EXAMPLE: prints "Screen width: 1280".
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # WHAT: sets up all of Pygame's internal parts (display, input, etc.).
    # WHY: "initialize pygame using the pygame.init() function at the
    # beginning of your program." Pygame calls need this to happen first.
    # EXAMPLE: skipping it can make the window or events fail to work.
    pygame.init()

    # WHAT: opens a 1280x720 window and returns a Surface, saved in the
    # variable `screen`. (SCREEN_WIDTH, SCREEN_HEIGHT) is a tuple, an
    # ordered pair of values, giving width then height in pixels.
    # WHY: "Use pygame's display.set_mode function to get a new instance of
    # GUI window." Later lines draw onto `screen`.
    # TERMS:
    # - variable: a named slot that stores a value.
    # - Surface: a rectangle of pixels (tiny colored dots) you can draw on.
    # - pixel: one dot of the screen.
    # EXAMPLE: screen now represents the window's drawing area.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # WHAT: `while True:` repeats its indented lines forever, because True
    # is always true. Only a `return` can end it.
    # WHY: "Create the game loop... Use an infinite while loop (e.g.
    # while True:)". A game must redraw many times per second.
    # TERMS:
    # - loop: code that repeats.
    # - frame: one complete picture shown on screen; each trip through this
    #   loop makes one frame.
    # EXAMPLE: trip 1 draws frame 1, trip 2 draws frame 2, and so on.
    while True:
        # WHAT: runs your logger function (no arguments needed).
        # TERM: argument = a value passed inside the parentheses; none here.
        # WHY: "Call log_state() - no arguments needed." The lesson's tests
        # read the file it writes, game_state.jsonl.
        # EXAMPLE: each frame adds a record to that file.
        log_state()

        # WHAT: pygame.event.get() returns a list of things that happened
        # since the last frame (key presses, clicks, the window's X button).
        # The for loop examines each one, with `event` as the current one.
        # WHY: "start processing the pygame event queue."
        # TERMS:
        # - event: one thing that happened.
        # - event queue: Pygame's waiting line of events; get() empties it.
        # EXAMPLE: you click the X, so the list holds one QUIT event.
        for event in pygame.event.get():
            # WHAT: checks whether this event is the "window closed" kind.
            # `==` means "is equal to" and gives True or False; the indented
            # line below runs only when it is True.
            # WHY: "if the event type is a pygame.QUIT event, return."
            # TERM: pygame.QUIT = Pygame's label for the close-button click.
            # EXAMPLE: a key press has a different type, so this is False
            # and nothing happens.
            if event.type == pygame.QUIT:
                # WHAT: `return` immediately ends main().
                # WHY: the while loop lives inside main(), so leaving main()
                # exits the loop. The program ends and the window closes,
                # which "will make the window's close button actually work."
                # EXAMPLE: you click X, return runs, and your terminal
                # prompt comes back without needing Ctrl+C.
                return

        # WHAT: paints every pixel of the screen black.
        # WHY: "Use the screen's .fill method to fill the screen with a solid
        # "black" color." It wipes the last frame so old drawings don't smear.
        # TERMS:
        # - method: a function attached to an object, called with a dot
        #   (screen is the object, fill is the method).
        # EXAMPLE: screen.fill("red") would make a solid red window.
        screen.fill("black")

        # WHAT: shows the finished picture in the real window.
        # WHY: "Use pygame's display.flip() function to refresh the screen.
        # Be sure to call this last!" Pygame draws into a hidden copy first,
        # and nothing appears until the flip. Anything drawn after it would
        # wait for the next frame.
        # EXAMPLE: fill makes the hidden picture black, flip shows it, so
        # you see a black window.
        pygame.display.flip()


# WHAT: runs main() only when you start this file directly, as in
# `uv run main.py`.
# WHY: this is the standard block `uv init` gives you.
# TERMS:
# - __name__: a variable Python sets automatically. It equals "__main__"
#   when the file is run directly, and the file's name when it is imported.
# - dunder: short for "double underscore"; names like __name__ with a
#   double underscore on both sides have special meaning to Python.
# EXAMPLE: `uv run main.py` makes the condition true, so main() runs.
if __name__ == "__main__":
    main()