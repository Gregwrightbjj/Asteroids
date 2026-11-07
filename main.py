import random  # bring in Python's random-number tools; this file uses them to decide whether a destroyed rock leaves a bonus item and which bonus it gives
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
from controls import draw_controls, draw_game_over  # look in controls.py and bring in the functions that draw keyboard instructions and the final-score/restart panel
from sounds import SoundEffects  # look in sounds.py and bring in the manager that generates arcade effects and music, remembers volume/mute, and plays named events without stopping the game loop


def reset_game(updatable, sounds):  # prepare a fresh round using the existing groups and audio manager, so restarting does not recreate the window or reset volume
    for obj in updatable:  # visit every old game object, including the invisible rock creator, before creating the next round's objects
        obj.kill()  # remove this object from all its groups, clearing old rocks, bullets, bombs, bonuses, effects, and the previous ship
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, sounds=sounds)  # create a new centered ship with its normal weapon, full bomb supply, zero velocity, and no leftover bonus timers
    asteroid_field = AsteroidField()  # create a new invisible rock producer with its timer at zero, preventing the old round's spawn timing from carrying over
    return player, asteroid_field  # give main references to the new ship and creator; the caller separately resets score, lives, and screen-state flags


def main():  # define the main game function; window/audio setup runs once, then the loop can play multiple rounds until the user exits
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")  # print the installed Pygame version in the terminal; the f prefix replaces the expression inside braces with its current value
    print(f"Screen width: {SCREEN_WIDTH}")  # print the configured window width in the terminal; {SCREEN_WIDTH} inserts that setting's numeric value into the text
    print(f"Screen height: {SCREEN_HEIGHT}")  # print the configured window height in the terminal; {SCREEN_HEIGHT} inserts that setting's numeric value into the text

    pygame.mixer.pre_init(44100, -16, 2, 512)  # request a small audio buffer before initialization, reducing the delay between an action and its sound; graphics can still start if no audio device opens
    pygame.init()  # initialize Pygame's systems, including the display, fonts, and audio mixer, before using them
    sounds = SoundEffects()  # generate and cache the effects/music once, or continue in silent mode if this computer has no working audio device
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

    player, asteroid_field = reset_game(updatable, sounds)  # create the first round using the same setup function that Enter will later use after game over

    score = 0  # start the player's total points at zero; main() owns this value because bullets and bombs can both increase it
    lives = PLAYER_LIVES  # copy the starting number of lives from the settings; losing a life changes this local value without changing the setting
    started = False  # store whether Enter has started the game; False means no, so the instruction screen is shown and game objects do not advance
    showing_help = False  # store whether the controls panel is open; False means closed, and setting it to True pauses game updates while instructions are visible
    game_over = False  # remember whether the final life was lost; True freezes the world and shows the final score until Enter begins a fresh round

    while True:  # repeat this game loop for menus and active rounds; only the close button or Esc leaves main, while losing all lives changes the displayed screen
        for event in pygame.event.get():  # collect pending window/keyboard events and handle each once; get() removes them from the queue, so use only one event-reading loop per frame
            if event.type == pygame.QUIT:  # check whether the user clicked the window's close button; QUIT is Pygame's name for that close request
                return  # leave main() immediately, ending the game loop and closing the program after this close-button or Esc request
            if event.type == pygame.KEYDOWN:  # handle a key-press event; this branch runs when a press is received rather than checking every frame whether the key is held
                if event.key == pygame.K_ESCAPE:  # check whether the pressed key was Esc; the return below exits main() from gameplay or either instruction screen
                    return  # leave main() immediately, ending the game loop and closing the program after this close-button or Esc request
                if event.key == pygame.K_m:  # accept M on the start screen, while paused, or during play to mute/unmute both music and effects
                    sounds.toggle_mute()  # reverse the mute setting and immediately stop current audio or restart the background loop
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):  # accept the ordinary minus key or the numeric keypad minus key as volume down
                    sounds.change_volume(-0.1)  # reduce master volume by ten percentage points, keeping it in the zero-to-one range
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):  # accept the equals/plus key or keypad plus so increasing volume does not require a particular Shift-key layout
                    sounds.change_volume(0.1)  # increase master volume by ten percentage points; if muted, remember the new level without unmuting
                elif event.key == pygame.K_RETURN:  # Enter starts play, resumes help, or resets the round when the final-score screen is open
                    if game_over:  # reset only after the last life is lost, so pressing Enter during ordinary gameplay cannot erase the current score
                        player, asteroid_field = reset_game(updatable, sounds)  # remove every old object and create a new ship and rock producer using the existing groups and audio settings
                        score = 0  # begin the new round with no points, rather than carrying over the previous final score
                        lives = PLAYER_LIVES  # restore all starting lives for the fresh round
                        game_over = False  # close the final-score panel so normal gameplay can run again
                        dt = 0.0  # prevent the time spent on the final-score screen from moving the newly created ship or advancing its timers
                    started = True  # mark the game as started so the next frames can update movement, create asteroids, and check collisions
                    showing_help = False  # close the instructions after Enter is pressed; the game can now reach the movement and collision code below
                elif event.key == pygame.K_h and started and not game_over:  # allow help during a live round, but keep H from replacing the final-score panel
                    showing_help = not showing_help  # reverse the help setting: not False becomes True to pause/show instructions, and not True becomes False to resume play
                elif event.key == pygame.K_b and started and not showing_help and not game_over:  # accept bombs only during active play, preventing drops on start, help, or final-score screens
                    player.drop_bomb()  # call the ship's drop_bomb method; it checks the remaining supply, spends one bomb, and creates it at the ship's current position

        if not started or showing_help or game_over:  # draw a menu instead of advancing gameplay before starting, while reading help, or after the last life is lost
            screen.blit(background, (0, 0))  # copy the background image onto the screen starting at its top-left corner (0, 0), painting over the previous frame
            if started:  # draw the frozen game objects behind the help panel only if gameplay has already started; the initial start screen shows just the background
                for obj in drawable:  # go through the objects that should be visible; obj refers to one ship, rock, bullet, or other object at a time
                    obj.draw(screen)  # call the current object's own drawing method, so each type draws its correct shape onto the same screen
            if game_over:  # choose the final-score panel when no lives remain, keeping the old world frozen behind it
                draw_game_over(screen, title_font, help_font, score)  # display the completed round's score and explain how to restart or quit
            else:  # use the usual keyboard guide before play or while the player has paused a live round
                draw_controls(screen, title_font, help_font, paused=started)  # choose start/resume wording using the same existing instruction-panel function
            audio_label = help_font.render(sounds.status_text(), True, "white")  # turn the current audio setting into text so volume and mute changes are visible even before playing
            screen.blit(audio_label, (SCREEN_WIDTH - audio_label.get_width() - 15, 15))  # place audio status above the instruction panel near the window's top-right corner
            pygame.display.flip()  # make the completed frame visible in the window after all its background, objects, and text have been drawn
            clock.tick(60)  # wait if needed so the start/help screen does not redraw more than roughly 60 times per second and waste processing power
            dt = 0.0  # set elapsed frame time to zero; before the first frame or after a menu pause, objects must not jump forward using old elapsed time
            continue  # skip movement, new rocks, countdowns, and contact checks while any menu is open, including the final-score screen

        log_state()  # ask the course logger to occasionally save the current objects and their positions to game_state.jsonl; this runs only during active play

        updatable.update(dt)  # call update(dt) on every object in the collection before collision checks, so positions and countdowns are current for this frame

        for bomb in bombs:  # check dropped bombs one at a time; bomb refers to the current bomb, which may or may not have finished its countdown
            if bomb.detonated:  # only process this bomb's explosion when its update method has set detonated to True after its fuse reaches zero
                sounds.play("bomb_blast")  # play one deep blast per bomb, avoiding a stack of identical sounds when it destroys several nearby rocks
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
                sounds.play(powerup.kind)  # use the collected item's shield/speed name to choose its distinct rising confirmation tone
                powerup.kill()  # remove the collected shield/speed item from every group so it disappears and cannot be collected repeatedly

        for asteroid in asteroids:  # go through the current rocks one at a time; asteroid refers to the particular rock being checked during this pass
            if not player.is_protected() and player.collides_with(asteroid):  # damage the ship only if it has neither shield nor respawn protection AND its triangular shape touches this rock
                log_event("player_hit")  # write a player_hit entry to the course event log so the collision can be checked later
                sounds.play("ship_hit")  # play the damage warning only when an unprotected collision actually removes a life
                lives -= 1  # subtract one from the remaining lives; -= means subtract the value and save the result back into the same variable
                asteroid.split()  # remove the hit rock and show its explosion; medium or large rocks also create two smaller rocks moving in different directions
                if lives <= 0:  # switch screens when the ship loses its final life instead of closing the program
                    print("Game over!")  # record the end of the round in the terminal while the window stays open to show its score and restart option
                    game_over = True  # remember that this round is finished so the next loop pass shows its final score and accepts restart input
                    player.kill()  # remove the destroyed ship from the update/drawing groups while leaving the remaining world frozen behind the panel
                    break  # stop checking more rocks immediately, preventing another hit or extra scoring after the round has ended
                player.respawn()  # move the ship back to the center, stop its movement, reset its direction, and grant a short period of protection
                continue  # start the next rock check because this rock was destroyed by hitting the ship; skip bullet checks against that removed rock

            for shot in shots:  # inside the current rock's loop, check every bullet against that rock; shot refers to one bullet at a time
                if asteroid.collides_with(shot):  # test whether the circular areas of this rock and this bullet touch or overlap, meaning the bullet hit the rock
                    log_event("asteroid_shot")  # write an asteroid_shot entry to the course event log whenever a bullet hits a rock
                    sounds.play("rock_hit")  # play a brief impact when a bullet actually hits, rather than when a shot merely passes nearby
                    score += asteroid.points()  # ask this rock how many points its size is worth and add that amount to score; += means add and store the new total
                    asteroid.split()  # remove the hit rock and show its explosion; medium or large rocks also create two smaller rocks moving in different directions
                    if random.random() < POWERUP_DROP_CHANCE:  # choose a decimal from 0 up to 1 and compare it with 0.15, giving each bullet-destroyed rock a 15% chance to leave a collectible item
                        PowerUp(asteroid.position.x, asteroid.position.y, random.choice(["shield", "speed"]))  # create a collectible at the destroyed rock's coordinates, randomly choosing shield protection or a speed boost as its effect
                    if not shot.pierce:  # remove the bullet only if its pierce setting is False; heavy bullets set it to True and can keep traveling after hitting rocks
                        shot.kill()  # remove this ordinary bullet from every group because it has already hit a rock and should no longer move or be drawn
                    break  # leave the bullet-checking loop for this destroyed rock so no second bullet scores another hit against the same rock

        if game_over:  # a final-life collision happened during this frame's rock loop
            dt = 0.0  # discard the old movement duration before entering the frozen final-score screen or starting a replacement round
            continue  # go straight to menu/event handling without running more gameplay or drawing the ordinary live-game HUD

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
        audio_label = help_font.render(sounds.status_text(), True, "white")  # make a visible readout of mute state and master volume while the game is running
        screen.blit(audio_label, (SCREEN_WIDTH - audio_label.get_width() - 15, 45))  # draw the audio readout below the help hint, keeping it separate from the score/lives text on the left

        pygame.display.flip()  # make the completed frame visible in the window after all its background, objects, and text have been drawn
        dt = clock.tick(60) / 1000  # limit play to about 60 frames per second and convert the measured milliseconds to seconds; the next update uses this duration for movement and timers


if __name__ == "__main__":  # run the game only when this file is launched directly, such as uv run main.py; importing main from another file does not start the game
    main()  # call the main function defined above; defining a function alone does not run its contents, so this call actually starts the game
