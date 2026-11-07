import pygame  # bring in Pygame's drawing tools; this file uses them to make the dark instruction panel, rounded border, and partly see-through layer behind it


CONTROLS = (  # store the instruction rows in a tuple, an ordered collection; each inner pair contains the text for a key and the text describing its action
    ("Left / Right", "Rotate the ship"),  # instruction row for the arrow keys that turn the ship; the first string is the displayed key label and the second describes its action
    ("Up / Down", "Forward / reverse thrust"),  # instruction row for the arrow keys that change the ship's speed forward or backward along the direction it faces
    ("Space (hold)", "Shoot"),  # instruction row telling the player to hold Space to keep firing; the selected weapon determines the delay between bullets
    ("1 / 2", "Single shot / three-shot spread"),  # instruction row explaining that number key 1 selects one straight bullet and key 2 selects three bullets fired in a fan
    ("3 / 4", "Rapid fire / heavy piercing shot"),  # instruction row explaining that key 3 selects fast firing and key 4 selects large bullets that continue after hitting a rock
    ("B", "Drop a bomb (3 per game; 2-second fuse)"),  # instruction row explaining the three-bomb supply and the two-second countdown between dropping a bomb and its explosion
    ("H", "Pause and show / hide controls"),  # instruction row explaining that H stops game movement and timers while showing help, then resumes play when pressed again
    ("M", "Mute / unmute music and effects"),  # explain the audio toggle, which works during play and while either instruction screen is open
    ("- / +", "Lower / raise master volume"),  # explain volume adjustments; equals on the main keyboard also increases volume without requiring Shift
    ("Esc", "Quit the game"),  # instruction row explaining that Esc closes the game from gameplay, the start screen, or paused help
)


def draw_controls(screen, title_font, text_font, paused=False):  # define the function main.py calls to draw instructions; screen is where to draw, the fonts describe the lettering, and paused=False means show the start-screen version unless told the game is paused
    """Draw the shared start/help panel; the main loop pauses the game."""
    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # create an image layer matching the window dimensions; SRCALPHA allows each pixel to include transparency so the scene can show through
    shade.fill((0, 0, 0, 180))  # fill the layer with black using red/green/blue values 0/0/0; the fourth value 180 sets opacity between invisible 0 and fully solid 255
    screen.blit(shade, (0, 0))  # copy the partly transparent black layer over the whole window, making the background scene darker while the instructions are visible
    panel = pygame.Rect(0, 0, 900, 600)  # create a rectangle describing the panel's position and size: left 0, top 0, width 900, and height 600 pixels
    panel.center = screen.get_rect().center  # move the panel so its center matches the center of the window; get_rect() provides a rectangle covering the drawing surface
    pygame.draw.rect(screen, (12, 20, 35), panel, border_radius=16)  # fill the panel rectangle with a dark blue made from red/green/blue values 12/20/35; border_radius rounds each corner by 16 pixels
    pygame.draw.rect(screen, "cyan", panel, width=2, border_radius=16)  # draw the same rounded rectangle again as a cyan outline; width=2 draws only a two-pixel border instead of filling the rectangle

    def centered(text, font, y, color="white"):  # define a small function used only inside draw_controls: give it a message, lettering style, and height y, and it places that message in the horizontal middle; omitted colors are white
        rendered = font.render(text, True, color)  # convert the supplied text string into a drawable image using the supplied font and color; True makes the letter edges smoother
        screen.blit(rendered, rendered.get_rect(center=(panel.centerx, y)))  # position the text image so its center is at the panel's horizontal middle and height y, then copy that image onto the screen

    centered("PAUSED - CONTROLS" if paused else "ASTEROIDS", title_font, panel.top + 55)  # show PAUSED - CONTROLS when paused is True, otherwise ASTEROIDS; use the large font and place its center 55 pixels below the panel top
    centered("Destroy asteroids, collect power-ups, and survive.", text_font, panel.top + 105)  # draw the game's goal below the heading using the smaller font; power-ups means the shield/speed items collected by touching them
    for index, (key, action) in enumerate(CONTROLS):  # read the instruction rows one at a time; enumerate supplies a zero-based row number and (key, action) separates the two strings in each pair
        y = panel.top + 150 + index * 30  # place instruction rows thirty pixels apart so the movement, weapons, help, audio, and quit controls fit inside the same panel
        screen.blit(text_font.render(key, True, "cyan"), (panel.left + 40, y))  # create a cyan text image of the key label and draw it in the left column, 40 pixels from the panel's left edge
        screen.blit(text_font.render(action, True, "white"), (panel.left + 275, y))  # create a white text image explaining that key and draw it in the right column at the same row height
    centered("Cyan pickup: shield | Yellow pickup: speed boost", text_font, panel.top + 485)  # explain that touching a cyan collectible grants temporary protection, while touching a yellow collectible temporarily increases speed; these items are called pickups
    centered("Your ship drifts and wraps around the screen edges.", text_font, panel.top + 520)  # explain that the ship keeps moving after thrust is released and reappears on the opposite side when it leaves a screen edge
    centered("Press Enter or H to resume" if paused else "Press Enter to play",  # choose the bottom instruction based on paused: Enter starts a new game, while Enter or H returns from the paused help panel
             text_font, panel.top + 565, "cyan")  # finish the centered(...) call from the previous line, using the smaller font and cyan text 565 pixels below the panel's top edge


def draw_game_over(screen, title_font, text_font, score):  # draw the end-of-round panel using the final score passed by main; this function changes pixels, while main handles restart input and object reset
    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # create a partly transparent full-window layer so the frozen world remains faintly visible behind the score panel
    shade.fill((0, 0, 0, 190))  # darken the background with black at opacity 190 out of 255, making the final score easy to read
    screen.blit(shade, (0, 0))  # place the dark layer over the already-drawn frozen objects before drawing the panel itself
    panel = pygame.Rect(0, 0, 680, 340)  # describe a compact rectangle large enough for the title, final score, and restart/quit instructions
    panel.center = screen.get_rect().center  # move that panel to the exact center of the game window
    pygame.draw.rect(screen, (12, 20, 35), panel, border_radius=16)  # draw the same dark-blue rounded style used by the start/help screen
    pygame.draw.rect(screen, "cyan", panel, width=2, border_radius=16)  # outline the panel with a two-pixel cyan border so it stands out from the scene behind it
    title = title_font.render("GAME OVER", True, "white")  # make a large text image announcing that this round has ended
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.top + 65)))  # center the heading near the top of the panel
    messages = (f"Final score: {score}", "Press Enter to play again", "Press Esc to quit")  # store the final points total and the two available end-of-round actions in display order
    for index, message in enumerate(messages):  # visit each line with its zero-based row number so the same positioning calculation can space all three
        text = text_font.render(message, True, "cyan" if index == 0 else "white")  # highlight the score in cyan while leaving the restart and quit instructions white
        screen.blit(text, text.get_rect(center=(panel.centerx, panel.top + 145 + index * 65)))  # place the centered score/instruction lines sixty-five pixels apart inside the panel
