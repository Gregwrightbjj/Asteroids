import random  # bring in Python's random-number tools; this file uses them to decide whether a destroyed rock leaves a bonus item and which bonus it gives
import sys  # load Python's system tools so sys.exit() can stop the program when the player loses their last life
import pygame  # load Pygame, the library that creates the game window, reads keys, draws shapes, and manages groups of game objects
from constants import (  # import the named settings below from constants.py; parentheses allow this one import statement to span several lines
    SCREEN_WIDTH,  # bring in the window width from constants.py; set_mode below reads this number when it opens the window, and pixels are the tiny dots used to measure screen distances
    SCREEN_HEIGHT,  # bring in the window height from constants.py; together with SCREEN_WIDTH it determines the window size and the center where the ship is created
    PLAYER_LIVES,  # bring in the starting life count from constants.py; lives below copies this number and decreases it when an unprotected ship hits a rock
    HUD_FONT_SIZE,  # bring in the lettering size for score, lives, bombs, and weapon information; HUD means heads-up display, the status text visible during play
    POWERUP_DROP_CHANCE,  # bring in the chance that a bullet-destroyed rock leaves a shield or speed item; the random-number check below uses this fraction to decide whether to create one
    BOMB_BLAST_RADIUS,  # bring in how far a bomb explosion reaches from its center; the bomb-handling code compares this distance with the positions and sizes of nearby rocks
)
from logger import log_state, log_event  # look in logger.py and bring in two functions: log_state writes the current game information to a file, and log_event writes actions such as a ship getting hit
from player import Player  # look in player.py and bring in the Player class, a blueprint for creating the ship; its code handles steering, shooting, bombs, and temporary bonuses
from asteroid import Asteroid  # look in asteroid.py and bring in the Asteroid class, a blueprint for creating rocks; main.py uses its groups and checks when rocks hit the ship or bullets
from asteroidfield import AsteroidField  # look in asteroidfield.py and bring in AsteroidField, the blueprint for an invisible object that creates new rocks at intervals along the screen edges
from shot import Shot  # look in shot.py and bring in the Shot class, a blueprint for bullets; main.py assigns new bullets to the collections used for moving, drawing, and checking hits
from particle import Particle, spawn_explosion  # look in particle.py and bring in Particle, the blueprint for one tiny effect dot, and spawn_explosion, a function that creates many dots to look like an explosion
from powerup import PowerUp  # look in powerup.py and bring in the PowerUp class, a blueprint for cyan shield items and yellow speed items; touching one gives the ship its bonus
from bomb import Bomb  # look in bomb.py and bring in the Bomb class, a blueprint for a bomb; main.py checks when its countdown finishes and destroys nearby rocks
from background import make_starfield  # look in background.py and bring in the make_starfield function; calling it builds the black image with stars that will be drawn behind the game
from controls import draw_controls  # look in controls.py and bring in the draw_controls function; calling it draws the keyboard instructions on the start screen or the paused help screen


def main():  # define the main game function; its setup runs once, then its while loop handles the game repeatedly until the player exits
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")  # print the installed Pygame version in the terminal; the f prefix replaces the expression inside braces with its current value
    print(f"Screen width: {SCREEN_WIDTH}")  # print the configured window width in the terminal; {SCREEN_WIDTH} inserts that setting's numeric value into the text
    print(f"Screen height: {SCREEN_HEIGHT}")  # print the configured window height in the terminal; {SCREEN_HEIGHT} inserts that setting's numeric value into the text

    pygame.init()  # initialize Pygame's systems, including the display and fonts, before trying to open a window or draw text
    clock = pygame.time.Clock()  # create a timing object that measures time between frames and makes the loop wait when needed to stay near 60 frames per second
    dt = 0.0  # set elapsed frame time to zero; before the first frame or after a menu pause, objects must not jump forward using old elapsed time
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # open the game window at the requested width/height and save its drawing surface, an image-like object, in screen
    pygame.display.set_caption("Asteroids")  # set the window's title-bar text to Asteroids so the game can be identified in the desktop and taskbar
    background = make_starfield()  # call the imported function once to create the star image; reuse this image every frame instead of generating new stars repeatedly
    font = pygame.font.Font(None, HUD_FONT_SIZE)  # create the font for score/lives text; None selects Pygame's built-in font and HUD_FONT_SIZE sets its size
    title_font = pygame.font.Font(None, 56)  # create a larger built-in font, size 56, for the ASTEROIDS or PAUSED heading on the instruction panel
    help_font = pygame.font.Font(None, 28)  # create a smaller built-in font, size 28, for the keyboard explanations and the reminder shown during play

    updatable = pygame.sprite.Group()  # create an initially empty collection of game objects whose update(dt) methods must run each active frame to move them or change timers
    drawable = pygame.sprite.Group()  # create an initially empty collection of objects the drawing loop should display; invisible objects such as the asteroid creator stay out
    asteroids = pygame.sprite.Group()  # create a collection containing only rocks, allowing the game to check them against the ship, bullets, and bomb explosions
    shots = pygame.sprite.Group()  # create a collection containing only bullets, allowing the game to test each bullet against each rock
    powerups = pygame.sprite.Group()  # create a collection of shield and speed-boost items; the game checks whether the ship touches any of these items to collect them
    bombs = pygame.sprite.Group()  # create a collection containing dropped bombs so the game can find those whose countdown has ended and destroy nearby rocks

    Player.containers = (updatable, drawable)  # store these two collections on the Player blueprint; when Player(...) creates the ship, CircleShape's setup adds it to both so it will move and be drawn
    Asteroid.containers = (asteroids, updatable, drawable)  # tell every new rock to join the rock-only collection as well as the collections that update and draw objects
    AsteroidField.containers = (updatable,)  # give the asteroid creator only an update group because it has nothing to draw; the trailing comma makes a tuple containing one item
    Shot.containers = (shots, updatable, drawable)  # tell new bullets to join the bullet-only collection, move during updates, and appear during drawing
    Particle.containers = (updatable, drawable)  # tell explosion dots to update and draw, but keep them out of the rock/bullet collections so they never cause collision damage
    PowerUp.containers = (powerups, updatable, drawable)  # tell collectible shield/speed items to join their own collection, update their position/lifetime, and appear on screen
    Bomb.containers = (bombs, updatable, drawable)  # tell dropped bombs to join their own collection, update their countdown, and draw their flashing shape

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # create the ship in the window's center; dividing width and height by two gives the horizontal and vertical halfway points
    asteroid_field = AsteroidField()  # create the invisible object that produces rocks; its setup adds it to updatable, so the game calls its update function along with the visible objects

    score = 0  # start the player's total points at zero; main() owns this value because bullets and bombs can both increase it
    lives = PLAYER_LIVES  # copy the starting number of lives from the settings; losing a life changes this local value without changing the setting
    started = False  # store whether Enter has started the game; False means no, so the instruction screen is shown and game objects do not advance
    showing_help = False  # store whether the controls panel is open; False means closed, and setting it to True pauses game updates while instructions are visible

    while True:  # repeat this indented game loop indefinitely; one pass prepares one frame, and return or sys.exit() ends the game
        for event in pygame.event.get():  # collect pending window/keyboard events and handle each once; get() removes them from the queue, so use only one event-reading loop per frame
            if event.type == pygame.QUIT:  # check whether the user clicked the window's close button; QUIT is Pygame's name for that close request
                return  # leave main() immediately, ending the game loop and closing the program after this close-button or Esc request
            if event.type == pygame.KEYDOWN:  # handle a key-press event; this branch runs when a press is received rather than checking every frame whether the key is held
                if event.key == pygame.K_ESCAPE:  # check whether the pressed key was Esc; the return below exits main() from gameplay or either instruction screen
                    return  # leave main() immediately, ending the game loop and closing the program after this close-button or Esc request
                if event.key == pygame.K_RETURN:  # check whether Enter was pressed; RETURN is Pygame's name for Enter, which starts the game or resumes from help
                    started = True  # mark the game as started so the next frames can update movement, create asteroids, and check collisions
                    showing_help = False  # close the instructions after Enter is pressed; the game can now reach the movement and collision code below
                elif event.key == pygame.K_h and started:  # otherwise check for H, but accept it only after the game has started; and requires both conditions to be true
                    showing_help = not showing_help  # reverse the help setting: not False becomes True to pause/show instructions, and not True becomes False to resume play
                elif event.key == pygame.K_b and started and not showing_help:  # otherwise accept B only if play has started and help is closed, preventing bombs from being spent while reading instructions
                    player.drop_bomb()  # call the ship's drop_bomb method; it checks the remaining supply, spends one bomb, and creates it at the ship's current position

        if not started or showing_help:  # enter the instruction-screen branch if play has not begun OR the player has opened help; either condition is enough
            screen.blit(background, (0, 0))  # copy the background image onto the screen starting at its top-left corner (0, 0), painting over the previous frame
            if started:  # draw the frozen game objects behind the help panel only if gameplay has already started; the initial start screen shows just the background
                for obj in drawable:  # go through the objects that should be visible; obj refers to one ship, rock, bullet, or other object at a time
                    obj.draw(screen)  # call the current object's own drawing method, so each type draws its correct shape onto the same screen
            draw_controls(screen, title_font, help_font, paused=started)  # draw instructions using the two fonts; paused=started tells the function whether to show the start message or the paused/resume message
            pygame.display.flip()  # make the completed frame visible in the window after all its background, objects, and text have been drawn
            clock.tick(60)  # wait if needed so the start/help screen does not redraw more than roughly 60 times per second and waste processing power
            dt = 0.0  # set elapsed frame time to zero; before the first frame or after a menu pause, objects must not jump forward using old elapsed time
            continue  # start the next game-loop pass without moving objects, creating rocks, changing timers, or checking collisions while instructions are open

        log_state()  # ask the course logger to occasionally save the current objects and their positions to game_state.jsonl; this runs only during active play

        updatable.update(dt)  # call update(dt) on every object in the collection before collision checks, so positions and countdowns are current for this frame

        for bomb in bombs:  # check dropped bombs one at a time; bomb refers to the current bomb, which may or may not have finished its countdown
            if bomb.detonated:  # only process this bomb's explosion when its update method has set detonated to True after its fuse reaches zero
                for asteroid in asteroids:  # go through the current rocks one at a time; asteroid refers to the particular rock being checked during this pass
                    if bomb.position.distance_to(asteroid.position) <= BOMB_BLAST_RADIUS + asteroid.radius:  # compare center-to-center distance with explosion radius plus rock radius; this also destroys rocks whose edge overlaps the blast
                        score += asteroid.points()  # ask this rock how many points its size is worth and add that amount to score; += means add and store the new total
                        spawn_explosion(asteroid.position, count=int(asteroid.radius / 2))  # create moving effect dots at the rock's location; larger rocks create more dots, and int converts their count to a whole number
                        asteroid.kill()  # remove this rock from all groups immediately; a bomb destroys the whole rock rather than splitting it into smaller rocks
                spawn_explosion(bomb.position, count=60, max_speed=300)  # make the bomb explosion visibly larger by creating 60 dots whose randomly chosen speeds can reach 300 pixels per second
                bomb.kill()  # remove the exploded bomb from its collections so this same explosion cannot be processed again next frame

        for powerup in powerups:  # look at each collectible shield or speed-boost item one at a time; powerup is the current item and powerups is the collection of them
            if player.collides_with(powerup):  # ask whether the ship touches this item; calling the player's method uses the ship's triangular shape rather than a simple circle
                player.apply_powerup(powerup.kind)  # give the ship this item's effect; kind contains shield or speed, which determines which temporary protection or speed timer starts
                powerup.kill()  # remove the collected shield/speed item from every group so it disappears and cannot be collected repeatedly

        for asteroid in asteroids:  # go through the current rocks one at a time; asteroid refers to the particular rock being checked during this pass
            if not player.is_protected() and player.collides_with(asteroid):  # damage the ship only if it has neither shield nor respawn protection AND its triangular shape touches this rock
                log_event("player_hit")  # write a player_hit entry to the course event log so the collision can be checked later
                lives -= 1  # subtract one from the remaining lives; -= means subtract the value and save the result back into the same variable
                asteroid.split()  # remove the hit rock and show its explosion; medium or large rocks also create two smaller rocks moving in different directions
                if lives <= 0:  # check whether the ship has used its final life; <= includes both zero and any negative value
                    print("Game over!")  # write Game over! in the terminal to explain why the game is about to close
                    sys.exit()  # end the Python program immediately because no lives remain
                player.respawn()  # move the ship back to the center, stop its movement, reset its direction, and grant a short period of protection
                continue  # start the next rock check because this rock was destroyed by hitting the ship; skip bullet checks against that removed rock

            for shot in shots:  # inside the current rock's loop, check every bullet against that rock; shot refers to one bullet at a time
                if asteroid.collides_with(shot):  # test whether the circular areas of this rock and this bullet touch or overlap, meaning the bullet hit the rock
                    log_event("asteroid_shot")  # write an asteroid_shot entry to the course event log whenever a bullet hits a rock
                    score += asteroid.points()  # ask this rock how many points its size is worth and add that amount to score; += means add and store the new total
                    asteroid.split()  # remove the hit rock and show its explosion; medium or large rocks also create two smaller rocks moving in different directions
                    if random.random() < POWERUP_DROP_CHANCE:  # choose a decimal from 0 up to 1 and compare it with 0.15, giving each bullet-destroyed rock a 15% chance to leave a collectible item
                        PowerUp(asteroid.position.x, asteroid.position.y, random.choice(["shield", "speed"]))  # create a collectible at the destroyed rock's coordinates, randomly choosing shield protection or a speed boost as its effect
                    if not shot.pierce:  # remove the bullet only if its pierce setting is False; heavy bullets set it to True and can keep traveling after hitting rocks
                        shot.kill()  # remove this ordinary bullet from every group because it has already hit a rock and should no longer move or be drawn
                    break  # leave the bullet-checking loop for this destroyed rock so no second bullet scores another hit against the same rock

        screen.blit(background, (0, 0))  # copy the background image onto the screen starting at its top-left corner (0, 0), painting over the previous frame
        for obj in drawable:  # go through the objects that should be visible; obj refers to one ship, rock, bullet, or other object at a time
            obj.draw(screen)  # call the current object's own drawing method, so each type draws its correct shape onto the same screen

        hud_lines = [  # build a list of status messages for the heads-up display, meaning the score, lives, bombs, and weapon information shown during play
            f"Score: {score}",  # create the score label, replacing {score} with the player's current total points
            f"Lives: {lives}",  # create the lives label, replacing {lives} with the number of hits the ship can still survive before the game ends
            f"Bombs: {player.bombs_left}",  # create the bombs label using bombs_left, the remaining supply stored on the ship object
            f"Weapon: {player.weapon}",  # create the weapon label using the ship's selected weapon name, such as single, spread, rapid, or heavy
        ]
        for i, line in enumerate(hud_lines):  # go through the status messages with their row numbers; enumerate produces pairs such as (0, first message), (1, second message)
            text = font.render(line, True, "white")  # turn this message into a white text image that can be drawn; True smooths the edges of the letters
            screen.blit(text, (10, 10 + i * 40))  # copy the text image 10 pixels from the left; use its row number to place each message 40 pixels below the previous one

        hint = help_font.render("H: controls / pause", True, "white")  # create a small white text image reminding the player that H pauses the game and opens the keyboard instructions
        screen.blit(hint, (SCREEN_WIDTH - hint.get_width() - 15, 15))  # draw the help reminder at the top right; subtract its text width and 15 pixels from the screen width to leave a right-hand margin

        pygame.display.flip()  # make the completed frame visible in the window after all its background, objects, and text have been drawn
        dt = clock.tick(60) / 1000  # limit play to about 60 frames per second and convert the measured milliseconds to seconds; the next update uses this duration for movement and timers


if __name__ == "__main__":  # run the game only when this file is launched directly, such as uv run main.py; importing main from another file does not start the game
    main()  # call the main function defined above; defining a function alone does not run its contents, so this call actually starts the game
