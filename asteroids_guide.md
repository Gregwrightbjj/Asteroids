# How Your Asteroids Game Works (and Why): Study Guide

This guide explains the code in this project, including its 14 Python files,
the start/help screens, and the connections between them. It describes the
current implementation rather than an earlier version of the course project.
You do not need to already know Python to start reading it.

Open the named Python file alongside each explanation. The comments beside
its code explain individual lines; this guide explains how those lines work
together. Small examples below illustrate ideas; they are not additional code
you need to paste into the game.

### How to read this guide

Read these parts in order the first time:

1. [The Python words and symbols used here](#python-basics).
2. [The controls](#game-controls), then [the overall loop](#game-loop).
3. [The file map](#file-map) and [classes, groups, and time](#core-mechanisms).
4. [What happens from launch to play](#game-startup).
5. [The individual file chapters](#file-chapters), using the suggested order below.
6. [Worked journeys across the files](#action-walkthroughs).
7. [Individual features](#game-features), [logging](#course-logging), and [current limits](#current-limits).

Use [the change map](#change-map) to find
the right files for an experiment. Use [the questions at the end](#understanding-questions)
to check whether the connections make sense.

<a id="contents" name="contents"></a>

### Complete contents

Each destination below has an explicit link target, including numbered
headings, so the links do not rely on the preview inventing a heading address.
The links in the file-chapter table jump within this guide; each chapter also
has an **Open the source** link to the actual Python file.

| Start here and learn the game | Detailed reference and practice |
| --- | --- |
| [Python words and symbols](#python-basics) | [7. Feature interaction map](#feature-interactions) |
| [0. Getting started and controls](#game-controls) | [8. Ordering rules](#ordering-rules) |
| [1. Before changing the project](#before-changing) | [9. Bugs and error messages](#debugging-basics) |
| [2. The overall game loop](#game-loop) | [10. Experiments](#learning-experiments) |
| [3. One frame in order](#frame-order) | [11. Glossary](#glossary) |
| [4. How the files connect](#file-map) | [14. Course logging](#course-logging) |
| [5. Classes, groups, time, vectors, and settings](#core-mechanisms) | [15. Current behavior and limits](#current-limits) |
| [6. Individual game features](#game-features) | [16. Where to make changes](#change-map) |
| [12. From launch to play](#game-startup) | [17. Understanding questions and answers](#understanding-questions) |
| [Detailed file chapters](#file-chapters) | [A method for tracing a problem](#trace-a-problem) |
| [13. Worked action journeys](#action-walkthroughs) | [Study sessions and prediction exercises](#study-sessions) |
| [Who stores and changes each value](#value-ownership) | [Python, Pygame, or project code?](#code-origins) |

Section 6's feature explanations are also linked individually here:

| Feature | Feature |
| --- | --- |
| [Arrow keys](#feature-arrow-keys) | [Rock outlines](#feature-rock-outlines) |
| [Screen-edge reappearance](#feature-wrapping) | [Triangle contact math](#triangle-contact-math) |
| [Scoring and text](#feature-scoring) | [Weapons](#feature-weapons) |
| [Lives and protection](#feature-lives) | [Collectible bonus items](#feature-bonuses) |
| [Acceleration and slowdown](#feature-acceleration) | [Bombs](#feature-bombs) |
| [Background](#feature-background) | [Creating new rocks](#feature-rock-creation) |
| [Explosion dots](#feature-explosion-dots) | [Instruction-panel drawing](#feature-help-drawing) |

| Each Python file, in the suggested reading order | What you will understand |
| --- | --- |
| [1. constants.py](#chapter-constants) | Where shared settings come from, their units, and which older settings are unused. |
| [2. circleshape.py](#chapter-circleshape) | The common setup behind visible objects, group membership, position, contact checks, and screen edges. |
| [3. shot.py](#chapter-shot) | A small complete object: create it, draw it, move it, expire it. |
| [4. player.py](#chapter-player) | Ship setup, triangle math, every ship function, keys, weapons, and protection. |
| [5. asteroid.py](#chapter-asteroid) | Rock shape, spinning, movement, scoring, and splitting. |
| [6. asteroidfield.py](#chapter-asteroidfield) | The invisible timer that chooses where and how new rocks enter. |
| [7. particle.py](#chapter-particle) | Short-lived explosion dots and the function that creates them. |
| [8. powerup.py](#chapter-powerup) | Collectible shield/speed items and why collecting them involves other files. |
| [9. bomb.py](#chapter-bomb) | A countdown and signal, with damage coordinated elsewhere. |
| [10. background.py](#chapter-background) | Star-image creation and the optional image-file alternative. |
| [11. controls.py](#chapter-controls) | The instruction text, panel layout, and drawing helper. |
| [12. logger.py](#chapter-logger) | Saved records, Python's inspection tools, timing, and file-writing rules. |
| [13. main.py](#chapter-main) | How all those parts are assembled and used in the correct order. |
| [14. sounds.py](#chapter-sounds) | How original effects and background music are synthesized, played, muted, and controlled. |

Reading the small bullet file before the larger ship file gives you a
concrete example of an object before handling all the ship's additional
behavior. Reading `main.py` last makes its names familiar. You can still
start with its chapter if you prefer seeing the coordinator first.

<a id="python-basics" name="python-basics"></a>

### Before the game: the Python words and symbols used here

A **file** such as `player.py` contains Python instructions. A Python file
that another file imports is also called a **module**. Here is an actual
line from the project:

```python
from circleshape import CircleShape
```

Read it as: **"Look in `circleshape.py` and bring in the name `CircleShape`
so this file can use it."** The filename is written without `.py` in an
import. `CircleShape` is the class defined inside that file; its capitalization
must match. Importing it does not create a ship or a rock.

Python runs the top-level instructions of an imported file when it first
loads that module in this process. Defining a function makes that function
available; it does not run the function's body. Later imports normally reuse
the already-loaded module. This is why importing `main` does not start a
game: its final `if __name__ == "__main__"` guard calls `main()` only when
that file is the program being launched directly.

| Word or symbol | Meaning here | Example from this project |
| --- | --- | --- |
| Variable | A name referring to a value; that value can be replaced later | `score = 0` starts the points total at zero. |
| `=` | Assign the value on the right to the name or stored field on the left | `self.weapon = "spread"` selects a weapon. |
| `==` | Compare two values; the answer is `True` or `False` | `kind == "shield"` asks which bonus was collected. |
| String | Text enclosed in quotes | `"shield"` is an item name, not a special Python command. |
| `True` / `False` | Yes/no values, also called booleans | `showing_help = True` means the help panel is open. |
| Function | A named set of instructions you can ask Python to run | `make_starfield()` creates the star image. |
| `def` | Define a function; its indented body runs when called | `def main():` describes the main game function. |
| Call | Run a function by writing parentheses after its name | `player.shoot()` asks this ship to fire. |
| Parameter / argument | A parameter is a function's input name; an argument is the value supplied when calling it | `dt` is a parameter of `update`; the measured seconds are its argument. |
| `return` | Leave the current function, optionally giving a value back | `return SCORE_SMALL` gives the caller the points value. |
| Class | A blueprint for making objects with related stored values and functions | `Player` describes ships; `Shot` describes bullets. |
| Object / instance | One actual thing made using a class | `player = Player(...)` makes one ship; each `Shot(...)` makes a separate bullet. |
| `self` | The particular object whose function is currently running | `self.bombs_left` is this ship's remaining bomb supply. |
| Attribute | A name belonging to an object or class, accessed with a dot | `player.weapon` reads the ship's selected weapon name. |
| Method | A function belonging to a class, used through an object | `player.respawn()` runs the ship's respawn function. |
| List | An ordered collection whose contents can change | `self.offsets = []` starts an empty collection of rock corners. |
| Tuple | An ordered collection whose entries cannot be replaced, added, or removed in place | `(shots, updatable, drawable)` groups three collection references; it does not copy those groups. |
| Dictionary | A collection that finds values by named keys | `WEAPONS["spread"]` finds the spread weapon's settings. |
| `[]` after a value | Look up one item using a position or key | `edge[0]` takes the first edge entry; `weapon["speed"]` takes a named setting. |
| `+=` / `-=` | Add/subtract and save the changed value | `lives -= 1` uses one life. |
| `if` / `elif` / `else` | Choose which indented instructions to run based on conditions | The item type chooses shield or speed behavior. |
| `and` / `or` / `not` | Require both conditions, accept either condition, or reverse a yes/no value | `not showing_help` means help is closed. |
| `for` | Repeat instructions for each item in a collection | `for powerup in powerups` checks one collectible bonus item at a time. |
| `while True` | Keep repeating until something explicitly exits or interrupts the loop | The outer game loop keeps producing frames. |
| `break` | Leave the nearest surrounding loop | After a bullet hit, stop testing more bullets against that destroyed rock. |
| `continue` | Skip to the next pass of the nearest surrounding loop | The help screen skips the rest of the outer game loop, freezing play. |
| `#` | Begin a comment Python ignores | The explanations beside the code are for the reader. |

Indentation is part of Python's meaning. The lines indented beneath an `if`
run only when that condition is true; lines beneath a loop repeat with that
loop. A `return` inside `Player.shoot()` stops that firing attempt. A `return`
inside `main()` leaves the whole game function. The same word can have a
different effect depending on which function contains it.

In a definition such as `def update(self, dt: float) -> None`, `float` and
`None` are **type hints**: notes that the input should be a decimal number
and no result value is returned. They do not make the function run or
automatically check every value. The colon ending the definition introduces
the indented function body; the colon after `dt` introduces its type hint.

<a id="game-controls" name="game-controls"></a>

## 0. Getting started and controls

This file is `asteroids_guide.md`, linked from [README.md](README.md).
Run `uv run main.py` from the project folder. The start screen explains
the controls; press **Enter** when ready. No asteroids spawn until you start.

| Key | Action |
| --- | --- |
| Left / Right | Rotate the ship |
| Up / Down | Apply forward / reverse thrust |
| Space (hold) | Shoot with the selected weapon |
| 1 / 2 | Select single shot / three-shot spread |
| 3 / 4 | Select rapid fire / heavy piercing shot |
| B | Drop a bomb: three per game, two-second fuse |
| H | Pause and show / hide controls during play |
| M | Mute / unmute both music and sound effects |
| - / + | Lower / raise master volume by ten percentage points; = and keypad +/- also work |
| Enter | Start, resume from help, or begin a fresh round after game over |
| Esc | Quit from any screen |

You can select any weapon immediately; weapons do not need unlocking.
Touch a cyan bonus item to gain a shield, or a yellow bonus item to increase
engine strength and maximum speed. These collectible items are sometimes
called **power-ups** or **pickups**. Each collected effect lasts five seconds;
an item left floating uncollected disappears after eight seconds.
Your ship keeps drifting after you release thrust and reappears across the
window when it leaves a screen edge.

### How the start and help screens work

`controls.py` holds the control descriptions and `draw_controls()`, shared
by the start screen and the paused help screen. Fonts are created once in
`main.py`. The HUD's **H: controls / pause** hint keeps help discoverable.

`main.py` uses three yes/no values (booleans): `started` begins as `False`,
`showing_help` toggles with H during a live round, and `game_over` becomes
True after the last life is lost. Enter starts, resumes, or resets a finished
round according to those values. Events are still
read on every frame, so closing the window and pressing Esc always work.
Bomb input is accepted only during play.

After the last life, `draw_game_over()` shows the final score over the frozen
world and explains Enter to play again or Esc to quit. H and B are ignored
on this panel. Enter calls `reset_game()`, which removes old objects from all
their groups and creates a new ship and invisible rock creator. Main resets
score to zero, lives to the starting count, `game_over` to False, help closed,
and dt to zero. A new ship restores its starting weapon, bombs, position,
velocity, angle, and timers. This is a new round in the same running program;
it does not recreate the window, regenerate music, or reset audio preferences.

Music and audio controls are separate from gameplay updates. The background
loop continues on the start/help screens; M and the volume keys work there
too. Muting immediately stops music and effects, while unmuting restarts the
music without replaying old impacts. The on-screen sound label shows volume,
mute, or an unavailable device. Audio settings start fresh on each launch.

While either screen is open, the loop draws the panel and skips updates,
spawning, collisions, and course state logging. That freezes movement,
bomb fuses, and protection/pickup timers. It still caps rendering at 60 FPS
and resets `dt` to zero, preventing a jump when play resumes. The logger's
wall-clock elapsed time can still include time spent reading help.

<a id="before-changing" name="before-changing"></a>

## 1. Safety first

- This project includes logging helpers that record actions such as
  `player_hit`. Changes to lives, input, or logging can change the records.
  Check the requirements of the particular course lesson before assuming
  this extended game produces the records that lesson expects.
- A Git **branch** is a named line of development. Save your current work
  before experimenting. A branch named `main` is not automatically an
  untouched or safe version; it contains whatever was committed there.
- Change one thing, run the game, and compare what you expected with what
  happened. Keep a record of changes you want to keep so you can undo an
  experiment without losing other work.

<a id="game-loop" name="game-loop"></a>

## 2. The 30-second picture

The game is a **loop** that runs about 60 times per second. Each trip (a
**frame**) does the same things in the same order:

1. Read events (window closed? start, help, quit, or bomb key pressed?).
   If on the start/help screen, draw it and skip gameplay for this frame.
2. Update every object (move it, count down its timers).
3. Resolve interactions (bombs, collecting shield/speed items, collisions, scoring).
4. Draw everything onto the screen, then show it.
5. Wait if necessary to cap redraws near 60 frames per second, and measure
   the time between clock calls (`dt`). A slow frame can still take longer.

The visible moving things are separate objects: the ship, rocks, bullets,
tiny explosion dots, collectible bonus items, and bombs. The invisible
`AsteroidField` is an object too. Other values, such as score, lives, and
timers, keep track of the game's condition; programmers call this its **state**.

<a id="frame-order" name="frame-order"></a>

## 3. One frame, step by step, and why the order matters

```
for event in pygame.event.get() events: close, start, help, quit, bomb
start/help screen?              draw panel, cap FPS, reset dt, continue
log_state()                     record active gameplay for course tests
updatable.update(dt)            every object moves / counts down
bombs: detonate?                explosion needs fresh positions
powerups: touched?              pickup needs fresh positions
asteroids: hit player? hit by shots?
background, then drawables      draw back to front
HUD text                        drawn last so it sits on top
pygame.display.flip()           show the finished picture
dt = clock.tick(60) / 1000      wait, then measure the frame time
```

Why this order:

- **Update before collisions.** The contact checks use the positions after
  this frame's movement, rather than the old positions before movement.
  This order does not guarantee detecting every contact: a fast bullet
  can still move completely past a small rock between checks.
- **Draw after all changes.** Objects destroyed this frame must not be drawn.
  Drawing last means the picture matches the game state.
- **Background first, HUD last.** Later drawing covers earlier drawing, like
  layers of paper.
- **`flip()` after drawing.** Drawing changes the screen Surface, the
  image-like area holding the window's pixels. `pygame.display.flip()`
  updates the whole display with that completed picture. The code does not
  need to present the picture separately after drawing every object.
- **`tick()` at the end.** It pauses just long enough for a 60 FPS cap and
  returns the milliseconds since the previous call, which becomes `dt`.
  `dt` is therefore the duration of the PREVIOUS frame, which is the
  standard approach.

<a id="file-map" name="file-map"></a>

## 4. How the files connect

```
constants.py        holds shared settings; imports no other project file
circleshape.py      imports constants
shot.py             imports circleshape, constants
particle.py         imports circleshape
powerup.py          imports circleshape, constants
bomb.py             imports circleshape, constants
asteroid.py         imports circleshape, constants, particle, logger
asteroidfield.py    imports asteroid, constants
player.py           imports circleshape, constants, shot, bomb
background.py       imports constants
controls.py         imports pygame; draws the shared start/help panel
sounds.py           uses Python tools and pygame to synthesize and play music/effects
logger.py           uses Python's own tools to write game-state/event logs
main.py             brings together settings, logging, game objects, and drawing helpers
```

These relationships describe **imports**, meaning which files bring in
names from other files. For example, `player.py` needs `Shot` from
`shot.py` to create bullets. `shot.py` does not need to import `Player`:
the ship hands the new bullet its starting position and speed.

`main.py` imports the object types and helpers directly; it reaches
`CircleShape` indirectly through those object files. `logger.py` imports
only Python's standard tools, and `controls.py` imports Pygame rather than
any other project file. Not literally every file imports `constants.py`.

A **circular import** happens when files depend on each other in a loop.
It can fail if one asks for a name before the other has finished defining
it. This project avoids that problem: `player.py` imports `Bomb`, but
`bomb.py` does not import `Player`. A circular import is not guaranteed to
fail in every possible Python program, but it would make this arrangement
harder to follow and initialize correctly.

**Separation of jobs** is the idea behind the file list:
`constants.py` = settings (numbers and named collections), `circleshape.py` = shared behavior, each object
file = what that object is and does, `main.py` = how objects interact.

| File | Main names defined there | Job and connection to the rest of the game |
| --- | --- | --- |
| [main.py](main.py) | `reset_game`, `main` | Creates collections, resets rounds, handles input, runs updates, coordinates contact/damage/scoring, and draws each frame. |
| [constants.py](constants.py) | `SCREEN_WIDTH`, `WEAPONS`, and other settings | Supplies shared values. It does not open a window or create game objects. |
| [circleshape.py](circleshape.py) | `CircleShape` | Supplies shared position, movement values, size, group setup, circle contact checks, and reappearance across screen edges. Its default `draw` and `update` do nothing. |
| [player.py](player.py) | `Player`, `point_segment_distance`, `side`, `point_in_triangle` | Handles held keys, ship motion, triangular contact checks, weapons, bomb creation, bonus effects, and returning after losing a life. |
| [asteroid.py](asteroid.py) | `Asteroid` | Gives each rock its outline and rotation, moves it, returns its score value, and splits it when asked. |
| [asteroidfield.py](asteroidfield.py) | `Edge`, `AsteroidField` | Describes four starting edges and creates new rocks at intervals. `Edge` is a type description; `AsteroidField` is the actual object blueprint. |
| [shot.py](shot.py) | `Shot` | Moves a bullet and removes it when its lifetime expires. `main.py`, rather than `Shot`, decides what happens when it hits a rock. |
| [bomb.py](bomb.py) | `Bomb` | Counts down and flashes. It signals that it has exploded; `main.py` applies the blast to rocks and awards points. |
| [powerup.py](powerup.py) | `PowerUp` | Moves, colors, and expires collectible shield/speed items. `main.py` detects collection; `Player.apply_powerup` gives the bonus. |
| [particle.py](particle.py) | `Particle`, `spawn_explosion` | Creates, moves, fades, and removes the tiny dots that make explosions visible. These dots cause no damage. |
| [background.py](background.py) | `make_starfield`, `load_background` | Creates the star image used by the game. The alternative image-loading function exists but is not called by `main.py`. |
| [controls.py](controls.py) | `CONTROLS`, `draw_controls`, `draw_game_over` | Stores instruction rows and draws start/help and final-score panels. Main decides which screen is open and whether gameplay runs. |
| [logger.py](logger.py) | `SpriteInfo`, `GroupInfo`, `log_state`, `log_event` | Describes and saves records for inspecting gameplay. It does not control ship movement or decide collisions. |
| [sounds.py](sounds.py) | `EFFECTS`, `make_sound`, `make_music`, `SoundEffects` | Synthesizes original music/effects once and manages playback, mute, and shared volume. Main passes this manager to the ship. |

<a id="core-mechanisms" name="core-mechanisms"></a>

## 5. Core mechanisms in depth

### 5.1 Classes, inheritance, and which method runs

A **class** is a blueprint; an **instance** is one object built from it.
`Player` is the blueprint; `player = Player(...)` creates an actual ship.
Each call to `Shot(...)` similarly creates a separate bullet with its own
age, position, and speed.

`class Player(CircleShape)` means **"Define the ship blueprint by building
on the existing `CircleShape` blueprint."** This reuse is called
**inheritance**. In that relationship, `CircleShape` is called the base or
parent class and `Player` the child class. Those words describe the reuse
relationship, not two visible things sitting on screen.

`CircleShape.__init__` stores `position`, `velocity`, and `radius` on each
new object when the ship's setup calls it. `Player` also has access to
`CircleShape` functions such as `wrap`. The ship replaces `draw`, `update`,
and `collides_with` with ship-specific versions.

**The lookup rule:** when you write `thing.method()`, Python looks in
`thing`'s own class first, then its parent. If the child defines
`draw`, the child's `draw` runs; the parent's empty `draw` is a safety
default. Replacing a parent's method is called **overriding**.

Why this matters here:

- The game loop calls `obj.draw(screen)` on a mixed list of ships,
  asteroids, bullets, particles, pickups, and bombs. Each one draws itself
  differently, and the loop does not need to know which is which.
  This is **polymorphism**: one call, different behavior per object.
- `collides_with` is the sharpest example. `asteroid.collides_with(ship)`
  runs the asteroid's (circle) version. `ship.collides_with(asteroid)` runs
  the ship's own triangle version. Same two objects, different answer,
  depending on which one is before the dot.

`super().__init__(...)` asks the blueprint being built on to run its setup.
For a ship, the chain is `Player.__init__` → `CircleShape.__init__` →
Pygame's `Sprite.__init__`. Each level does a different part of setup.
The ship level adds weapons and timers; `CircleShape` adds position and
size; Pygame's Sprite setup joins the supplied groups. Skipping the
`CircleShape` setup without replacing its work would leave needed values
such as `position` missing.

`self` makes this work for many objects. Inside `Shot.update`,
`self.age += dt` changes the age of the particular bullet being updated,
not the age of every bullet. A **method** is simply a function belonging
to a class and normally called through an object, as in `player.shoot()`.

### 5.2 Groups and containers: how objects join the game

`pygame.sprite.Group` is a collection. Your game has several, and one object
can be in several (like overlapping circles of a Venn diagram):

| Group | Members | Used for |
|---|---|---|
| `updatable` | ship, rocks, bullets, explosion dots, bonus items, bombs, and the invisible rock creator | `updatable.update(dt)` calls each member's `update` function. |
| `drawable` | every visible object, excluding the invisible rock creator | The draw loop calls each member's `draw` function. |
| `asteroids` | asteroids only | collision checks |
| `shots` | bullets only | collision checks |
| `powerups` | collectible shield/speed items only | Check whether the ship touches an item. |
| `bombs` | bombs only | detonation checks |

**What actually happens when you write `Shot(x, y)`:**

1. Python runs `Shot.__init__`, which calls `super().__init__(x, y, radius)`.
2. That reaches `CircleShape.__init__`, which asks
   `hasattr(self, "containers")`: "does this object have an attribute named
   containers?" Because you set `Shot.containers = (shots, updatable, drawable)`
   on the CLASS in `main.py`, the answer is yes.
3. It calls `super().__init__(*self.containers)`. The `*` spreads the tuple
   into separate arguments, and pygame's Sprite constructor adds the new
   object to each group.

So creating an object is also registering it. That is why
`Shot.containers = ...` must run BEFORE the first Shot is created: the
object reads `containers` at the moment of creation.

**`kill()`** removes an object from every group it is in. Later group passes
will no longer include it. It does not delete its stored values or erase
references held by code or an already-started loop. Python can release the
object once no references keep it alive.

**Why separate groups at all?** Different loops need different slices. The
collision loop must test asteroids against bullets, not particles against
anything. Particles are in `updatable` and `drawable` but NOT in `asteroids`
or `shots`, so they are invisible to collision code. Choosing which groups an
object joins is how you choose what it can do.

**Changes during a loop:** this installed version of Pygame takes a list
of members when a group iteration or `Group.update()` starts. New members
do not join that already-running pass. However, a later loop in the same
frame takes a fresh list and can see them.

For example, `Player.update()` can create a bullet while
`updatable.update(dt)` is already running. That bullet does not receive
its own `update()` in the current pass, but the later bullet contact loop
and drawing loop can see it immediately. New rocks created by
`AsteroidField.update()` can also be checked and drawn before their first
movement update.

Removing a member does not remove it from a list a loop already captured.
That is why you must reason about the loop currently running, rather than
treating `kill()` as an instruction to erase every reference immediately.

### 5.3 Time, units, and `dt`

Every number has a unit. Speeds are pixels per second, turn rates are
degrees per second, timers are seconds. `dt` is seconds per frame (about
0.0167 at 60 FPS). Multiplying "per second" by "seconds" gives the amount to
change THIS frame:

```
position  += velocity * dt     (pixels/second x seconds = pixels)
rotation  += turn_speed * dt   (degrees/second x seconds = degrees)
```

This makes straight-line motion depend on elapsed seconds rather than the
number of frames. For example, a bullet moving at 500 pixels per second
travels about 8.33 pixels in a 1/60-second frame or 16.67 pixels in a
1/30-second frame. It does not guarantee identical gameplay at every frame
rate: acceleration, slowdown, collisions, and large time steps still affect
the result.

**The timer pattern** appears many times in this game, in two forms:

- **Count down to zero** (cooldowns): `shoot_timer`, `invulnerable_timer`,
  `shield_timer`, `speed_boost_timer`, a bomb's `fuse`. Set it to a duration,
  subtract `dt` each frame, and treat `<= 0` as "done".
- **Count up to a limit** (lifetimes): a particle's, shot's, or pickup's
  `age`. Add `dt` each frame and `kill()` the object when `age` reaches
  the limit.

Countdowns can dip below zero, for example -0.004. A positive value means
the effect or waiting period is still active; zero or less means it has
finished. Age/lifetime checks work the other way, using `age >= lifetime`.

### 5.4 Vectors: position, velocity, direction

A `Vector2` is an (x, y) pair that can be a point or an arrow.

- `position`: where the object is.
- `velocity`: an arrow showing which way and how fast it moves per second.
- A **direction** is an arrow of length 1 (a *unit vector*). The ship's
  facing is `Vector2(0, 1).rotate(rotation)`. `(0, 1)` points DOWN the
  screen because y grows downward. The ship was designed so that rotation 0
  means the tip points down.
- `rotate(angle)` returns a NEW vector and leaves the original untouched.
- Multiplying an arrow by a number changes its length, not its direction.
  That is how a direction becomes a velocity: `direction * speed`.
- `+=` on a vector changes it in place.

**Why `Shot(self.position.x, self.position.y)` passes numbers, not the
vector:** `CircleShape.__init__` builds a brand-new `Vector2(x, y)`. If it
reused the ship's own vector, every bullet would share it and move with the
ship. Copying the numbers gives each object its own position.

### 5.5 Constants

Many shared tuning settings (speeds, sizes, firing delays, chances) live in
`constants.py`. Some literal numbers remain in the code, such as the panel
size in `controls.py` and the initial rock-speed range in `asteroidfield.py`.
The shared settings provide one place to tune much of the game feel; names explain
meaning (`PLAYER_MAX_SPEED` beats `350`), and several files can read the
same setting definition instead of maintaining separate copies. Values derived from others
(`ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS`) stay
consistent automatically when you change the inputs.

<a id="game-features" name="game-features"></a>

## 6. Every feature in depth

<a id="feature-arrow-keys" name="feature-arrow-keys"></a>

### 6.1 Arrow keys

**Mechanism:** `pygame.key.get_pressed()` returns the state of every key
right now. `keys[pygame.K_LEFT]` is True while the left arrow is held.
`Player.update` checks the keys every frame and calls `rotate` or
`accelerate`.

**Why `-dt` for the opposite direction:** `rotate(dt)` adds turn; `rotate(-dt)`
subtracts it. One method, two directions, by flipping the sign of the input.
The same trick makes Down apply thrust backward.

**Polling:** checking held keys every frame is called *polling*. It is right
for continuous actions (turning, thrusting, firing).

<a id="feature-wrapping" name="feature-wrapping"></a>

### 6.2 Wrap-around

**Mechanism:** `CircleShape.wrap(margin)` compares the position to the four
screen edges. If the object is more than `margin` pixels past an edge, its
coordinate jumps to just beyond the opposite edge, so it slides back in.

**Why a margin and not the exact edge:** wrapping at the edge would make the
object pop in half-visible. Waiting until the whole object is off-screen
(margin = its radius) hides the jump.

**Why asteroids use `ASTEROID_MAX_RADIUS`:** the spawner puts new asteroids
exactly `ASTEROID_MAX_RADIUS` outside the screen. With any smaller margin,
the asteroid would count as "already past the edge" and be teleported to the
far side the moment it spawned. Using the same number the spawner uses keeps
the two features compatible. (Two files sharing one constant is the design
payoff from 5.5.)

**Connections:** `wrap` lives in `CircleShape` so any object can use it.
The ship, rocks, and collectible shield/speed items call it. Bullets do not:
they continue in a straight line, including off screen, until their lifetime
ends. Bombs stay where dropped, and explosion dots do not wrap.
Contact checks do not wrap with the image: two objects on opposite sides
of a screen edge are not tested as if those edges touch each other.

<a id="feature-scoring" name="feature-scoring"></a>

### 6.3 Scoring and the on-screen text

**Mechanism:** `score` is a variable in `main()`. When a bullet destroys an
asteroid, `score += asteroid.points()`.

**Why `points()` belongs to the asteroid:** the asteroid knows its own
size, so it answers "what am I worth?". `main.py` doesn't need to know the
size rules. Small asteroids are worth more because they are harder to hit.

**Drawing text:** `font.render("Score: 520", True, "white")` makes a
**Surface** (a rectangle of pixels) containing the text. `screen.blit(surface,
(x, y))` copies those pixels onto the screen. The font object is created
once before the loop because creating it each frame would be wasteful.
The HUD is drawn after the game objects so it sits on top.

**Worked numbers:** if bullets destroy one large rock, both medium rocks
it produces, and all four small rocks they produce, the total is
20 + 2 × 50 + 4 × 100 = 520. Bombing the original large rock gives only
20 points because a bomb does not create those smaller rocks. A rock
destroyed by hitting the ship gives no points.

<a id="feature-lives" name="feature-lives"></a>

### 6.4 Lives, respawning, and protection

**Mechanism:** `lives` is a variable in `main()`. When the ship is hit:
lives drop by one; at zero the round ends and the final-score panel opens;
otherwise
`player.respawn()` resets the ship to the center with zero velocity and
starts the invulnerability timer.

**What happens to the rock:** the code calls `asteroid.split()`, removing
the original rock and possibly creating two smaller rocks at its position.
This does not guarantee the area is empty. The ship moves back to the
center, which may be elsewhere, and its two-second protection prevents an
immediate further loss of life while it gets moving again.

**Why `continue`:** after the player-hit branch, the asteroid is dead. The
`continue` skips the bullet checks so a destroyed asteroid isn't tested
again. On the final life, the code instead sets `game_over`, removes the
ship, and uses `break` to stop checking more rocks. Main then continues to
the menu branch so no more gameplay is processed after that round ends.

**`is_protected()`:** answers "is this ship protected right now?" It returns
True while either the respawn timer or
the shield timer is running. `main.py` asks the question without knowing
the reasons, so adding another protection source later changes only
`Player`.

**Blinking:** only the respawn-protection timer makes the triangle blink;
having a shield by itself does not. While that timer is positive, `draw`
skips drawing the triangle when
`int(timer * 10) % 2 == 0`. `timer * 10` counts tenths of a second left;
`% 2` (remainder after dividing by 2) alternates 0, 1, 0, 1 each tenth, so
the ship vanishes and returns every 0.1 s.

**Where values live:** `score` and `lives` are local variables in `main()`.
The ship stores its own motion, weapon, bombs, and protection timers.
An optional future design could put overall game values in a `Game` class;
this project currently has no such class.

<a id="feature-acceleration" name="feature-acceleration"></a>

### 6.5 Acceleration

The current code uses the Up/Down arrows to change **velocity**, meaning
horizontal/vertical movement speed, and that velocity changes position:

```
thrust:   velocity += facing * ACCELERATION * dt     (keys)
friction: velocity *= (1 - DRAG * dt)                (every frame)
motion:   position += velocity * dt                  (every frame)
```

Motion runs every frame even with no keys held, which creates drifting.

**Drag math:** the factor each frame is `1 - 1.0 * 0.0167 = 0.983`. Over a
second (60 frames) that compounds to about 0.36, so after one second of
coasting the ship has roughly a third of its speed.

**Speed cap:** `velocity.length()` is the current speed. If it exceeds
`PLAYER_MAX_SPEED`, `scale_to_length` shrinks the arrow to the cap while
keeping its direction.

**Reverse thrust:** passing `-dt` pushes opposite the ship's nose. If the
ship is moving nose-first, this initially brakes and can then reverse its
motion. If it is drifting sideways or facing a different direction than
its travel, the effect depends on both directions; Down is not a universal
stop button.

**Connections:** `respawn()` resets `velocity` or the new ship would keep
drifting. The speed power-up (6.11) multiplies acceleration and the cap.

<a id="feature-background" name="feature-background"></a>

### 6.6 Background

**Mechanism:** `make_starfield()` builds one **Surface** at startup and draws
150 random dots on it. Each frame, `screen.blit(background, (0, 0))` copies
that finished picture over the whole screen.

**Why it replaces `screen.fill("black")`:** `fill` existed to erase last
frame. The background covers every pixel, so it erases too.

**Why build once:** drawing 150 circles every frame is wasted work. A
finished Surface is copied far faster.

**Image option:** `pygame.image.load(path)` reads a file; `.convert()`
matches it to the screen's pixel format for speed (so it must run after
`set_mode`); `transform.scale` resizes it to the window.

<a id="feature-explosion-dots" name="feature-explosion-dots"></a>

### 6.7 Explosions (particles)

**Mechanism:** a **particle** is a tiny object with a position, a velocity,
and a limited life. `spawn_explosion(position, count)` creates `count`
particles at one spot, each with a random direction and speed. Each frame a
particle moves and ages. Its brightness is `255 * (1 - age / lifetime)`, so
it fades, and it `kill()`s itself when `age >= lifetime`.

**Why particles are CircleShapes:** reuse. They get `position`, `velocity`,
`radius`, and group registration for free.

**Why they aren't in `asteroids` or `shots`:** the collision loops iterate
those groups, so particles can never hurt or be hurt. Group membership
decides behavior (5.2).

**Connections:** `Asteroid.split()` calls `spawn_explosion`, and the bomb
(6.12) calls it too. `Particle.containers` must be set in `main()` first.

<a id="feature-rock-outlines" name="feature-rock-outlines"></a>

### 6.8 Lumpy asteroids

**Mechanism:** when an asteroid is created it builds a list of
**offsets**: points around the center at evenly spaced angles
(`i * 360 / count`), each pulled inward by a random amount. Drawing places
each offset relative to the current `position` and draws a polygon. A random
`spin` rotates the offsets every frame for a tumbling look.

**Drawing and contact checks use different shapes:** the code uses a circle
of `radius` as its invisible contact-checking area, often called a **hitbox**,
even though the visible outline is uneven. The corners only move
inward, so the visible rock never pokes outside its hitbox.

**Connections:** `split()` creates new `Asteroid` objects, so every fragment
gets its own random shape with no extra code.

<a id="triangle-contact-math" name="triangle-contact-math"></a>

### 6.9 Triangular hitbox

The contact check handles these two cases; they can both be true:

1. The circle's center is **inside** the triangle, or
2. The circle crosses an **edge**, meaning the center is within one radius
   of some edge.

(If the center is outside and the circle overlaps, the circle must cross an
edge, so test 2 catches it.)

**Test 1, point in triangle:** `side(p, a, b)` computes a number whose sign
says which side of edge `a-b` the point is on. Do it for all three edges. If
the signs are mixed, the point is outside; if they all agree (or are zero),
it is inside.

**Test 2, distance to an edge:** find the closest point on the finite
straight edge between `a` and `b`, then compare its distance from the
circle's center with the circle's radius. The code uses:

```python
ab = b - a
length_sq = ab.length_squared()
t = (p - a).dot(ab) / length_sq
t = max(0, min(1, t))
```

`ab` is the horizontal/vertical change from `a` to `b`. `length_sq` is
`ab.x * ab.x + ab.y * ab.y`. `.dot(ab)` multiplies the horizontal parts
together and the vertical parts together, then adds them. Dividing by the
squared edge length expresses the closest location as a fraction of the
edge: `t=0` is at `a`, `t=0.5` is halfway, and `t=1` is at `b`.

For a concrete example, let `a=(0, 0)`, `b=(10, 0)`, and the circle center
`p=(4, 3)`. The edge runs horizontally for ten pixels. The calculation
gives `t=0.4`, so the closest edge point is `(4, 0)`. Its distance from the
circle center is three pixels. A radius-three circle touches that edge;
a radius-two circle does not reach it.

If the calculated fraction is below 0 or above 1, `max(0, min(1, t))`
keeps it at the nearest endpoint instead. Limiting a value to a range is
called **clamping**. Before dividing, the real function also checks for a
zero-length edge: if `a` and `b` are the same point, it returns the distance
to that point rather than dividing by zero.

**The call-order trap:** the ship's `collides_with` only runs when called as
`player.collides_with(asteroid)` (5.1). That's why `main.py` calls it that
way.

<a id="feature-weapons" name="feature-weapons"></a>

### 6.10 Weapon types

**Data-driven design:** instead of four `shoot` methods, there is one
`shoot` and a table (`WEAPONS`, a dictionary of dictionaries):

```
"spread": cooldown 0.5, speed 450, radius 4, angles [-15, 0, 15], pierce False
```

`shoot` looks up the current weapon, sets the cooldown, and loops through
`angles`, creating one bullet per angle, each rotated by that angle from the
ship's facing. The firing function can use another entry without a new
firing method, but a playable new weapon also needs a way to select it in
`Player.update()` and instructions in `controls.py` and the documentation.

**Pierce:** a piercing bullet isn't killed when it hits. It keeps flying
and can hit more asteroids.

**Possible repeated hits:** `split()` creates two smaller rocks at the
original rock's center. A heavy bullet survives the first hit and may
also hit these smaller rocks if their later positions overlap it. It is
not guaranteed to hit both or clear the entire family: movement, hit
locations, and the bullet's remaining lifetime matter.

**Bullet lifetime:** every `Shot` has an `age` and kills itself after
`SHOT_LIFETIME_SECONDS`. Without it, bullets fly forever and the `shots`
group grows without limit.

**Default parameters:** `Shot(x, y, radius=SHOT_RADIUS, pierce=False)` lets
older calls like `Shot(x, y)` keep working.

<a id="feature-bonuses" name="feature-bonuses"></a>

### 6.11 Power-ups

**Collectible object:** `PowerUp` is a small drifting ring with a `kind`
(`"shield"` or `"speed"`). It ages and `kill()`s itself after 8 seconds if
nobody collects it.

**Creation:** when a bullet destroys an asteroid,
`random.random() < POWERUP_DROP_CHANCE` has a 15% chance, with the current
setting, to create a collectible shield or speed item at that spot. The
15% applies to each qualifying hit, not a promise of exactly fifteen
items for every hundred destroyed rocks. Bombs and ship hits do not run
this item-creation branch.

**Collect:** each frame, `main()` checks `player.collides_with(powerup)`.
On contact, `player.apply_powerup(kind)` sets a timer and the pickup is
removed from its groups. Both effects last five seconds after collection.
Collecting the same kind again resets its timer to five; it does not add
five to the remaining time or increase the bonus strength.

**Effects are just timers:**

- Shield: `shield_timer` > 0 makes `is_protected()` true and draws a ring.
- Speed: `speed_boost_timer` > 0 makes `boost = 1.5` (otherwise 1) in
  `accelerate`, scaling both the thrust and the speed cap. The line
  `A if condition else B` is a *conditional expression*: it picks A or B.

**Why it fits together so easily:** timers (5.3), `is_protected` (6.4), and
`accelerate` (6.5) were already there. Power-ups mostly flip existing
switches.

<a id="feature-bombs" name="feature-bombs"></a>

### 6.12 Bombs

**Mechanism:** pressing B calls `player.drop_bomb()`, which reduces
`bombs_left` and creates a `Bomb` at the ship's position. The bomb's fuse
counts down. At 0 it sets `detonated = True`. `main()` notices the flag,
destroys every asteroid within `BOMB_BLAST_RADIUS + asteroid.radius`
of the bomb (center-to-center distance), awards points, spawns
explosions, and kills the bomb.

**Events vs polling:** dropping a bomb uses a `KEYDOWN` **event**, which
fires once per press. If it used polling, holding B would drop a bomb every
frame. One-time actions use events; continuous actions use polling.

**Why the Bomb only sets a flag:** destroying asteroids needs the
`asteroids` group and the score, which live in `main()`. The bomb stays
simple and unaware of them, and `main()` coordinates. This is **low
coupling**: objects don't reach into each other's business.

**Why `kill()`, not `split()`:** the bomb is meant to obliterate. It is a
design choice; try `split()` to feel the difference.

**One event loop:** `pygame.event.get()` empties the queue. Handle
everything (quit and bomb key) inside the same loop; a second `get()` loop
would see nothing.

<a id="feature-rock-creation" name="feature-rock-creation"></a>

### 6.13 How new rocks enter the game

`AsteroidField` has no position or drawing of its own. It exists so
`updatable.update(dt)` can call its timer code just like the updates on
visible objects. Creating a new object and adding it to the game is often
called **spawning**; that is what `spawn_timer` and `spawn()` refer to here.

`self.spawn_timer += dt` accumulates active seconds. Once it exceeds
`ASTEROID_SPAWN_RATE_SECONDS`, the code resets the timer to zero and creates
one rock. It does not create several catch-up rocks after an unusually long
frame, and it discards time beyond the interval when resetting the timer.

Each entry in `edges` has two parts:

| Part | Example for the left edge | What it means |
| --- | --- | --- |
| Direction | `pygame.Vector2(1, 0)` | Begin with rightward movement, pointing from outside the left edge into the window. |
| Position function | `lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)` | Given a fraction `y` from 0 to 1, choose a starting position somewhere along the left edge, just beyond the visible area. |

`lambda` defines a short unnamed function. In that example its input is
called `y`, but it is initially a fraction, not yet a pixel coordinate.
Multiplying by the screen height converts it into a coordinate. With the
current height of 720, input `0.25` gives a vertical position of 180 pixels;
the horizontal position is -60, just outside the left edge.

`random.choice(self.edges)` picks one edge entry. `edge[0]` reads its first
part, the direction. Multiplying it by a random speed from 40 to 100 gives
actual movement speed, and rotating it by a random angle from -30 to 30
degrees varies the approach. `edge[1](random.uniform(0, 1))` reads its second
part, then calls that stored function to make the starting position.

The top, right, and bottom entries do the same job with different coordinates
and inward directions. The chosen size multiplier 1, 2, or 3 gives a radius
of 20, 40, or 60. Finally, `spawn()` creates an `Asteroid` at that position
and assigns its velocity. `Asteroid` builds the visible shape; it does not
choose which outer edge produced it.

`Edge = tuple[...]` near the top of the file is a **type alias**, a name for
the expected two-part layout, rather than a visible game object. `Callable`
in that description means its second part can be called as a function.

<a id="feature-help-drawing" name="feature-help-drawing"></a>

### 6.14 How the instruction panel is drawn

`controls.py` provides the image of the start/help screen. It does not read
keys or stop timers; the surrounding branch in `main.py` does those jobs.
The `CONTROLS` tuple stores pairs such as `("Space (hold)", "Shoot")`.
These strings describe the keys for the player; changing the string alone
does not change which key `Player.update()` reads.

`draw_controls()` draws in this order:

1. Create a screen-sized Surface using `SRCALPHA`, which permits partial
   transparency, and fill it with `(0, 0, 0, 180)`. The first three numbers
   mean no red, green, or blue: black. The fourth is opacity from 0 to 255.
   Copying this layer over the scene darkens it without completely hiding it.
2. Make a `Rect`, a description of position and size, for the 900-by-600
   panel. Assigning `panel.center = screen.get_rect().center` moves that
   rectangle to the window's center; it does not draw anything yet.
3. Draw the dark filled rectangle, then its cyan border. `border_radius=16`
   rounds the corners, while `width=2` draws a two-pixel outline.
4. Use the inner `centered()` function to turn messages into text images
   and position their centers along the panel's horizontal middle. Its
   `color="white"` input supplies white when no color is passed.
5. `enumerate(CONTROLS)` supplies both each row number and its pair of
   strings. The row number times 30 controls spacing; one string is drawn
   in the left key-label column and the other in the right explanation column.
6. Draw the bonus-item explanation, movement note, and start/resume prompt.
   The `paused` input selects whether the heading and prompt say to start
   or resume. `main.py` presents the completed screen with `display.flip()`.

The panel and text coordinates are fixed pixel values. Adding more rows or
making the window smaller does not automatically rearrange them. The layout
must be checked if either changes.

<a id="feature-interactions" name="feature-interactions"></a>

## 7. Feature interaction map

| Feature | Depends on | Affects |
|---|---|---|
| Arrow keys | pygame key constants | `Player.update` |
| Wrap | screen size, `ASTEROID_MAX_RADIUS` | ship, rocks, collectible bonus items |
| Scoring | `Asteroid.points`, HUD font | main loop, bombs |
| Lives | `respawn`, `is_protected` | main loop, HUD |
| Acceleration | velocity, drag, `dt` | ship motion, respawn, speed boost |
| Background | screen Surface | replaces `fill` |
| Particles | groups, lifetimes | split, bombs |
| Lumpy asteroids | random, Vector2 rotate | asteroid drawing only |
| Triangle hitbox | `triangle()`, geometry | ship collisions (asteroids and pickups) |
| Weapons | `WEAPONS`, `Shot` args | shoot, bullet-hit logic (pierce) |
| Power-ups | timers, `is_protected`, `accelerate` | ship, drops from asteroid hits |
| Bombs | events, particles, scoring | main loop, HUD |
| Start/help panel | `started`, `showing_help`, `draw_controls` | pauses movement, creating rocks, contacts, and game timers |
| Logging | calls in `main`, `Asteroid.split`, and Python time/inspection tools | writes state records and named events to text files |

<a id="ordering-rules" name="ordering-rules"></a>

## 8. Ordering rules (and what breaks if you ignore them)

| Rule | If broken |
|---|---|
| Set `X.containers` before creating any X | Setup may fail or objects may miss the expected groups, so the game does not update or draw them. |
| `update` before collision checks | Checks would use positions from before this frame's movement; even correct ordering cannot prevent every missed fast collision. |
| `break` after a bullet hit | One asteroid can split twice |
| `continue` after a ship hit | A dead asteroid is tested against bullets |
| `player.collides_with(...)` (player first) | The triangle code never runs |
| Create the font once, before the loop | Recreating it each frame repeats setup work the game does not need. |
| Background first, HUD last, `flip` last | Layers cover each other wrongly |
| Decrease timers before handling keys | Cooldown checks use stale values |
| `.convert()` after `set_mode` | "No video mode" error |
| One `pygame.event.get()` per frame | Events silently disappear |

<a id="debugging-basics" name="debugging-basics"></a>

## 9. Bugs you may meet and how to read them

| Symptom | Likely cause |
|---|---|
| `NameError: name 'X' is not defined` | Missing import in THAT file (each file has its own names) |
| `ImportError: cannot import name` | Misspelled name, or it isn't in `constants.py` yet |
| `AttributeError: ... no attribute 'X'` | Attribute never created (for example, missing from `__init__`) |
| `TabError` / `IndentationError` | Tabs mixed with spaces; use 4 spaces |
| Objects invisible | Not in `drawable`, or `containers` set too late |
| Objects frozen | Not in `updatable`, or `update` missing `position += ...` |
| New asteroids teleport instantly | Wrap margin smaller than the spawn distance |
| Ship contact feels too generous | `asteroid.collides_with(player)` uses circles, while `player.collides_with(asteroid)` uses the ship triangle. |
| Ship cannot lose a life temporarily | Check `invulnerable_timer` and `shield_timer`; either positive value makes the ship protected. |
| Holding B drops many bombs | Used `get_pressed()` instead of a `KEYDOWN` event |
| Explosion dots cause contact-check errors | Check whether they were accidentally added to `asteroids` or `shots`; those loops expect rock/bullet-specific behavior. |
| A window appears only as a blank taskbar preview with `[WARN:COPY MODE]` | WSLg may have a display-service problem even while Python runs; see the WSL note below. |

**Debug habit:** add `print(...)` for one value (a timer, a distance), run,
and watch the terminal. Remove it afterward.

**WSL note:** this session previously had a WSLg shared-memory error that
prevented the game window from appearing. Saving WSL work, running
`wsl --shutdown` in Windows PowerShell, reopening Ubuntu, and launching
the game again resolved that occurrence. This is a troubleshooting step,
not a claim that every blank window has the same cause. Shutdown stops
the running WSL sessions, so save work first.

<a id="learning-experiments" name="learning-experiments"></a>

## 10. Experiments to learn by changing things

1. Set `PLAYER_DRAG = 0`. While coasting without thrust or a collision, the
   ship no longer gradually slows. Find the multiplication that explains why.
2. Set `ASTEROID_LUMPINESS = 0.7`. How do the rocks look, and do hits still
   feel fair?
3. Set `BOMB_FUSE_SECONDS = 0.5`. What changes in how you use bombs?
4. Change `"angles": [-15, 0, 15]` to `[-30, -15, 0, 15, 30]`.
5. The heavy weapon already has `"pierce": True`. Temporarily change it to
   `False` and compare whether a bullet disappears at its first hit.
6. Set `POWERUP_DROP_CHANCE = 1.0` to test every pickup quickly, then
   put it back.
7. Move the wrap margin for asteroids to `ASTEROID_MIN_RADIUS`. Watch
   spawns break, then explain why with section 6.2.

<a id="glossary" name="glossary"></a>

## 11. Glossary

- **Attribute:** a named value or function accessible through an object or class, such as `self.rotation` or `player.shoot`.
- **blit:** copy one Surface onto another.
- **Branch:** a separate line of Git commits.
- **Class / instance:** a blueprint / one object built from it.
- **Clamp:** limit a value to a minimum and maximum.
- **Constant:** a setting intended to stay unchanged during a run, usually named in capitals; Python does not make capitalized values impossible to change.
- **Container:** generally something holding other values; this project's `containers` name stores the groups an object should join during setup.
- **Coupling:** how much one part of the code depends on another.
- **Default parameter:** a parameter with a fallback value.
- **Dictionary:** a lookup table of key/value pairs.
- **dt:** seconds since the last frame.
- **Event:** something that happened once (key press, window close).
- **Flag:** a True/False attribute used as a signal.
- **Frame:** one picture of the game (about 60 per second).
- **Group:** a container of game objects.
- **HUD:** on-screen information such as score and lives.
- **Hitbox:** the shape used for collision.
- **Inheritance:** defining a class by building on another class; functions can be reused, and calling the earlier setup creates the stored values that setup assigns.
- **Override:** redefine a parent's method in a child.
- **Particle:** a tiny short-lived object used for effects.
- **Polling:** asking "is it true right now?" every frame.
- **Polymorphism:** one call (`draw`) behaving differently per object.
- **Surface:** a rectangle of pixels you can draw on.
- **Tuple:** an ordered collection whose entries cannot be changed in place; commas form tuples, and `(updatable,)` is a one-entry example.
- **Unit vector:** an arrow of length 1 carrying only a direction.
- **Vector2:** an (x, y) point or arrow.

<a id="game-startup" name="game-startup"></a>

## 12. From launch to the first playable frame

This is the startup sequence in the order the code performs it. Keep
[main.py](main.py) open beside this section.

1. **You run `uv run main.py` from the project folder.** `uv` prepares the
   project's Python environment and runs the file. `pyproject.toml` declares
   Python 3.13 or newer and Pygame 2.6.1; `uv.lock` records dependency details.
   These files describe the environment, not ship behavior.
2. **Python loads the imported names at the top of `main.py`.** The class
   and function definitions become available. Defining `Player` does not
   make the ship yet. Loading `logger.py` also sets its initial clock time
   and logging flags, because those assignments are outside functions.
3. **The final guard calls `main()`.** Because this file was launched directly,
   `__name__` is `"__main__"`, so the bottom call actually starts the game
   function. Python does not start a function just because it was defined.
4. **`main()` prints startup information and initializes Pygame.** It requests
   a short audio buffer before initialization, then makes the sound manager,
   clock, and 1280-by-720 window. Sound generation happens once; an unavailable
   audio device switches audio to silent mode while graphics can still start.
5. **It makes reusable drawing resources.** `make_starfield()` creates the
   background once. The three font objects describe the lettering for
   status text, the panel title, and smaller instructions.
6. **It creates the six empty groups.** These collections will hold the
   objects to update, draw, or check for particular interactions. At this
   point the collections do not contain the ship or any rocks.
7. **It sets each class's `containers`.** This happens before object creation
   so each new object's setup knows which groups it must join. `Shot.containers`
   is a setting on the bullet blueprint; it is not itself a bullet.
8. **It creates the actual ship and asteroid creator.** `Player(...)` runs
   the ship setup and the setup it builds on. The ship appears in the update
   and drawing groups. `AsteroidField()` joins the update group, with a
   timer initially at zero, but it has no visible drawing.
9. **It initializes overall game values.** Score begins at zero, lives at
   three, `started` at False, and `showing_help` at False.
10. **The loop begins on the start screen.** Input events are still read,
    but the instruction-screen branch draws the panel, waits to limit
    redraw speed, resets `dt`, and uses `continue`. The update and collision
    code below it does not run, so the invisible creator makes no rocks yet.
11. **Enter changes the flags.** `started = True` and `showing_help = False`
    let this loop pass reach active gameplay. The first update after the
    start screen uses `dt = 0`, so elapsed movement time begins cleanly.
12. **Later frames advance the game.** The creator accumulates active elapsed
    seconds. When its timer exceeds 0.8, it chooses an edge, speed, angle,
    position, and one of the three rock sizes, then creates an `Asteroid`.

### Why the setup happens outside the loop

The game should have one ship, one background image, and one set of
collections. Making them again every frame would repeatedly reset them or
create unwanted duplicates. In contrast, reading keys, moving objects,
checking contact, and drawing the current picture must repeat during play.

This difference is a useful question when reading `main()`: **is this line
preparing something once, or doing part of the next frame?**

<a id="file-chapters" name="file-chapters"></a>

## File-by-file chapters

These chapters follow the reading order in the contents, not alphabetical
order. Within each file, the functions are explained in the order they
appear in its source. The **why** explains the purpose of this arrangement;
it does not mean this is the only possible way to write a game.

The worked numbers are examples with stated starting conditions. Random
choices, elapsed time, and collisions mean your actual run need not produce
those exact values. Follow the linked source for the current instructions.

<a id="chapter-constants" name="chapter-constants"></a>

### File 1: constants.py — the shared settings

**Open the source:** [constants.py](constants.py). [Back to contents](#contents).

**Its job and why it exists.** This file gives meaningful names to settings
that several parts of the game need. A name such as `BOMB_BLAST_RADIUS`
explains more than a bare `220` repeated in different files. Changing one
shared definition also avoids separately editing copies of the same rule.
It imports nothing, defines no functions, and creates no on-screen objects.
Its assignments run when Python first imports it in this process.

**What it stores, in source order:**

| Settings | Current values and meaning | Why another file needs them |
| --- | --- | --- |
| `SCREEN_WIDTH`, `SCREEN_HEIGHT` | 1280 × 720 pixels | Main opens the window; the ship finds its center; backgrounds and edge positions fit it. |
| `PLAYER_RADIUS`, `LINE_WIDTH` | Ship size 20 pixels; outlines 2 pixels thick | Ship geometry and visible outlines need dimensions. Radius means distance from center to edge; it is not the full width. |
| `PLAYER_TURN_SPEED` | 300 degrees per second | `Player.rotate` converts elapsed seconds into an angle change. |
| `PLAYER_SPEED` | 200, an unused older setting | Current motion uses acceleration and velocity, so this value does not move the ship. |
| `PLAYER_ACCELERATION`, `PLAYER_DRAG`, `PLAYER_MAX_SPEED` | 400 pixels/second of velocity change per second, drag factor 1.0, normal maximum 350 pixels/second | The engine adds motion, drag reduces it, and `accelerate` limits speed. These are different jobs. |
| `PLAYER_LIVES`, `PLAYER_RESPAWN_INVULNERABLE_SECONDS` | Three starting lives; two seconds of protection after a lost life | Main tracks the life count; the ship tracks its temporary protection. |
| `PLAYER_SHOOT_SPEED`, `PLAYER_SHOOT_COOLDOWN_SECONDS` | 500 and 0.3, both older unused settings | Current firing reads the selected `WEAPONS` entry instead. |
| `SHOT_RADIUS`, `SHOT_LIFETIME_SECONDS` | Default radius 5 pixels; lifetime 1.5 seconds | A bullet can use the default size, and every bullet expires so missed shots do not accumulate forever. |
| `WEAPONS` | Four named settings dictionaries | One shooting function can make different bullets by looking up the selected name. |
| `ASTEROID_MIN_RADIUS`, `ASTEROID_KINDS`, `ASTEROID_MAX_RADIUS` | 20 pixels, three sizes, maximum `20 * 3 = 60` | The creator chooses size; splitting reduces it; wrapping and starting positions share the maximum. |
| `ASTEROID_SPAWN_RATE_SECONDS` | 0.8 seconds | The invisible rock creator waits between new rocks. |
| `ASTEROID_MIN_VERTICES`, `ASTEROID_MAX_VERTICES`, `ASTEROID_LUMPINESS`, `ASTEROID_MAX_SPIN` | 9–14 corners, inward variation up to 30%, turning speed up to 45 degrees/second either way | Rocks generate varied outlines and spin without changing the circle used for contact checks. |
| `SCORE_LARGE`, `SCORE_MEDIUM`, `SCORE_SMALL`, `HUD_FONT_SIZE` | 20/50/100 points and font size 36 | Rocks report the score value for their size; main draws the total and other status messages. |
| `POWERUP_RADIUS`, `POWERUP_LIFETIME_SECONDS`, `POWERUP_DROP_CHANCE`, `POWERUP_DRIFT_SPEED` | Item radius 12; eight seconds before an uncollected item disappears; 15% creation chance per bullet hit; drift speed 20 pixels/second | The item file manages existence and motion, while main decides when to create one. |
| `SHIELD_DURATION_SECONDS`, `SPEED_BOOST_DURATION_SECONDS`, `SPEED_BOOST_MULTIPLIER` | Five seconds each; speed factor 1.5 | The ship stores collected-effect timers and uses the factor for engine strength and the speed limit. |
| `POWERUP_COLORS` | `shield` → cyan; `speed` → yellow | Item drawing chooses its color from the saved bonus name. |
| `BOMB_RADIUS`, `BOMB_FUSE_SECONDS`, `BOMB_BLAST_RADIUS`, `BOMB_START_COUNT` | Visible radius 8; two-second wait; damage radius 220; three bombs | Bomb drawing, its countdown, main's damage check, and the ship's supply each read the setting they need. |

Inside each weapon entry, `cooldown` means seconds to wait between firing
attempts that succeed, `speed` means bullet travel speed, `radius` means
bullet size, `angles` lists offsets from the nose direction, and `pierce`
means whether the bullet survives a hit. `WEAPONS["spread"]["angles"]`
first finds the spread dictionary, then its angle list.

**Worked example.** Spread has angles `[-15, 0, 15]`. If the ship faces
90 degrees, the three bullet directions are 75, 90, and 105 degrees.
The same shooting code processes all three list entries.

**Check your understanding.** Will changing `PLAYER_SHOOT_SPEED` make the
rapid weapon faster? **Answer:** no. The active shooting function reads
`WEAPONS[self.weapon]["speed"]`; change the rapid entry's `speed` instead.
The lesson is to follow where a setting is actually read, not just its name.

<a id="chapter-circleshape" name="chapter-circleshape"></a>

### File 2: circleshape.py — the common object foundation

**Open the source:** [circleshape.py](circleshape.py). [Back to contents](#contents).

**Its job and why it exists.** Ships, rocks, bullets, explosion dots, bombs,
and bonus items all need their own position, movement values, and size.
This blueprint supplies that setup once. Each more specific blueprint
builds on it and adds its own behavior. Reusing this foundation is called
inheritance; it does not mean all those things must look like circles.

**What it brings in.** Pygame supplies `Sprite`, group membership, and
`Vector2` pairs of horizontal/vertical numbers. `SCREEN_WIDTH` and
`SCREEN_HEIGHT` come from `constants.py` so the edge function knows where
the opposite side of the window is.

**What it stores.** `position` holds x/y coordinates; `velocity` holds
horizontal/vertical speeds; `radius` holds size. These belong to each
individual object. `containers` identifies which Pygame groups a new object
should join. Main assigns it on each specific class before creating objects.
The annotation alone does not assign a group.

**Functions in source order:**

| Function and inputs | What it does | Result and why it matters |
| --- | --- | --- |
| `__init__(self, x, y, radius)` | If groups were supplied, calls Pygame's Sprite setup with each group. Then creates an independent position, zero velocity, and radius. | Sets up this object; it does not return a separate result. `super()` reaches the blueprint being built on, and `*self.containers` passes its groups as separate arguments. |
| `draw(self, screen)` | Contains `pass`, so this version draws nothing. | Provides the function name other objects replace with their actual drawing code. |
| `update(self, dt)` | Also contains `pass`, doing nothing in this version. | Each specific object defines the changes it needs each active frame. |
| `collides_with(self, other)` | Measures center distance and compares it with both radii added together. | Returns True for touching/overlapping circles, otherwise False. The ship replaces this check with its triangle version. |
| `wrap(self, margin=None)` | Uses the supplied off-screen allowance, or this object's radius if omitted. Past each boundary, changes that coordinate to the opposite side. | Changes position in place and returns no result. The object retains its velocity. |

```text
Player / Asteroid / Shot / Particle / PowerUp / Bomb setup
                          |
                          v
                 CircleShape.__init__
                  /                 \
                 v                   v
       join the assigned groups   store this object's
       through Sprite setup       position, velocity, radius
```

This diagram shows the jobs of the shared setup, not parallel execution:
Sprite setup joins the groups first, then the position/motion/size values
are assigned. An object can belong to more than one group without being copied.

**Worked example.** Two circles centered at `(10, 10)` and `(25, 10)` are
15 pixels apart. With radii 10 and 5, their sum is 15, so `<=` returns
True: they touch exactly. A 16-pixel center distance would return False.
For wrapping, a radius-20 ship centered at x=-21 has fully passed the
left allowance; its x becomes `1280 + 20 = 1300`, just beyond the right side.

**Check your understanding.** Does `pass` automatically move an object?
**Answer:** no. It explicitly does nothing. A bullet moves because `Shot`
defines its own `update` containing `position += velocity * dt`.

<a id="chapter-shot" name="chapter-shot"></a>

### File 3: shot.py — one bullet's complete life

**Open the source:** [shot.py](shot.py). [Back to contents](#contents).

**Its job and why it exists.** This file describes a bullet after the ship
has fired it. It draws the bullet, moves it, and removes it after enough
time has passed. The ship decides when to fire and gives the bullet its
speed; main handles hits and score. Keeping those jobs separate lets every
weapon reuse the same `Shot` blueprint.

**What it brings in.** Pygame draws the circle. `CircleShape` from
`circleshape.py` supplies position, velocity, size, and group setup.
`SHOT_RADIUS`, `SHOT_LIFETIME_SECONDS`, and `LINE_WIDTH` from `constants.py`
supply a fallback size, the expiration time, and outline thickness.

**What it stores.** In addition to the shared position/velocity/radius,
each bullet stores `pierce`, a yes/no value saying whether it survives hits,
and `age`, the active seconds since creation. It does not store the score,
the ship's current position, or the whole weapon dictionary.

**Functions in source order:**

| Function and inputs | What it does | Result and connection |
| --- | --- | --- |
| `__init__(self, x, y, radius=SHOT_RADIUS, pierce=False)` | Runs shared setup, saves the hit-survival setting, and starts age at zero. | Creates a bullet in the groups assigned by main; the ship subsequently assigns its velocity. Omitted arguments use their displayed defaults. |
| `draw(self, screen)` | Draws a white circle using this bullet's position and radius. | Changes the screen image, not bullet motion. |
| `update(self, dt)` | Adds elapsed seconds to age. At 1.5 seconds or older, removes the bullet and returns; otherwise moves it by velocity times dt. | The early return prevents an expired bullet from also moving in that call. It does not wrap at screen edges. |

**Worked example.** For an existing bullet at `(100, 100)` with velocity
`(500, 0)`, an update with `dt=0.02` adds 0.02 seconds of age and ten pixels
to x, reaching `(110, 100)`, provided it has not expired. A bullet already
aged 1.49 seconds instead reaches 1.51 and is removed before movement.

**Check your understanding.** If the ship turns after firing, does the old
bullet turn too? **Answer:** no. The ship assigned that bullet its own
velocity when creating it. Neither `Shot.update` nor `Shot.draw` reads the
ship's later angle. A different behavior would need additional code.

<a id="chapter-player" name="chapter-player"></a>

### File 4: player.py — the ship, controls, and weapons

**Open the source:** [player.py](player.py). [Back to contents](#contents).

**Its job and why it exists.** This file handles behavior belonging to the
ship: its outline, engine, steering, weapons, bomb supply, and temporary
bonuses. Main coordinates encounters between objects, but it asks the ship
questions such as `is_protected()` rather than duplicating the ship's timer
rules. The three geometry functions above `Player` support its triangle
contact check; they are ordinary functions, not methods on a particular ship.

**What it brings in:**

| Imported name or group | Why this file needs it |
| --- | --- |
| `pygame` | Read held keys, construct/rotate x/y arrows, and draw the ship and shield. |
| `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `PLAYER_RADIUS`, `LINE_WIDTH` | Place a returning ship in the center and calculate/draw its outline. |
| `PLAYER_TURN_SPEED`, `PLAYER_ACCELERATION`, `PLAYER_DRAG`, `PLAYER_MAX_SPEED` | Set turning, engine strength, gradual slowdown, and the speed limit. |
| `PLAYER_RESPAWN_INVULNERABLE_SECONDS`, `SHIELD_DURATION_SECONDS`, `SPEED_BOOST_DURATION_SECONDS`, `SPEED_BOOST_MULTIPLIER` | Start protection/bonus timers and apply the speed effect. |
| `WEAPONS`, `BOMB_START_COUNT` | Look up firing settings and initialize the limited bomb supply. |
| `CircleShape` from `circleshape.py` | Reuse position/velocity/size, collection setup, and screen-edge movement. |
| `Shot` from `shot.py`, `Bomb` from `bomb.py` | Create actual bullets and bombs when the ship's functions are called. |

**What it stores.** The shared setup gives each ship `position`, `velocity`,
and `radius`. Ship setup adds `rotation`, `shoot_timer`,
`invulnerable_timer`, `shield_timer`, `speed_boost_timer`, `weapon`, and
`bombs_left`. All timers start at zero, the angle starts at zero, the weapon
name is `"single"`, and the bomb supply is three. Score and lives are not
stored here: main stores them separately. The `sounds` field remembers the
audio manager supplied by main, or None when a ship is created without audio
for a small example. It does not create a second music loop for the ship.

**Geometry helpers in source order:**

| Function and inputs | Work performed | Returned result |
| --- | --- | --- |
| `point_segment_distance(p, a, b)` | Finds the closest point to p on the finite edge from a to b; handles an edge of zero length, calculates a fraction along it, limits that fraction to 0–1, then measures distance. | A number of pixels. The caller compares it with a rock/item radius. See the [worked edge-distance example](#triangle-contact-math). |
| `side(p1, p2, p3)` | Combines coordinate differences so the result's sign identifies which side of the line through p2/p3 holds p1. | A positive, negative, or zero number; its sign matters here, not its size. |
| `point_in_triangle(p, a, b, c)` | Runs the side test against all three triangle edges and checks whether positive and negative results are mixed. | True when p is inside/on the triangle; False when outside. |

**Ship methods in source order:**

| Method and inputs | What it does and why | Result or changed values |
| --- | --- | --- |
| `__init__(self, x, y, sounds=None)` | Calls shared setup, stores the optional sound manager, then adds the ship values described above. | Initializes this ship; returns no result value. Old `Player(x, y)` examples remain valid and silent. |
| `triangle(self)` | Uses the angle to calculate a forward arrow and a sideways arrow; places the nose ahead of the center and two corners behind it. Both drawing and contact checks need these same corners. | Returns a list of three x/y positions. |
| `draw(self, screen)` | Draws the shield ring if its timer is positive, then skips the triangle during alternating respawn-protection blink intervals; otherwise draws the white triangle. | Changes the picture only. The shield alone does not cause blinking. |
| `rotate(self, dt)` | Adds turn speed times dt to the facing angle. Passing negative dt changes the turn direction. | Changes `rotation`; it does not rotate existing bullets. |
| `accelerate(self, dt)` | Chooses bonus factor 1 or 1.5, adds thrust along the nose direction, and limits velocity length to the current maximum. Negative dt applies reverse thrust. | Changes `velocity`; the position change happens later in `update`. |
| `respawn(self)` | Returns the ship to the center, stops motion, resets the angle, and starts two seconds of protection after losing a life. | Changes only position, velocity, rotation, and `invulnerable_timer`. Weapon, bombs, and other timers remain as they were. |
| `is_protected(self)` | Checks whether respawn protection OR the collected shield still has time remaining. | Returns a yes/no value that main uses before applying collision damage. |
| `apply_powerup(self, kind)` | Selects the matching timer for the text `"shield"` or `"speed"` and resets it to the configured duration. | Changes a timer; does not itself remove the collected item. Main removes the item after calling this. |
| `collides_with(self, other)` | Gets the triangle corners, checks whether the other object's center is inside, then checks its distance to every triangle edge. | Returns True if the ship touches that object's circle, otherwise False; replaces the shared circle-only check. |
| `shoot(self)` | Stops if the firing countdown is positive; otherwise looks up the selected weapon, resets the countdown, creates one bullet per angle, assigns their velocities, and requests one firing sound. | Creates `Shot` objects in the assigned groups; a spread volley makes one sound, and an attempt during cooldown makes none. |
| `drop_bomb(self)` | Stops if none remain; otherwise uses one bomb, creates a `Bomb` at the current ship coordinates, and requests its drop sound. | Reduces `bombs_left` and creates an object; an empty supply does not produce a false confirmation sound. |
| `update(self, dt)` | Reduces all four timers, reads held keys, turns/thrusts/selects/fires, applies drag, moves using velocity, then handles screen edges. | Advances this ship for one active frame. Its order explains why thrust, slowdown, and motion must be considered together. |

**Connections.** The ship can create bullets and bombs because their
blueprints are imported here. It does not need to import `main`: the
collections assigned in main make those newly created objects available
to the main loop. Conversely, main can ask the ship to draw, check contact,
or apply a bonus through the methods above.

**Worked movement example.** Suppose the ship is stationary at `(100, 100)`,
faces its initial downward direction, has no active speed bonus, and only
Up is held during an update with `dt=0.1`. Thrust adds `(0, 40)` to velocity
because `400 * 0.1 = 40`. This is below the speed limit. Drag then multiplies
by `1 - 1.0 * 0.1 = 0.9`, leaving `(0, 36)`. Motion adds `(0, 3.6)` because
`36 * 0.1 = 3.6`, so the position becomes `(100, 103.6)`. The numbers depend
on those stated conditions; a normal 60-FPS frame is much shorter than 0.1 seconds.

**Check your understanding.** Why is `player.collides_with(rock)` used
instead of `rock.collides_with(player)`? **Answer:** the name before the
dot selects whose function runs. The ship defines triangle contact logic;
a rock uses the shared circle logic. The same pair of objects can therefore
produce different results depending on which version is called.

<a id="chapter-asteroid" name="chapter-asteroid"></a>

### File 5: asteroid.py — one rock's shape, motion, and splitting

**Open the source:** [asteroid.py](asteroid.py). [Back to contents](#contents).

**Its job and why it exists.** This file describes individual rocks.
`AsteroidField` decides when and where to create one; `Asteroid` decides
its outline, spin, movement, score value, and what smaller rocks replace
it when split. Main decides when a hit deserves score or damage.

**What it brings in.** `random` varies corners, spin, and split angle;
Pygame supplies x/y arrows and outline drawing. `CircleShape` supplies
stored position/velocity/radius and circle contact checks. `spawn_explosion`
comes from `particle.py`, and `log_event` from `logger.py` records splitting.
The imported settings define line thickness, minimum/maximum rock radius,
corner counts, inward corner variation, spin limit, and the three score values.

**What it stores.** Besides shared position/velocity/radius, each rock has
`angle`, its current visible rotation; `spin`, its degrees turned per
second; and `offsets`, the list of corner locations relative to its center.
Offsets are chosen once, so the outline does not randomly change shape every
frame. A newly created rock begins at angle zero with independently chosen
spin and outline.

**Methods in source order:**

| Method and inputs | What it does | Result and why |
| --- | --- | --- |
| `__init__(self, x, y, radius)` | Runs shared setup, chooses spin and 9–14 corners, spaces their directions around 360 degrees, and varies each distance inward. | Stores this rock's outline inside its radius-based contact circle. |
| `draw(self, screen)` | Turns each stored corner offset by the current angle, adds the center position, and connects the resulting points. | Draws a white uneven outline without modifying the stored base shape. |
| `update(self, dt)` | Advances angle by spin times time, position by velocity times time, and calls wrapping with the maximum-rock allowance. | Changes this rock's motion/appearance; does not detect hits. |
| `points(self)` | Tests radius against the small and medium size cutoffs. | Returns 100, 50, or 20 for small, medium, or large; it does not add that value to main's score by itself. |
| `split(self)` | Makes explosion dots and removes the original rock; if larger than minimum, records a split and creates two smaller rocks with turned, faster velocities. | Creates replacement objects when appropriate and returns no result value. Small rocks simply disappear. |

**Worked example.** A radius-40 rock moving at `(100, 0)` splits into two
radius-20 rocks. If the random split angle happens to be 30 degrees, their
movement vectors are approximately `(103.92, 60)` and `(103.92, -60)` after
the 1.2 multiplier. Both speeds are 120 pixels/second. The original rock
is removed, but references to it can still read its center to place a bonus item.

**Check your understanding.** Why does bombing a large rock not create two
medium rocks? **Answer:** main's bomb branch calls `kill()`, not `split()`.
Having a splitting function available does not make it run automatically
whenever a rock disappears.

<a id="chapter-asteroidfield" name="chapter-asteroidfield"></a>

### File 6: asteroidfield.py — the invisible rock creator

**Open the source:** [asteroidfield.py](asteroidfield.py). [Back to contents](#contents).

**Its job and why it exists.** One invisible object handles the repeating
creation of rocks, keeping the timing and starting-edge choices out of
main's collision/drawing code. It builds directly on Pygame's `Sprite`,
not `CircleShape`, because the creator itself needs no position, radius,
contact circle, or visible outline.

**What it brings in.** `random` makes the choices, Pygame supplies Sprite
and x/y arrows, and `Asteroid` from `asteroid.py` creates actual rocks.
`from constants import *` brings in the public settings, including screen
dimensions, rock radii/kinds, and the interval. `Callable` from Python's
`collections.abc` helps describe the stored position-making functions.

**What it stores.** `Edge` names an expected pair layout: direction plus a
function that turns a fraction into a starting x/y position. The class's
`edges` list contains four such pairs. Its `containers` value is assigned
by main; `spawn_timer` belongs to the one creator object and counts active
seconds. The word **spawn** means create and add an object to the game.

**Methods in source order:**

| Method and inputs | What it does | Result and why |
| --- | --- | --- |
| `__init__(self)` | Runs Sprite setup with the assigned collection and starts `spawn_timer` at zero. | Joins the update group only; there is no drawing function for this object. |
| `spawn(self, radius, position, velocity)` | Creates `Asteroid(position.x, position.y, radius)`, then assigns its velocity. | Creates a rock in the rock/update/draw groups, using the rock's own setup; returns no separate result. |
| `update(self, dt)` | Adds elapsed time; when the timer exceeds 0.8 seconds, resets it and chooses edge, speed 40–100, angle -30–30, edge fraction, and size multiplier 1–3. Then calls `spawn`. | Creates at most one new rock per call. It does not catch up by creating many after a long frame. |

**Worked example.** If the accumulated timer is 0.79 and `dt=0.02`, it
becomes 0.81, exceeding 0.8, so one rock is created and the timer resets to
zero. If the chosen edge is left and its fraction is 0.25, the current
starting position is `(-60, 180)`: outside the left side and a quarter of
the way down a 720-pixel window. The separately selected speed/angle point
its motion generally into the window.

**Check your understanding.** Why can the timer exist without a visible
object? **Answer:** being in `updatable` causes its `update` to run; only
members of `drawable` are drawn by main's object loop. Those collections
serve separate purposes, and the creator joins only the first.

<a id="chapter-particle" name="chapter-particle"></a>

### File 7: particle.py — visible explosion dots

**Open the source:** [particle.py](particle.py). [Back to contents](#contents).

**Its job and why it exists.** A particle is one tiny dot used for a visual
effect. Many short-lived dots moving outward look like an explosion.
Both rock splitting and bomb handling can call the same creation function,
so neither needs to repeat the dot-lifetime and fading code. These dots do
not cause explosion damage; main's bomb distance check does.

**What it brings in.** `random` selects lifetimes, directions, and speeds.
Pygame supplies x/y arrows and circle drawing. `CircleShape` from
`circleshape.py` supplies independent position/velocity/radius and group
setup. This file does not import shared game settings from `constants.py`;
its defaults and dot-generation numbers are written directly here.

**What it stores.** Each dot has its shared position, velocity, and radius,
plus `lifetime`, the allowed seconds of existence, and `age`, seconds lived.
`spawn_explosion` is a separate function, not another kind of dot. Its
local `particle` name refers to the dot currently being created; groups
keep that dot available afterward.

**Functions in source order:**

| Function and inputs | What it does | Result and connection |
| --- | --- | --- |
| `Particle.__init__(self, x, y, radius, lifetime)` | Runs shared setup, saves the allowed lifetime, and starts age at zero. | Adds this dot to the update/draw groups assigned by main. |
| `Particle.update(self, dt)` | Adds to age; removes/returns if expired, otherwise moves by velocity times time. | Changes the dot or removes it; does not wrap it or check damage. |
| `Particle.draw(self, screen)` | Calculates `1 - age / lifetime`, converts it to brightness 0–255, and draws a filled gray circle. | Reduces brightness as the dot ages; equal red/green/blue values give gray rather than a colored dot. |
| `spawn_explosion(position, count=12, max_speed=150)` | Repeats dot creation count times, using radius 2, a random lifetime 0.3–0.8 seconds, a random direction around 360 degrees, and speed 30–max_speed. | Creates objects in their assigned groups; does not return a collection or apply damage. Callers can override count and maximum speed. |

**Worked example.** A dot aged 0.2 seconds with a lifetime of 0.5 has
remaining fraction `1 - 0.2 / 0.5 = 0.6`. Its brightness is `int(255 * 0.6)`
= 153, so the color is `(153, 153, 153)`. At or beyond 0.5 seconds, its
update removes it rather than continuing to draw darker values forever.

**Check your understanding.** Will increasing `max_speed` increase bomb
damage range? **Answer:** no. It makes the picture spread faster. Damage
uses `BOMB_BLAST_RADIUS` in main, not where these visual dots happen to be.

<a id="chapter-powerup" name="chapter-powerup"></a>

### File 8: powerup.py — collectible shield and speed items

**Open the source:** [powerup.py](powerup.py). [Back to contents](#contents).

**Its job and why it exists.** This file describes the item floating in the
game before collection, not the effect already active on the ship. The item
has a position, color, slow motion, and an expiration time. Main detects
when the ship touches it; `Player.apply_powerup` starts the ship's bonus.
This separation is why the item can disappear while the collected effect
continues for five seconds.

**What it brings in.** `random` chooses a drift direction. Pygame supplies
the x/y arrow and circle drawing. `CircleShape` supplies position, velocity,
radius, group setup, and opposite-edge reappearance. The settings imported
from `constants.py` supply item radius, uncollected lifetime, color lookup,
drift speed, and outline thickness. Effect-duration settings are read by
the ship file, not by this item file.

**What it stores.** Each item has `kind`, the text `"shield"` or `"speed"`,
and `age`, plus its shared position/velocity/radius. The color is looked up
when drawing rather than stored as a separate changing field. It has no
`shield_timer`: that belongs to the ship after collection.

**Methods in source order:**

| Method and inputs | What it does | Result and why |
| --- | --- | --- |
| `__init__(self, x, y, kind)` | Runs shared setup, stores the effect name, starts age at zero, and chooses a random direction multiplied by drift speed 20. | Creates a slow-moving collectible in the item/update/draw groups. |
| `update(self, dt)` | Ages the item; removes/returns at eight seconds, otherwise moves it and calls wrapping. | Limits how long an uncollected item remains and lets it drift across screen edges. |
| `draw(self, screen)` | Uses `POWERUP_COLORS[self.kind]` to draw the circular outline. | Shield is cyan and speed is yellow; an unknown kind without a color entry would cause a lookup error. |

**Worked example.** Suppose an item was created five active seconds ago
and the ship collects it now. The item's five-second age does not shorten
the effect: collecting a shield starts the ship's separate five-second
shield countdown, then main removes the item. If not collected, the item
would instead disappear once its own age reaches eight seconds.

**Check your understanding.** Does changing this item's eight-second
lifetime change shield duration? **Answer:** no. One controls the time
allowed to collect the floating item; the other controls protection after
collection. They are different settings read in different files.

<a id="chapter-bomb" name="chapter-bomb"></a>

### File 9: bomb.py — wait, flash, and signal an explosion

**Open the source:** [bomb.py](bomb.py). [Back to contents](#contents).

**Its job and why it exists.** The bomb keeps its own countdown and draws
itself. Main already has the rock collection and score, so main handles
which rocks the explosion destroys. The bomb communicates by changing the
yes/no value `detonated`; it does not need to import main or know the score.

**What it brings in.** Pygame draws the outline. `CircleShape` supplies
position/size and group setup. `BOMB_RADIUS`, `BOMB_FUSE_SECONDS`, and
`LINE_WIDTH` from `constants.py` determine visible size, waiting duration,
and outline thickness. The blast-radius setting is deliberately read by
main, where the damage calculation runs.

**What it stores.** The shared setup supplies `position`, zero `velocity`,
and radius 8. Its own fields are `fuse`, initially two seconds, and
`detonated`, initially False. Nothing in this file moves the bomb, even
though the shared foundation gives it a velocity field.

**Methods in source order:**

| Method and inputs | What it does | Result and connection |
| --- | --- | --- |
| `__init__(self, x, y)` | Runs shared setup at the supplied drop coordinates and initializes the fuse and explosion signal. | The new bomb joins the collections assigned by main; no damage happens yet. |
| `update(self, dt)` | Subtracts elapsed seconds from the fuse and sets `detonated=True` when it reaches zero or below. | Changes the signal main will read later in the same active frame. |
| `draw(self, screen)` | Converts fuse time to a changing integer, tests its remainder after division by two, and chooses red or white for the outline. | Produces flashing without needing a separate flash timer or damage logic. |

**Worked example.** If a bomb has `fuse=0.03` and an active update receives
`dt=0.05`, the fuse becomes -0.02 and `detonated` becomes True. Main then
checks nearby rocks, awards their size values, creates visual dots, and
removes the bomb. Negative fuse time is acceptable because the check uses
`<= 0`, not exact equality with zero.

**Check your understanding.** Why does the bomb stay where dropped when
the ship moves away? **Answer:** setup copies the ship's coordinates into
a separate position. The bomb's update only changes its fuse and signal;
it neither follows the ship's position nor adds velocity to its own position.

<a id="chapter-background" name="chapter-background"></a>

### File 10: background.py — the reusable image behind the action

**Open the source:** [background.py](background.py). [Back to contents](#contents).

**Its job and why it exists.** This file builds a full-window image so main
can copy it behind the action each frame. Reusing the same image avoids
randomizing stars every frame and erases the previous positions of moving
objects when the background is drawn again.

**What it brings in.** `random` chooses star positions, brightness, and
size. `Path` from Python's `pathlib` builds locations for the optional
image-loading function. Pygame creates/draws/loads/resizes images, and
`SCREEN_WIDTH`/`SCREEN_HEIGHT` from `constants.py` determine their size.

**What it stores.** There is no background class or per-frame timer. The
functions create local image values and return a finished Surface, meaning
an image-like grid of pixels. Main stores the returned image in its own
`background` variable and reuses it.

**Functions in source order:**

| Function and inputs | What it does | Returned result and requirements |
| --- | --- | --- |
| `make_starfield(star_count=150)` | Creates a window-sized black Surface, then chooses x/y, brightness 80–255, and radius from `(1, 1, 2)` for each star and draws it. | Returns the finished star image. The repeated 1 makes radius-one stars twice as likely as radius-two stars. Main calls this once. |
| `load_background(filename="background.png")` | Builds a path from this Python file's directory through `assets` to the filename, loads the image, converts it to the display format, and resizes it. | Returns the resized image; the file must exist and the display must already be opened before `.convert()`. Main currently does not call this alternative. |

`__file__` refers to this source file's location. `Path(__file__).parent`
means its containing folder. The `/` operator joins path parts for a
`Path`; it is not dividing numbers in that expression.

**Worked example.** If a star's chosen brightness is 120, `(shade,) * 3`
builds `(120, 120, 120)`: equal red, green, and blue gives gray. With
`make_starfield(10)`, the loop draws ten stars instead of the default 150.
Those dots still form a single returned background image.

**Check your understanding.** Why not call `make_starfield()` inside the
drawing loop? **Answer:** that would create a new image and new random star
positions every frame, repeating setup work and making the star pattern
change continually. Main only needs to copy the already-finished image.

<a id="chapter-controls" name="chapter-controls"></a>

### File 11: controls.py — the instructions the player sees

**Open the source:** [controls.py](controls.py). [Back to contents](#contents).

**Its job and why it exists.** This file draws one reusable instruction
panel for the start and paused-help screens, plus a separate final-score
panel after game over. Reusing the instruction panel keeps those two
screens' key descriptions consistent. Main controls timing, input, and
round reset; this file controls the pictures.

**What it brings in.** Only Pygame. It needs Surfaces for image layers,
Rects for positioning, and rectangle drawing. The window and already-created
fonts are arguments passed by main, so this file does not need to import
main or construct another window.

**What it stores.** `CONTROLS` is a tuple of ten pairs of displayed strings.
Each pair says what to print in the key column and the action column. These
are instructions for a person, not actual keyboard bindings. The local
`shade`, `panel`, `rendered`, row `index`, `key`, `action`, and `y` values
exist while drawing; they are not saved game progress.

**Functions in source order:**

| Function and inputs | What it does | Result and why |
| --- | --- | --- |
| `draw_controls(screen, title_font, text_font, paused=False)` | Makes a partly see-through black layer, draws the centered panel and border, selects the heading, draws each key/action row and the explanatory messages. | Changes the supplied screen image and returns no result. `paused` selects wording; it does not stop updates by itself. |
| Inner `centered(text, font, y, color="white")` | Renders the supplied message to a small image, gets a rectangle centered at the panel's middle and height y, then copies the image to screen. | A local drawing helper used only during the outer call. It avoids repeating the same centering calculation for each message. |
| `draw_game_over(screen, title_font, text_font, score)` | Darkens the frozen scene and draws a centered GAME OVER panel with the supplied score and Enter/Esc instructions. | Draws the result but does not remove old objects or start another round; main performs those actions after the appropriate input. |

The inner helper is defined after the panel is created and before it is
called. It can read that outer call's `screen` and `panel`, so those do not
have to be passed again in every centered-message call. Defining the helper
does not draw anything until a later `centered(...)` call runs its body.

**Worked example.** A 900-by-600 panel centered in a 1280-by-720 window
starts at x=190 and y=60: `(1280 - 900) / 2` and `(720 - 600) / 2`.
For row index 2, the formula `panel.top + 150 + index * 30` gives y=270.
The key text goes at x=230, while the action text goes at x=465.
These are positions within this fixed layout, not automatically responsive columns.

**Check your understanding.** If you change the displayed Space label to
F, will F fire? **Answer:** no. Firing is checked in `Player.update`.
Instruction text and actual key checks must both be updated when a binding
changes. Likewise, main must skip updates to pause; drawing PAUSED alone
would not freeze any object.

<a id="chapter-logger" name="chapter-logger"></a>

### File 12: logger.py — records of what the game did

**Open the source:** [logger.py](logger.py). [Back to contents](#contents).

**Its job and why it exists.** This file writes machine-readable records
that let someone inspect positions and actions after they happen. It
does not move objects or provide a save/load system. The course-oriented
output is separate from the status messages drawn on screen.

**What it brings in:**

| Python tool | Why it is used here |
| --- | --- |
| `inspect` | Find the function that called the state logger and inspect its local variables, so main need not pass every collection separately. |
| `json` | Convert dictionaries to structured text before writing them. JSON Lines stores one such record per line. |
| `math` | Round elapsed real-world seconds down with `floor`. |
| `datetime` from `datetime` | Obtain the initial time and each entry's time. |
| `NotRequired`, `TypedDict` from `typing` | Describe the possible fields in saved dictionaries for readers and type-checking tools. These do not create visible game objects. |

**Definitions and stored values, in source order:**

| Name | Meaning and reason |
| --- | --- |
| `SpriteInfo` | A dictionary layout: `type` is the object's class name; optional `pos`, `vel`, `rad`, and `rot` mean position, velocity, radius, and facing angle. Not every kind of object has every field. |
| `GroupInfo` | A dictionary layout containing the total `count` and a `sprites` list of sampled object details. The count can be larger than the sample. |
| `__all__` | Names exposed by `from logger import *`; main instead names its two requested functions explicitly. |
| `_FPS`, `_MAX_SECONDS`, `_SPRITE_SAMPLE_LIMIT` | Values 60, 16, and 10: count-based snapshot interval, approximate active-frame recording duration, and maximum sampled members per group. |
| `_frame_count` | Counts active state-logger calls until its limit. It is not a counter that keeps running forever. |
| `_state_log_initialized`, `_event_log_initialized` | Remember whether each output has had its first write during this run, so later writes append rather than replace. |
| `_start_time` | Clock time when this module first loads, used for elapsed seconds; it is not the moment Enter starts play. |

**Functions in source order:**

| Function and inputs | What it does | Result and connection |
| --- | --- | --- |
| `log_state()` | Stops after its count limit; otherwise counts the call, samples every 60th call, finds the caller's variables, captures group counts/member details and dimensions, adds timing, and writes a JSON line. | Returns no game value. Main calls it before active updates, so saved state describes that point in the frame. |
| `log_event(event_type, **details)` | Receives an action name and optional additional named details, combines them with clock time and current frame-counter value, and writes a JSON line. | Returns no value. Main records ship/bullet hits, while `Asteroid.split` records qualifying rock splits. |

The `global` statements let those functions update the flags/counter
defined outside them, preserving progress between calls. The single leading
underscore marks names intended for internal use; it does not enforce privacy.

In `log_state`, `frame.f_back` reaches the caller's execution record and
`f_locals.copy()` reads a copy of its name/value mapping. The loop recognizes
groups by class names containing `Group`, and uses `hasattr` before reading
optional object values. `round(value, 2)` limits saved coordinate digits.
For each group, the total comes from `len(group)` even if only ten members
are described. A fallback permits an individual positioned object when no
state has yet been captured. The record dictionaries, rather than the
original objects, are turned into text.

`with open(...)` ensures a file is closed after writing. Mode `"w"` replaces
the old file on the first actual write; `"a"` adds later lines. `**game_state`
and `**details` copy named dictionary entries into the final record, while
`"\n"` ends its line. See [the longer logging explanation](#course-logging)
for clock-versus-frame counting and the possibility of an old log remaining
when a run never produces its first write.

**Worked example.** At active call 60, the first state line is written.
If a bullet group contains 23 members, its record says `count: 23` but
includes details for at most ten. There are sixteen state snapshots at
counts 60 through 960. The counter then stops at 961; later events can
still be written using that counter value, with later clock times.

**Check your understanding.** Does `elapsed_s=20` mean a newly collected
shield has expired? **Answer:** not by itself. That number measures time
since the logger loaded, including menus. The shield has its own timer,
started on collection and reduced only by active ship updates.

<a id="chapter-main" name="chapter-main"></a>

### File 13: main.py — the coordinator that runs the game

**Open the source:** [main.py](main.py). [Back to contents](#contents).

**Its job and why it exists.** Main connects objects that intentionally do
not know about each other's collections or the overall score. A bullet
knows how to move; main knows which rocks to test it against. A bomb knows
when its countdown finishes; main knows which rocks to destroy. This keeps
the object files smaller while giving the whole game one explicit order.

**What it brings in:**

| Imported names | What main needs them for |
| --- | --- |
| `random`, `pygame` | Decide whether to create bonus items and use window/input/time/font/group/audio tools. Losing the last life now opens a panel rather than exiting through sys. |
| `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `PLAYER_LIVES`, `HUD_FONT_SIZE`, `POWERUP_DROP_CHANCE`, `BOMB_BLAST_RADIUS` | Configure window/setup values and the cross-object rules main applies. |
| `log_state`, `log_event` from `logger.py` | Record occasional state and named hits. |
| `Player`, `Asteroid`, `AsteroidField`, `Shot`, `Particle`, `PowerUp`, `Bomb` from their respective files | Assign each blueprint's groups and create the initial ship/creator; main also creates random bonus items. Individual bullets, fragments, and bombs are created by their relevant object functions. |
| `spawn_explosion` from `particle.py` | Make visible effects for bomb damage. Rock splitting calls the same helper from the rock file. |
| `make_starfield` from `background.py`, `draw_controls`, `draw_game_over` from `controls.py` | Prepare the background and draw the correct instructions or final-score panel. |
| `SoundEffects` from `sounds.py` | Build the music/effects manager once, use it for audio controls and main-handled events, and pass it to the ship for firing/drop sounds. |

**What it stores.** `clock` measures/limits frame time, `dt` is elapsed
seconds, `screen` is where drawing happens, `background` is the star image,
and `font`, `title_font`, and `help_font` describe lettering. `sounds` refers
to the shared audio manager, which owns mute, volume, cached audio, and
playback channels. Six groups
organize the objects: `updatable`, `drawable`, `asteroids`, `shots`,
`powerups`, and `bombs`. `player` and `asteroid_field` refer to the two
objects for the current round. `score`, `lives`, `started`, `showing_help`, and `game_over` describe
overall progress and menu state. Temporary names inside loops refer to the
object or message currently being processed, not separate saved game systems.

**Functions and execution in source order.** `reset_game(updatable, sounds)`
comes first. It loops through the old update-group members and calls
`kill()` on each, removing them from every group they joined. It then
creates a centered `Player` using the existing sound manager and a new
`AsteroidField` with a fresh creation timer, returning both references.
Using only `updatable.empty()` would be insufficient: it would leave the
old objects in their drawing and interaction groups. Every game object in
this project's setup joins `updatable`, so killing its members clears the world.

`main()`, which has no arguments, creates the window/audio once and uses
that reset function for the first round and each Enter restart. Score,
lives, and menu flags belong to main, so it resets those separately.
Its body performs these phases:

| Phase inside `main()` | Work performed | Why this position in the code matters |
| --- | --- | --- |
| Print and initialize | Report Pygame/version/window settings, initialize Pygame, create clock/window/title. | Display and font work must have their required systems ready. |
| Prepare drawing resources | Create the star image and fonts. | These are reused instead of repeatedly recreated during gameplay. |
| Create collections and assign `containers` | Make empty groups, then tell each class which ones its new objects join. | Assignment must precede the initial ship/creator and later object creation. |
| Create initial objects and overall values | Call reset_game for ship/creator and initialize score, lives, and menu flags. | The same reset helper is reused after game over; ordinary frames do not recreate the ship. |
| Start the repeating loop and read events | Accept close, Esc, Enter, H, B, M, and volume keys under their stated conditions. | Menu/quit/audio controls still work while paused; B calls the ship only during active play. |
| Handle start/help/game-over screen | Draw the appropriate panel, present it, cap redraw speed, set dt to zero, and continue. | Skipping everything below this branch freezes movement and timers; Enter after game over resets the round before resuming. |
| Log and update | Save occasional state, then call `updatable.update(dt)`. | Object positions and countdowns change before main uses them for this frame's interactions. |
| Apply bomb explosions | For each detonated bomb, score/remove overlapping rocks and create visual effects, then remove the bomb. | Those removed rocks do not appear in the later fresh rock-contact pass. |
| Collect bonus items | Check ship triangle against item circles, apply the matching ship timer, then remove each collected item. | A collected shield can protect the ship during the later rock checks in this frame. |
| Handle rock/ship and rock/bullet contact | For each rock, first handle an unprotected ship hit; otherwise check bullets. Update lives, score, fragments, event records, and bonus-item creation as appropriate. | `continue` skips bullet checks for a rock that hit the ship; `break` stops further bullet hits against a rock already destroyed. |
| Draw the completed scene | Copy background, draw visible objects, render status text and help hint, then present the display. | Later pictures cover earlier ones, keeping text in front and erasing old positions. |
| Measure and cap time | `clock.tick(60) / 1000` waits if necessary and converts elapsed milliseconds to seconds for the next update. | Motion/timers use elapsed seconds, rather than moving a fixed amount per loop pass. |

After the function definitions, the `if __name__ == "__main__"` guard calls
main only when this file is launched directly. A window-close or Esc request
returns out of main. Losing the final life keeps the program running on the
score panel, allowing the damage sound to finish without a blocking wait.
Enter creates a fresh round while keeping the same audio manager and window.

```text
events read -> start/help/game over? -> yes -> draw panel -> next loop pass
                         |
                         no
                         v
log -> update objects -> bombs -> collect bonuses -> check rocks/ship/bullets
                                                          |
                                                          v
                                 next pass <- measure time <- draw scene
```

This diagram shows the main loop's phases, not calls from every method.
The cross-file action journeys immediately after these chapters fill in
what occurs inside those phases.

**Worked example.** Suppose score is 100 and a detonated bomb overlaps one
large rock and one small rock, with no other hits in that pass. Their point
values are 20 and 100, so main changes score to 220 and removes both without
splitting. The individual rock functions return values, but the addition
to the overall score occurs here.

**Check your understanding.** Why can't `Bomb.draw()` freeze the game just
by drawing a paused message? **Answer:** drawing changes pixels, not which
instructions execute. Main must take the help branch and skip updates and
interactions to freeze gameplay. The same distinction separates a picture
of an explosion from the distance calculation that actually applies damage.

<a id="chapter-sounds" name="chapter-sounds"></a>

### File 14: sounds.py — original arcade music and action effects

**Open the source:** [sounds.py](sounds.py). [Back to contents](#contents).

**Its job and why it exists.** This file creates sounds mathematically,
loads them into Pygame once, and plays them when another part of the game
requests a named event. It also creates an original eight-second background
loop using a bright melody, lower bass notes, and simple drum-like sounds.
There are no downloaded tracks or separate sound assets to find or install.
Keeping generation and playback here prevents the ship and main loop from
having to calculate thousands of audio samples while processing a hit.

**What it brings in:**

| Tool | Purpose |
| --- | --- |
| `io` | Make an in-memory file so a valid WAV recording can be loaded without writing it to disk. |
| `math` | Calculate sine waves, pitch changes, and fading curves. A wave's frequency is the number of repetitions per second; higher frequency sounds higher. |
| `random` | Supply repeatable noise for impacts/percussion. Each generator has its own seed and does not consume the random choices used for rocks or bonus items. |
| `struct` | Encode each calculated amplitude as the two bytes used for a signed 16-bit audio sample. |
| `wave` | Write a WAV header describing sample rate, channel count, and sample size, followed by the encoded samples. |
| `pygame` | Load the WAV data as Sound objects and play them on the audio mixer. |

**What it stores.** `EFFECTS` maps ten event names to recipes containing
duration, starting pitch, ending pitch, and noise amount. `SoundEffects`
stores `enabled`, `muted`, `volume`, cached `effects`, the generated `music`,
and dedicated `shot_channel` and `music_channel` playback objects. The
default master setting is 0.5, or 50%; music receives another factor of
0.35 so it stays behind the action. These are session settings, not saved
preferences that persist after closing the game.

**Functions in source order:**

| Function and inputs | Work performed | Result and connection |
| --- | --- | --- |
| `make_sound(duration, start_pitch, end_pitch, noise)` | Generates amplitude samples at 44,100 per second, slides the pitch, mixes the requested fraction of noise, fades the edges, and writes a mono WAV into memory. | Returns one Pygame Sound. The mixer converts the source recording to the playback format if needed. |
| `make_music()` | Generates eight seconds at 22,050 samples per second. Each 0.125-second step selects a melody note/rest; four two-second bars use A minor, F major, G major, and E major chords. Low sine-wave bass and short noise/thump percussion accompany the pulse-wave melody. | Returns the original loop as one cached Pygame Sound; playback repeats the recording rather than recomposing every frame. |
| `SoundEffects.__init__(self)` | Checks whether the mixer initialized, allocates sixteen channels, reserves zero for weapons and one for music, creates the effects/music, sets volumes, and starts looping music. | With no device, reports silent mode and returns. A Pygame audio setup/conversion error also disables audio instead of closing the game. |
| `play(self, name)` | Returns immediately if audio is unavailable or muted; otherwise finds the requested effect. `shoot_` events use the weapon channel; other effects use a free unreserved channel. | Starts playback without waiting. A new shot can replace an old shot on that channel, while music has its own reserved channel. |
| `toggle_mute(self)` | Reverses the mute setting. On mute, stops current playback. On unmute, restarts the music loop. | Old shots and impacts are not replayed; later successful actions can request new effects. |
| `change_volume(self, amount)` | Adds the adjustment, rounds it, and limits it to 0–1. Applies it to all effects and the quieter music. | Changing volume while muted remembers the level but leaves mute active. |
| `status_text(self)` | Builds the sound-percentage/mute/key label, or reports an unavailable device. | Returns text that main renders on both instruction screens and during play. It does not draw the label itself. |

A **sample** is one measurement of a sound wave's amplitude at an instant.
In an effect, `index / rate` converts its sample number to seconds. A sine
wave supplies a smooth tone, while random amplitudes supply rough noise.
The changing phase in `make_sound` produces the rising or falling pitch.
Its envelope is a multiplier that brings the volume in gently and then
reduces it toward the end, avoiding an abrupt full-amplitude start/stop.

`struct.pack("<h", value)` encodes a sample as a two-byte signed integer
with the byte order required here. `wave` adds the recording description,
and `buffer.seek(0)` returns to the beginning so Pygame reads that header
before the samples. The separate `random.Random(...)` objects make audio
generation repeatable without changing the gameplay's random sequence.

Music uses a different recipe: short pulse-wave notes for a retro melody,
smoother low bass, a rapidly fading kick-like tone, and quiet noise ticks.
`None` entries leave melody rests while the rhythm continues. At four
steps per half-second beat, the loop has a 120-beats-per-minute pulse.
The beginning/end fade softens the join when the cached recording repeats.
It evokes old electronic arcade music without copying a game's melody.

**Where audio requests happen:**

| Event | Code requesting playback | Why it is requested there |
| --- | --- | --- |
| Successful weapon volley | `Player.shoot` after making all its bullets | One sound per accepted firing action, rather than per spread bullet or per held-key frame. |
| Successful bomb drop | `Player.drop_bomb` after creating it | An empty bomb supply returns before playing confirmation. |
| Bullet destroys a rock | Main's bullet-hit branch | That branch knows an actual hit occurred; simply drawing a nearby bullet should make no impact sound. |
| Bomb explosion | Main's detonated-bomb branch | One blast per bomb, even if many rocks are destroyed. |
| Ship loses a life | Main's unprotected ship-hit branch | Protected contact makes no false damage warning. The final hit can finish while the final-score panel is open, without delaying the event loop. |
| Collected shield/speed item | Main's item-contact branch | The saved item kind selects the corresponding rising tone only when collected. |
| Music | Sound-manager setup and leaving mute | Playback is not tied to sprite updates, so it continues during menu/help screens. |

**Worked example.** At master volume 0.5, each action effect's playback
setting is 0.5 and music's is `0.5 * 0.35 = 0.175`. These multiply already
restrained generated sample amplitudes; 50% is a software setting, not a
measurement of speaker loudness. Pressing minus changes master to 0.4 and
music to 0.14. Pressing M stops both, keeping 0.4 remembered. Pressing plus
while muted changes the remembered setting to 0.5 but stays silent until M
is pressed again.

**Check your understanding.** Why do sounds continue while sprites are
paused? **Answer:** Pygame's mixer plays its channels independently after
being asked to start. The help branch skips sprite updates, but does not
stop the music channel. Main still reads M and volume events before that
branch, so the player can silence or adjust it while reading.

If no audio device opens, the HUD says `Sound: unavailable` and game actions
continue silently. Available effect channels are finite: when every
unreserved channel is busy, another non-weapon effect may not play. Weapon
and music slots remain reserved. No audio setting or effect changes collision
geometry, score values, or how many bombs the ship has.

In this WSL Ubuntu environment, playback initially failed because the native
`libpulse0` library was missing, even though WSLg's audio server existed.
Installing that library restored audio. The game needs no additional Python
audio package, but the operating system still needs a usable audio device and
its client libraries. Silent fallback keeps play available if those are absent.

<a id="value-ownership" name="value-ownership"></a>

### Who stores and changes each important value?

An object's functions can change its fields; main also directly assigns some
starting velocities during creation. This table identifies the current code's
usual writer and reader, so you can follow a value instead of guessing from
its name. These are not copies kept automatically in sync across files.

| Value | Where it lives | Who changes it | Who reads it and why |
| --- | --- | --- | --- |
| Shared settings | Names in `constants.py` | Defined at module load; edited between runs when tuning | Importing files read the settings they use. Capital letters express intent, not enforced immutability. |
| `score`, `lives` | Local variables in `main()` | Main's hit/explosion code | Main draws them; zero lives ends the game. The ship does not hold a second lives value. |
| `started`, `showing_help`, `game_over`, `dt` | Local variables in `main()` | Main's event/menu/timing code | Main chooses the start/help/game-over/live branch, resets finished rounds, and passes dt to updates. |
| `containers` | Assigned on object classes in main | Main during setup | New-object setup reads it to join groups. It is not a bag of copied objects. |
| `position`, `velocity`, `radius` | Each object's own stored values | Shared setup creates them; relevant motion/creation methods change them | Drawing/contact/movement functions read them; each object has its own position. |
| Ship `rotation`, `weapon`, `bombs_left` | The Player instance | Ship turning/key/drop methods and setup; respawn resets rotation only | Ship geometry, firing, bomb checks, and main's status text read them. |
| Ship's four countdowns | The Player instance | Setup/collection/respawn/shooting start them; `Player.update` subtracts elapsed time | Shooting, protection checks, speed calculation, and drawing use them. |
| Rock `angle`, `spin`, `offsets` | Each Asteroid instance | Setup chooses spin/shape; update changes angle | Drawing rotates the stored offsets; circular contact checks do not use that outline list. |
| Creator `spawn_timer` | The AsteroidField instance | Its update adds time and resets it when creating a rock | The same update checks when another rock is due. |
| Bullet `age`, `pierce` | Each Shot instance | Setup saves pierce; update increments age | Bullet update removes expired shots; main decides whether a hit removes a piercing bullet. |
| Item `kind`, `age` | Each PowerUp instance | Setup saves the kind; update increments age | Item drawing picks color; main passes kind to the ship; age determines uncollected expiration. |
| Bomb `fuse`, `detonated` | Each Bomb instance | Bomb update counts down and sets the signal | Main reads the signal to apply damage; bomb drawing reads the fuse for flashing. |
| Dot `age`, `lifetime` | Each Particle instance | Setup saves lifetime; update increments age | Update removes expired dots; drawing calculates fading. |
| Logging counters, flags, start time | Module-level names in `logger.py` | Import-time assignments and logging functions | Logging decides whether to sample, append/replace output, and record timing. |
| Audio `volume`, `muted`, cached effects/music | One `SoundEffects` manager created by main | Audio key events call its adjustment methods; setup generates recordings once | Main displays status; ship/main request events; the mixer independently plays the cached audio, including while help pauses sprite updates. |

<a id="code-origins" name="code-origins"></a>

### Is this Python, Pygame, or something this project defines?

| Example | Where it comes from | What to understand about it |
| --- | --- | --- |
| `if`, `for`, `def`, `class`, `return`, `and`, `not` | Python language | These words control how the instructions are organized and run. |
| `len`, `range`, `int`, `max`, `min`, `hasattr`, `super` | Python's built-in tools | Available without importing a project file; they count, convert, limit, inspect names, or reach setup/functions from a class being built on. |
| `self` | A conventional Python parameter name | Refers to the object passed to an instance method; it is not an imported Pygame tool or a specially declared ship variable. |
| `random`, `json`, `math`, `datetime`, `inspect`, `Path` | Python's standard library | Included with Python but brought in through imports to provide specific tools. |
| `pygame.Vector2`, `Surface`, `Rect`, `sprite.Group`, `sprite.Sprite` | The installed Pygame package | Pygame's implementations of two-number arrows, images, rectangle layouts, object collections, and group-compatible objects. |
| `pygame.K_LEFT`, `KEYDOWN`, `QUIT` | Pygame's named constants | Names for keys and event types; the project decides what to do when it sees them. |
| `Player`, `CircleShape`, `Shot`, `AsteroidField` | This project's Python files | Blueprints defined by this game, using Python and Pygame to implement its particular behavior. |
| `shoot`, `drop_bomb`, `apply_powerup`, `spawn_explosion` | This project's definitions | Their names are chosen here. Their bodies determine what happens; Python has no built-in rule saying a function called shoot must create bullets. |
| `PLAYER_MAX_SPEED`, `WEAPONS` | This project's `constants.py` | Chosen settings, not Pygame's built-in limits. |
| `SoundEffects`, `make_sound`, `make_music` | This project's `sounds.py` | Our sound manager and synthesis functions; they use Python to build recordings and Pygame to play them. |

For a name you do not recognize, first look at the imports and definitions
in that file. Follow a local import into its source file. A dot often helps:
`pygame.draw.circle` points into the package, while `player.shoot` runs a
function on this game's ship object.

<a id="action-walkthroughs" name="action-walkthroughs"></a>

## 13. Follow an action through the files

An import tells you where a name comes from. A call tells you when its code
actually runs. These examples follow real calls across the project so the
connections are visible.

### 13.1 Holding Space: from keyboard to visible bullet

```text
main.py: updatable.update(dt)
  -> player.py: Player.update(dt)
      -> read held keys
      -> self.shoot()
          -> choose WEAPONS[self.weapon] from constants.py
          -> shot.py: Shot(...) creates a bullet
              -> circleshape.py: store position/size and join groups
          -> set the new bullet's velocity
  -> main.py: later contact and drawing loops can see that bullet
```

The steps in detail:

1. `updatable.update(dt)` calls the ship's update along with the other
   members' updates. It does not require `main.py` to know which keys
   control the ship.
2. `Player.update` reduces the firing countdown and asks Pygame which keys
   are held. If Space is held, it calls this ship's `shoot()` method.
3. `shoot()` returns immediately if positive waiting time remains. Holding
   Space therefore keeps requesting shots without bypassing the weapon's delay.
4. When ready, it finds the selected name in `WEAPONS`. With `"spread"`
   selected, the angle list is `[-15, 0, 15]`, so the next loop makes three
   separate bullets. It also resets the firing countdown to 0.5 seconds.
5. Each `Shot(...)` receives the ship's x/y coordinates, bullet radius,
   and whether it survives hits. The bullet's setup calls `CircleShape`'s
   setup, which creates its own position and adds it to `shots`, `updatable`,
   and `drawable` through the previously assigned `Shot.containers`.
6. The ship sets each new bullet's velocity using its facing angle plus
   the bullet's angle offset. The position is an independent x/y pair:
   moving the ship afterward does not drag an already-fired bullet along.
7. The later loops in `main.py` can check and draw the bullets in this frame.
   Their own age/movement updates start in a subsequent update pass, because
   they were added after the current update pass's member list was captured.

**The connection:** `player.py` decides when and how to fire; `shot.py`
defines a bullet's lifetime, motion, and drawing; `circleshape.py` provides
its basic stored values and joins its collections; `main.py` checks hits
and draws it. None of those jobs alone creates the whole firing behavior.

### 13.2 A bullet hits a medium rock

Assume an ordinary, non-piercing bullet overlaps a radius-40 rock when
`main.py` reaches the bullet contact checks.

1. `asteroid.collides_with(shot)` uses `CircleShape`'s circle check: the
   distance between centers must be no larger than rock radius plus bullet radius.
2. `main.py` records `"asteroid_shot"` using `logger.log_event`.
3. `asteroid.points()` in `asteroid.py` returns 50, and `main.py` adds it
   to the game's score. The rock returns the value; it does not own or
   directly change the game's score variable.
4. `asteroid.split()` creates explosion dots by calling
   `particle.spawn_explosion`, then removes the original rock from its groups.
5. Radius 40 is larger than the minimum 20, so `split()` records
   `"asteroid_split"` and creates two radius-20 rocks at the old center.
   They receive directions turned to opposite sides of the original motion
   and speeds multiplied by 1.2. Each gets its own randomly generated outline.
6. Back in `main.py`, a random check may create a shield/speed item at the
   old rock's position. The removed rock object still has readable position
   values even though `kill()` removed it from the groups.
7. Since the ordinary bullet has `pierce=False`, `shot.kill()` removes it.
   The `break` then leaves the bullet loop for the original rock, avoiding
   another hit against that same already-destroyed object.
8. The smaller rocks and effect dots belong to drawing collections, so the
   later drawing pass can display them. The smaller rocks are not added
   retroactively to the already-running outer rock loop.

A new bonus item created here also is not collected until a later frame:
the bonus-collection loop for this frame already ran before bullet hits.
The order in `main.py` explains that behavior.

### 13.3 Touching a shield item

1. A `PowerUp` object exists with `kind = "shield"`. Its drawing uses
   `POWERUP_COLORS` to make the item cyan; it does not grant protection
   merely because it exists or is nearby.
2. During active play, `main.py` loops through `powerups`. That means
   **"check each shield or speed item the ship could collect."** The
   singular name `powerup` refers to the current item in that loop.
3. `player.collides_with(powerup)` checks the ship's triangle against the
   item's circle. Putting `player` before the dot selects the ship's
   version of the contact-checking function.
4. On contact, `player.apply_powerup(powerup.kind)` passes the text
   `"shield"` to the ship, which sets `shield_timer` to five seconds.
5. `main.py` removes the item, so it cannot grant the bonus again.
6. The rock-contact loop runs afterward. `player.is_protected()` now returns
   True, so a rock cannot remove a life during those checks.
7. On later updates, `shield_timer -= dt` counts down. While positive,
   `Player.draw` shows a cyan ring. This shield does not make the triangle
   blink; blinking comes from the separate respawn-protection timer.

Speed-item collection takes the same route but sets `speed_boost_timer`.
The timer is read inside `accelerate()`, increasing engine strength and the
speed limit when thrust is applied. It does not instantly multiply the
ship's existing velocity at the moment of collection.

### 13.4 Pressing B: from dropped bomb to rock damage

1. The event loop in `main.py` sees a B key press. It accepts it only when
   the game has started and help is closed, then calls `player.drop_bomb()`.
2. `Player.drop_bomb()` checks the remaining supply. If none remain, it
   returns. Otherwise it subtracts one and creates a `Bomb` at the ship's x/y.
3. The bomb joins the bomb, update, and drawing groups. It stays at the
   drop location; it neither follows the ship nor receives the ship's velocity.
4. Each active update subtracts `dt` from the bomb's two-second fuse.
   Its drawing alternates red/white while it waits.
5. At zero or below, `Bomb.update()` sets `detonated = True`. It does not
   reach into `main()` to search rocks or change the score.
6. The bomb-handling loop in `main.py` sees that True value. For each rock,
   it checks center distance against `BOMB_BLAST_RADIUS + asteroid.radius`.
   For example, a radius-60 rock centered 270 pixels from the bomb overlaps
   a 220-pixel blast because 270 is less than 220 + 60.
7. Qualifying rocks award their current-size points and are removed with
   `kill()`, without splitting and without the bullet branch's bonus-item roll.
8. `spawn_explosion()` creates the visible dots for destroyed rocks and the
   bomb. The bomb is removed so the same explosion is not applied again.

The explosion dots are the picture of the blast, not the thing that causes
damage. The distance check in `main.py` applies damage even though the dots
have no collision role.

### 13.5 Losing a life, and what actually resets

`main.py` checks each rock against the ship before checking bullets against
that rock. If the ship is unprotected and touches it, it records
`"player_hit"`, subtracts one life, and splits the rock. This branch does
not add score or create a random collectible item.

If lives reach zero, the terminal prints `Game over!` and the final-score
panel opens. The ship is removed, the current rock-checking loop stops, and
gameplay stays frozen. Enter creates a new round; Esc closes the program.
If a life remains, `Player.respawn()` resets only these values:

| Value | After `respawn()` |
| --- | --- |
| Position | Window center |
| Velocity | `(0, 0)`, meaning stationary |
| Facing angle | Zero, which points down in this triangle formula |
| Respawn-protection countdown | Two seconds |

It does not reset the score, selected weapon, remaining bombs, shield timer,
or speed-bonus timer. Existing rocks and bullets remain in the game.
Those results follow from which assignments are actually present in
`respawn()`, not from what other Asteroids games might do. This partial reset
after losing one life differs from `reset_game()` after losing the entire
round: restarting removes the old world and creates a brand-new ship,
restoring weapon, bombs, and bonus timers too. Main also resets score/lives.
Audio preferences and the running music manager are kept across rounds.

### 13.6 Opening help and resuming

After starting, pressing H reverses `showing_help`. If it becomes True,
the instruction branch redraws the background and frozen objects and then
calls `draw_controls(..., paused=True)`. `continue` skips the gameplay code
below it. No object update means no movement, bomb countdown, bonus aging,
shield expiration, or new-rock timer progress.

Window-close and Esc events still work because events are read before the
pause branch. Enter or H closes help. The paused frames kept `dt` at zero,
so the first resumed update does not include all the seconds spent reading.
Held movement/fire keys can be read again as soon as play resumes; pausing
does not require the user to release and repress them.

<a id="course-logging" name="course-logging"></a>

## 14. How the course logger works

[logger.py](logger.py) writes two kinds of text records. JSON is a text
format representing named values and lists; JSON Lines (`.jsonl`) stores
one complete record on each line. These files are diagnostic output, not
saved games that `main.py` can load to resume play.

| Function | Called from | Output | What it records |
| --- | --- | --- | --- |
| `log_state()` | `main()` before active updates | `game_state.jsonl` | Occasional records of positions, movement values, group counts, and timing |
| `log_event(name)` | `main()` and `Asteroid.split()` | `game_events.jsonl` | Actions named `player_hit`, `asteroid_shot`, and `asteroid_split`, with timing information |

### 14.1 Why `log_state()` takes no game arguments

The logger uses Python's `inspect` tools to look at the function that called
it. An **execution frame** is Python's record of a running function and its
variables. `inspect.currentframe()` obtains the logger's frame;
`frame.f_back` obtains the calling frame, normally `main()`. Reading
`frame_back.f_locals.copy()` copies the caller's variable-name/value pairs.

The logger looks through those values for Pygame drawing surfaces and
collections whose class names contain `Group`. For each group it saves the
full count and details for at most ten members. An individual object's
position, velocity, radius, or facing angle is included only if it has that
attribute. A fallback also permits recording an individual positioned object
when no game state has yet been captured.

`SpriteInfo` and `GroupInfo` use `TypedDict` to describe the expected field
names and kinds of values for readers and type-checking tools. They do not
create on-screen objects or automatically enforce the dictionary's contents.
`NotRequired` marks details that can be absent, such as rotation on an object
that has no `rotation` value. The actual dictionaries are built inside the
logging function.

### 14.2 Frame counting and clock time are different

Before its limit, `log_state()` counts active calls and writes only every
60th call. It records frames 60, 120, and so on through 960: sixteen
snapshots. This represents about sixteen seconds only when active play
stays near 60 frames per second. The counter subsequently stops advancing;
event logging can still continue with that stopped counter value.

`elapsed_s` instead uses the actual clock time since `logger.py` was first
loaded. Reading the start screen or paused help does not advance gameplay
timers, but it still advances this clock-based number. Also, because the
state call comes before `updatable.update(dt)`, a snapshot shows values at
that boundary, before this frame's object updates and contact handling.

### 14.3 Writing the files

The leading underscore in names such as `_frame_count` indicates that they
are internal implementation names; it does not make them inaccessible.
`global` lets a function update the variables defined outside it, preserving
the counter and first-write flags between calls.

The first actual write of each log during a run uses mode `"w"`, replacing
the previous file contents. Later writes use `"a"` to add a line at the end.
This happens on the first write, not immediately when the program launches:
if a new run never reaches a state snapshot or event, an old file can remain.
`with open(...)` closes the file after the block, and `json.dumps(...)`
turns the dictionary into the text written on that line.

The relative output filenames use the process's current working folder,
which is the project folder when launched as shown in this guide. Logging
errors are not caught here; for example, a file-permission error could stop
the game with a traceback. The logger is separate from the visual effects
and does not grant points or decide damage.

Restarting a round with Enter does not reload this module or reset its
diagnostic counters, flags, or initial clock time. The logs belong to the
running program and can span several rounds; round state such as score,
lives, and objects is reset separately. Relaunching the process initializes
the logging module again.

<a id="current-limits" name="current-limits"></a>

## 15. Current behavior and limits

These describe the code as it stands, not missing features that this guide
claims have been implemented.

- **Contacts are checked at sampled positions.** A bullet or ship that moves
  far enough between frames can pass a target without being found overlapping.
  Updating before checking contact does not perform a continuous path test.
- **Opposite screen edges are not connected for collision math.** An object
  moves across when `wrap()` changes its coordinates; contact checks still
  compare ordinary x/y positions in the window.
- **Rock appearance and contact size differ.** The rock's uneven outline is
  inside its circular collision area. Contact can therefore happen in a
  small visually empty gap near that outline. The ship's checks use a triangle.
- **Piercing bullets can hit later fragments, but do not guarantee a chain
  clear.** They still move, can miss, and expire after 1.5 seconds.
- **The speed limit is applied inside `accelerate()`.** Once a speed bonus
  expires, a still-coasting ship can remain above the normal limit until drag
  slows it or another acceleration call applies the normal limit. The next
  movement update always applies drag after handling thrust.
- **Weapons and keys are selected with separate `if` statements.** If several
  number keys are held at once, later matching assignments win; key 4 is
  checked last. Left/Right and Up/Down are also separate checks, so simultaneous
  opposite inputs are processed in order rather than choosing just one.
- **Bombs, bonuses, and lives have different creation rules.** You start with
  three bombs and cannot replenish them in this code. Only bullet hits run
  the random collectible-creation check. There are no extra-life items.
- **Restart resets the round, not the application.** Enter after game over
  clears the old world and starts from zero score and full lives, bombs,
  and default ship settings. Mute/volume and diagnostic logging remain
  associated with the running process. There is still no save/load or enemy ship.
- **Some settings are older course leftovers.** `PLAYER_SPEED`,
  `PLAYER_SHOOT_SPEED`, and `PLAYER_SHOOT_COOLDOWN_SECONDS` are defined but
  do not drive the current motion or weapons. Changing them alone will not
  change the active behavior.
- **New objects can be visible before their first update.** Each loop uses
  its own list of members; do not infer a mandatory one-frame delay for
  every operation just because an object was created during another loop.

<a id="change-map" name="change-map"></a>

## 16. Where to look when you want to change something

| Desired change | Read or edit first | Other connections to check |
| --- | --- | --- |
| Window dimensions | `SCREEN_WIDTH`, `SCREEN_HEIGHT` in `constants.py` | Ship center, edge starting positions, wrapping, background size, and fixed-size help-panel layout |
| Ship turning or engine feel | `PLAYER_TURN_SPEED`, `PLAYER_ACCELERATION`, `PLAYER_DRAG`, `PLAYER_MAX_SPEED` | `Player.rotate`, `accelerate`, `update`, and the temporary speed multiplier |
| A movement/fire key | `Player.update` in `player.py` | `CONTROLS` in `controls.py`, README controls, and this guide |
| Bomb/help/start/quit key | Event handling in `main.py` | Instruction text and ensuring menus still accept close/quit input |
| Weapon properties | `WEAPONS` in `constants.py` | `Player.shoot`, `Shot`, and main's bullet-hit handling |
| A new selectable weapon | Add its `WEAPONS` entry and selection in `Player.update` | Start/help rows and documentation; the existing fixed panel may need more room |
| Rate, size, or speed of new rocks | `AsteroidField.update` and rock settings | The starting speed range is in the function; keep edge-start distances and rock wrapping compatible |
| Shape of rocks | `Asteroid.__init__` and `draw` | Circular contact checks do not automatically change with the outline |
| Points or starting lives | `SCORE_*` and `PLAYER_LIVES` | `Asteroid.points`, main's hit branches, and HUD text |
| Bonus color, lifetime, or effect duration | `POWERUP_COLORS`, `POWERUP_LIFETIME_SECONDS`, shield/speed settings | `PowerUp`, `Player.apply_powerup`, `is_protected`, `accelerate`, and the on-screen explanations |
| A new kind of bonus | Its settings, `PowerUp` color lookup, and `Player.apply_powerup` | Main's random choice currently lists only shield/speed; any new timer/effect also needs updating and drawing rules |
| Bomb strength or waiting time | `BOMB_BLAST_RADIUS`, `BOMB_FUSE_SECONDS` | Main's distance check, bomb countdown, and displayed instructions |
| Explosion appearance | `spawn_explosion`, `Particle.draw`, and the counts passed by main/rocks | These visual changes do not change bomb damage range |
| Background image | `background.load_background` and the call in `main.py` | Add the referenced file under `assets`; open the display before `.convert()` |
| Help-panel appearance | `draw_controls` in `controls.py` | Its panel size and row spacing are literal numbers; this function draws help but does not pause the game itself |
| Log detail or frequency | `logger.py` | Frame limits, sampled member limit, output formats, and any course checks that read them |
| Effects, music, or initial volume | `sounds.py`: `EFFECTS`, `make_music`, and `SoundEffects` | Ship methods request shot/drop effects; main requests hits/bonuses/blasts and handles M/volume events. Update instruction text if keys change. |

<a id="understanding-questions" name="understanding-questions"></a>

## 17. Check your understanding

Try answering before reading the answer column. These questions connect
multiple files rather than asking you to memorize Python vocabulary.

| Question | Answer to check against |
| --- | --- |
| Why does importing `Player` not make the ship appear? | An import makes the blueprint name available; the actual ship is created later by `Player(...)`, joins drawing groups, and becomes visible when the loop draws it. |
| Why must `Shot.containers` be set before firing? | `CircleShape` reads it during each new bullet's setup; it tells Pygame which collections the bullet should join. |
| How can a bullet move after the player releases Space? | `Shot` has its own position and velocity and is already in `updatable`; Space controls creating bullets, not the motion of existing ones. |
| Why does the ship collect a bonus but an explosion dot does not? | Main checks the player against members of `powerups`; explosion dots are not included in that collection or used as the collecting object. |
| Why does a bonus created by a bullet hit wait until a later frame to be collected? | The bonus-collection loop already ran earlier in that frame. |
| Does `Bomb.update()` award points? | No. It sets `detonated`; the later bomb-handling code in main finds nearby rocks, adds their point values, and removes them. |
| Does every exploded large rock award a possible 520 points immediately? | No. A bullet-destroyed large rock gives 20 now; the extra points require subsequently destroying its smaller descendants. Bombs do not create those descendants. |
| Why does H freeze a bomb without changing the bomb file? | The help branch skips the whole group update, so the bomb's countdown function is not called while paused. |
| Does a cyan shield make the ship blink? | No. It draws a ring and prevents damage; the separate respawn timer controls blinking. |
| Does `kill()` immediately make an object's position unreadable? | No. It removes group membership; code that still references the object can still read its stored values. |
| Where would you change the arrow keys? | `Player.update`, then update the controls displayed by `controls.py` and the documentation to match. |
| Why might a log's elapsed seconds grow while a bomb stays frozen? | The logger reads clock time, but the bomb subtracts `dt` only when its update is called during active play. |

If an answer is unclear, follow the named call into its defining file and
read what it receives, what values it changes, and whether it returns
anything. Then return to the calling line and continue with the next step.
That is how to trace this program without needing to understand every file
at once.

<a id="trace-a-problem" name="trace-a-problem"></a>

## A method for tracing a problem

Use this process when the result differs from what you expected. Finding
the first step where reality differs is more useful than changing several
unrelated numbers and hoping one fixes it.

1. **Describe one observable symptom.** For example, "Holding Space creates
   no visible bullets after I press Enter" is more specific than "weapons
   are broken." Note whether the game exits, displays an error, freezes,
   or keeps moving with only one action missing.
2. **Confirm the conditions for that action.** Is play started, help closed,
   and the game window receiving keyboard input? A paused screen deliberately
   skips updates, so frozen bullets there are expected behavior.
3. **Find the entry point.** Held Space is checked in `Player.update`.
   A B press is handled in main's event loop. The file drawing a label is
   not necessarily the file implementing that key.
4. **Follow the calls in order.** For firing, follow `Player.update` →
   `shoot` → `Shot.__init__` → `CircleShape.__init__`. Ask what condition
   could return early, what values are supplied, and which groups are joined.
5. **Observe one useful value at a time.** Does `shoot_timer` reach zero?
   Is `weapon` a valid `WEAPONS` key? Does the bullet group gain members?
   Does a member have nonzero velocity? Does main's drawing loop include it?
6. **Compare with the code's timing.** A new bullet can be drawn before its
   own first movement update. A newly dropped bonus cannot be collected
   by a loop that already ran earlier in the frame. Those are order effects,
   not evidence that the objects failed to exist.
7. **Change the first incorrect step, then repeat the same scenario.** Keep
   unrelated tuning changes separate so you know which change caused the result.

### Using a small temporary print

Inside `Player.shoot`, after the countdown check, a temporary diagnostic
could be:

```python
print("firing weapon:", self.weapon, "delay:", self.shoot_timer)
```

This runs only when that point in the function is reached. No message
does not automatically mean Python ignored `print`: the key check or the
earlier return may have prevented reaching it. Immediately after
`updatable.update(dt)` in main, another possible check is:

```python
print("bullet count:", len(shots))
```

This is diagnostic code you would add temporarily, not a feature already
added to the game. A per-frame print can produce many lines; use it briefly
and remove it once you have the information. A count above zero tells you
bullets exist in that collection, not that they are necessarily on screen.

### Reading an error without guessing

A **traceback** is the list Python prints showing how function calls led
to an error. Start with the final exception type and message, then find the
last relevant project-file location listed above it. Open that actual line,
read the surrounding function, and trace the supplied values backward.

| Hypothetical message or symptom | What it tells you | Where to investigate in this project |
| --- | --- | --- |
| `NameError` for `Shot` | This file does not have that name available at this point. | Its imports and spelling, not the unrelated file that happens to use Shot successfully. |
| `KeyError: 'laser'` during firing | A lookup requested the key laser, which is absent from the dictionary being read. | The selected weapon name and `WEAPONS`; adding a key selection without its settings entry would cause this. |
| `AttributeError` mentioning `position` | The value being used lacks the expected stored position. | What object it is and whether its setup called the shared initialization; the exact traceback location matters. |
| Bullets exist but do not move | Creation succeeded at least far enough to join the checked group. | Their velocity, membership in `updatable`, and whether active updates are running. |
| Object position changes but nothing is drawn | Motion is occurring, so creation alone is not the whole problem. | Membership in `drawable`, its draw method, on-screen coordinates, and whether a later image covers it. |
| Changing a firing-speed setting has no effect | The changed value may not be what this behavior reads. | Trace `Player.shoot` into its selected `WEAPONS` entry; the older `PLAYER_SHOOT_SPEED` is unused. |

The table lists possible explanations, not a diagnosis of every error with
that name. Use the actual message, location, and values from your run.

<a id="study-sessions" name="study-sessions"></a>

## Study sessions and prediction exercises

You do not have to learn this entire document in one sitting. Use the
following checkpoints to decide whether a piece makes sense before adding
another layer.

| Session | Read | You are ready to continue when you can explain... |
| --- | --- | --- |
| 1. Names and one object | Python basics; constants, CircleShape, and Shot chapters | The difference between importing a blueprint and creating an actual bullet, and why each bullet has its own position. |
| 2. The ship | Player chapter and triangle-contact example | Where a held key is read, why velocity differs from position, and why putting player before the dot selects triangle contact logic. |
| 3. Other objects | Rock, creator, dot, item, and bomb chapters | The difference between creating rocks and moving rocks, between a floating bonus and its collected effect, and between blast visuals and damage. |
| 4. Pictures and records | Background, controls, and logger chapters | What is drawn once versus each frame, why drawing PAUSED is not the pause itself, and why log clock time differs from game timers. |
| 5. Connections | Main chapter, value-ownership table, and action journeys | The main loop's order and where score, life loss, object creation, and removal actually happen. |
| 6. Practice | Change map and tracing method | One predicted effect, one observed value, and one explanation supported by the relevant code, rather than by the name of a variable alone. |

Before running an experiment, write down the starting conditions, the line
or setting you plan to change, and the result you expect. Afterward, compare
the result with that prediction. If they differ, trace the function order
before making another change. This is a method for learning; these exercises
do not modify the code automatically.

### Predictions with explained answers

| Stated starting conditions | Predict before looking at the answer | Answer and reason |
| --- | --- | --- |
| Existing unexpired bullet at `(100, 50)`, velocity `(500, 0)`, dt 0.02 | Its position after one update? | `(110, 50)`: velocity times seconds adds `(10, 0)`. There is no bullet drag. |
| Bullet age 1.49, lifetime 1.5, dt 0.02 | Does it move before expiring? | No. Age becomes 1.51, then kill/return happens before its position-change line. |
| Ship timer `shield_timer=0.01`, no respawn protection, dt 0.02 | Is it shield-protected during main's later rock check? | No. Ship update reduces the shield timer below zero before that check. Collection of another shield in the intervening collection loop could change this, so assume no new item is collected. |
| A new shield item is collected while 2.5 seconds of shield remain | What timer value is set on collection? | Five seconds, not 7.5. The assignment replaces the remaining duration instead of adding to it. |
| A newly created bomb has a two-second fuse; its first active update uses dt 0.25 | What are fuse and detonated afterward? | 1.75 and False: the timer is positive, so no explosion signal yet. |
| One medium rock is worth 50 and main's score is 200 | Does calling only `rock.points()` change main's score? | No. It returns 50. Main must use the result in `score += ...` to change the total. |
| A game object is removed with kill but a local variable still refers to it | Can that variable read its position? | Yes. Group removal is not deletion of its stored values or of existing references. |
| Main draws moving objects, then copies the full background over them | Are those earlier object pictures still visible? | No. The later background copy covers them; draw order matters even if all objects updated correctly. |

If you can explain the reason without memorizing the answer, move on. If
not, return to the file chapter and point to the exact assignment, condition,
or call responsible. That ties the explanation to the code you are learning.
