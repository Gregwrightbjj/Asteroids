# How Your Asteroids Game Works (and Why): Private Study Guide

This guide explains how the finished game (all 13 extensions) works, why it is
built this way, and how every piece connects. It has no big code dumps on
purpose: the code lives in the chat. Read this next to your files.

## 0. About this hidden file

- A file whose name starts with a dot is hidden in Linux. `ls` skips it,
  `ls -a` shows it, `cat .asteroids_guide.md` prints it.
- Hidden is not secret. Git still tracks it. To keep it off GitHub:
  `printf '\n.asteroids_guide.md\n' >> .gitignore`

## 1. Safety first

- Submit the Boot.dev lessons BEFORE adding extensions. Their tests read your
  log files and expect exact behavior (for example, one `player_hit`).
- Work on a Git branch: `git checkout -b extensions`. A *branch* is a separate
  line of commits. `git checkout main` returns to the safe version.
- Add one feature at a time, run the game, commit.

## 2. The 30-second picture

The game is a **loop** that runs about 60 times per second. Each trip (a
**frame**) does the same things in the same order:

1. Read events (window closed? bomb key pressed?).
2. Update every object (move it, count down its timers).
3. Resolve interactions (bombs, pickups, collisions, scoring).
4. Draw everything onto the screen, then show it.
5. Wait so the speed stays at 60 frames per second, and measure how long
   the frame took (`dt`).

Everything in the game is either an **object** (ship, asteroid, bullet,
particle, pickup, bomb) or **bookkeeping** (score, lives, timers).

## 3. One frame, step by step, and why the order matters

```
log_state()                     record the game for the course tests
for event in pygame.event.get() events: window close, bomb key (KEYDOWN)
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

- **Update before collisions.** Collisions compare positions. If you checked
  first, you would compare last frame's positions with this frame's
  decisions, and objects could pass through each other.
- **Draw after all changes.** Objects destroyed this frame must not be drawn.
  Drawing last means the picture matches the game state.
- **Background first, HUD last.** Later drawing covers earlier drawing, like
  layers of paper.
- **`flip()` after drawing.** pygame draws into a hidden copy of the screen;
  `flip()` swaps it into view, so the player never sees a half-drawn frame.
- **`tick()` at the end.** It pauses just long enough for a 60 FPS cap and
  returns the milliseconds since the previous call, which becomes `dt`.
  `dt` is therefore the duration of the PREVIOUS frame, which is the
  standard approach.

## 4. How the files connect

```
constants.py        imports nothing; everyone reads it
circleshape.py      imports constants
shot.py             imports circleshape, constants
particle.py         imports circleshape
powerup.py          imports circleshape, constants
bomb.py             imports circleshape, constants
asteroid.py         imports circleshape, constants, particle, logger
asteroidfield.py    imports asteroid, constants
player.py           imports circleshape, constants, shot, bomb
background.py       imports constants
main.py             imports all of them
```

Arrows only point "downhill" toward more basic files. That is deliberate:
a **circular import** (file A imports B, and B imports A) makes Python fail
at startup. For example `bomb.py` does not import `player.py`, because
`player.py` already imports `bomb.py`.

**Separation of jobs** is the idea behind the file list:
`constants.py` = numbers, `circleshape.py` = shared behavior, each object
file = what that object is and does, `main.py` = how objects interact.

## 5. Core mechanisms in depth

### 5.1 Classes, inheritance, and which method runs

A **class** is a blueprint; an **instance** is one object built from it.
`class Player(CircleShape)` means Player starts with everything CircleShape
has (`position`, `velocity`, `radius`, `collides_with`, `wrap`) and adds or
replaces things.

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

`super().__init__(...)` runs the parent's setup. Skip it and attributes like
`position` would never exist.

### 5.2 Groups and containers: how objects join the game

`pygame.sprite.Group` is a collection. Your game has several, and one object
can be in several (like overlapping circles of a Venn diagram):

| Group | Members | Used for |
|---|---|---|
| `updatable` | ship, asteroids, bullets, particles, pickups, bombs, the spawner | `updatable.update(dt)` |
| `drawable` | everything visible (not the spawner) | the draw loop |
| `asteroids` | asteroids only | collision checks |
| `shots` | bullets only | collision checks |
| `powerups` | pickups only | pickup checks |
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

**`kill()`** removes an object from every group it is in. Nothing updates or
draws it afterward, and Python frees it once nothing references it.

**Why separate groups at all?** Different loops need different slices. The
collision loop must test asteroids against bullets, not particles against
anything. Particles are in `updatable` and `drawable` but NOT in `asteroids`
or `shots`, so they are invisible to collision code. Choosing which groups an
object joins is how you choose what it can do.

**Safe to modify during a loop:** iterating a Group walks over a snapshot
list, so `kill()` and newly created objects don't break the loop. New
objects simply aren't visited until the next frame.

### 5.3 Time, units, and `dt`

Every number has a unit. Speeds are pixels per second, turn rates are
degrees per second, timers are seconds. `dt` is seconds per frame (about
0.0167 at 60 FPS). Multiplying "per second" by "seconds" gives the amount to
change THIS frame:

```
position  += velocity * dt     (pixels/second x seconds = pixels)
rotation  += turn_speed * dt   (degrees/second x seconds = degrees)
```

This makes the game run at the same speed on any computer: a slower
computer takes fewer, bigger steps and covers the same distance per second.

**The timer pattern** appears many times in this game, in two forms:

- **Count down to zero** (cooldowns): `shoot_timer`, `invulnerable_timer`,
  `shield_timer`, `speed_boost_timer`, a bomb's `fuse`. Set it to a duration,
  subtract `dt` each frame, and treat `<= 0` as "done".
- **Count up to a limit** (lifetimes): a particle's, shot's, or pickup's
  `age`. Add `dt` each frame and `kill()` the object when `age` reaches
  the limit.

Timers can dip below zero (for example -0.004). That's fine because every
check uses `> 0` or `<= 0`.

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

Every tunable number (speeds, sizes, cooldowns, chances) lives in
`constants.py`. Reasons: one place to tune the game feel, names explain
meaning (`PLAYER_MAX_SPEED` beats `350`), and several files can share a
value so they never disagree. Values derived from others
(`ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS`) stay
consistent automatically when you change the inputs.

## 6. Every feature in depth

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
Player and asteroids call it; bullets don't, since a wrapping bullet could
circle forever (they expire instead, see 6.10). Limitation: collisions
don't cross the seam.

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

**Worked numbers:** fully clearing one large asteroid pays
20 + 2 x 50 + 4 x 100 = 520.

### 6.4 Lives, respawning, and protection

**Mechanism:** `lives` is a variable in `main()`. When the ship is hit:
lives drop by one; if that reaches 0 the game ends; otherwise
`player.respawn()` resets the ship to the center with zero velocity and
starts the invulnerability timer.

**Why the asteroid is also split:** if it were left in place, it would hit
the respawned ship on the next frame. Destroying it removes that overlap.

**Why `continue`:** after the player-hit branch, the asteroid is dead. The
`continue` skips the bullet checks so a destroyed asteroid isn't tested
again.

**`is_protected()`:** one question, "can this ship be hurt right now?",
answered in one place. Today it is true while either the respawn timer or
the shield timer is running. `main.py` asks the question without knowing
the reasons, so adding another protection source later changes only
`Player`.

**Blinking:** while protected, `draw` skips drawing when
`int(timer * 10) % 2 == 0`. `timer * 10` counts tenths of a second left;
`% 2` (remainder after dividing by 2) alternates 0, 1, 0, 1 each tenth, so
the ship vanishes and returns every 0.1 s.

**Where state lives:** `score` and `lives` belong to the whole game, not to
the ship, so they live in `main()`. When `main()` grows, move them into a
`Game` class.

### 6.5 Acceleration

**Before:** pressing W moved the position directly at a fixed speed. The
ship stopped the instant you let go.

**Now:** keys change **velocity**, and velocity moves the position:

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

**Reverse thrust:** passing `-dt` flips the push direction, so Down brakes
and then reverses.

**Connections:** `respawn()` resets `velocity` or the new ship would keep
drifting. The speed power-up (6.11) multiplies acceleration and the cap.

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

### 6.8 Lumpy asteroids

**Mechanism:** when an asteroid is created it builds a list of
**offsets**: points around the center at evenly spaced angles
(`i * 360 / count`), each pulled inward by a random amount. Drawing places
each offset relative to the current `position` and draws a polygon. A random
`spin` rotates the offsets every frame for a tumbling look.

**Key design point, drawing is separate from collision:** the shape is
cosmetic. The hitbox is still the circle of `radius`. The corners only move
inward, so the visible rock never pokes outside its hitbox.

**Connections:** `split()` creates new `Asteroid` objects, so every fragment
gets its own random shape with no extra code.

### 6.9 Triangular hitbox

A circle overlaps a triangle in exactly two ways:

1. The circle's center is **inside** the triangle, or
2. The circle crosses an **edge**, meaning the center is within one radius
   of some edge.

(If the center is outside and the circle overlaps, the circle must cross an
edge, so test 2 catches it.)

**Test 1, point in triangle:** `side(p, a, b)` computes a number whose sign
says which side of edge `a-b` the point is on. Do it for all three edges. If
the signs are mixed, the point is outside; if they all agree (or are zero),
it is inside.

**Test 2, distance to an edge:** treat an edge as a segment from `a` to `b`.
Project the point onto the line: `t = ((p - a) . (b - a)) / |b - a|^2`
(the dot product measures how far along the edge the point's shadow falls;
`t = 0` is at `a`, `t = 1` is at `b`). Clamp `t` between 0 and 1 so the
closest spot stays on the segment, then measure the distance to that spot.

**The call-order trap:** the ship's `collides_with` only runs when called as
`player.collides_with(asteroid)` (5.1). That's why `main.py` calls it that
way.

### 6.10 Weapon types

**Data-driven design:** instead of four `shoot` methods, there is one
`shoot` and a table (`WEAPONS`, a dictionary of dictionaries):

```
"spread": cooldown 0.5, speed 450, radius 4, angles [-15, 0, 15], pierce False
```

`shoot` looks up the current weapon, sets the cooldown, and loops through
`angles`, creating one bullet per angle, each rotated by that angle from the
ship's facing. Adding a weapon means adding a table row, not code.

**Pierce:** a piercing bullet isn't killed when it hits. It keeps flying
and can hit more asteroids.

**The cascade pitfall:** `split()` spawns two fragments exactly where the
bullet still is. A piercing bullet then hits both fragments next frame,
then their fragments, and one shot clears a whole family. Fixing it
(for example, brief immunity for fresh fragments) is a good exercise.

**Bullet lifetime:** every `Shot` has an `age` and kills itself after
`SHOT_LIFETIME_SECONDS`. Without it, bullets fly forever and the `shots`
group grows without limit.

**Default parameters:** `Shot(x, y, radius=SHOT_RADIUS, pierce=False)` lets
older calls like `Shot(x, y)` keep working.

### 6.11 Power-ups

**Pickup object:** `PowerUp` is a small drifting ring with a `kind`
(`"shield"` or `"speed"`). It ages and `kill()`s itself after 8 seconds if
nobody collects it.

**Drop:** when a bullet destroys an asteroid, `random.random() < 0.15`
(True about 15% of the time) creates a pickup at that spot.

**Collect:** each frame, `main()` checks `player.collides_with(powerup)`.
On contact, `player.apply_powerup(kind)` sets a timer and the pickup is
killed.

**Effects are just timers:**

- Shield: `shield_timer` > 0 makes `is_protected()` true and draws a ring.
- Speed: `speed_boost_timer` > 0 makes `boost = 1.5` (otherwise 1) in
  `accelerate`, scaling both the thrust and the speed cap. The line
  `A if condition else B` is a *conditional expression*: it picks A or B.

**Why it fits together so easily:** timers (5.3), `is_protected` (6.4), and
`accelerate` (6.5) were already there. Power-ups mostly flip existing
switches.

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

## 7. Feature interaction map

| Feature | Depends on | Affects |
|---|---|---|
| Arrow keys | pygame key constants | `Player.update` |
| Wrap | screen size, `ASTEROID_MAX_RADIUS` | ship, asteroids |
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

## 8. Ordering rules (and what breaks if you ignore them)

| Rule | If broken |
|---|---|
| Set `X.containers` before creating any X | Objects exist but never update or draw |
| `update` before collision checks | Objects pass through each other |
| `break` after a bullet hit | One asteroid can split twice |
| `continue` after a ship hit | A dead asteroid is tested against bullets |
| `player.collides_with(...)` (player first) | The triangle code never runs |
| Create the font once, before the loop | Slow frames |
| Background first, HUD last, `flip` last | Layers cover each other wrongly |
| Decrease timers before handling keys | Cooldown checks use stale values |
| `.convert()` after `set_mode` | "No video mode" error |
| One `pygame.event.get()` per frame | Events silently disappear |

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
| Ship never gets hit | Called `asteroid.collides_with(player)` while testing triangle code, or the ship is still protected |
| Holding B drops many bombs | Used `get_pressed()` instead of a `KEYDOWN` event |
| Particles collide | They were added to `asteroids` or `shots` |

**Debug habit:** add `print(...)` for one value (a timer, a distance), run,
and watch the terminal. Remove it afterward.

## 10. Experiments to learn by changing things

1. Set `PLAYER_DRAG = 0`. The ship never slows. Why?
2. Set `ASTEROID_LUMPINESS = 0.7`. How do the rocks look, and do hits still
   feel fair?
3. Set `BOMB_FUSE_SECONDS = 0.5`. What changes in how you use bombs?
4. Change `"angles": [-15, 0, 15]` to `[-30, -15, 0, 15, 30]`.
5. Give the heavy weapon `pierce: True` and watch the cascade (6.10).
6. Set `POWERUP_DROP_CHANCE = 1.0` to test every pickup quickly, then
   put it back.
7. Move the wrap margin for asteroids to `ASTEROID_MIN_RADIUS`. Watch
   spawns break, then explain why with section 6.2.

## 11. Glossary

- **Attribute:** a variable stored on an object (`self.rotation`).
- **blit:** copy one Surface onto another.
- **Branch:** a separate line of Git commits.
- **Class / instance:** a blueprint / one object built from it.
- **Clamp:** limit a value to a minimum and maximum.
- **Constant:** a value that doesn't change while the program runs.
- **Container:** a group an object auto-joins when created.
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
- **Inheritance:** a child class gets its parent's attributes and methods.
- **Override:** redefine a parent's method in a child.
- **Particle:** a tiny short-lived object used for effects.
- **Polling:** asking "is it true right now?" every frame.
- **Polymorphism:** one call (`draw`) behaving differently per object.
- **Surface:** a rectangle of pixels you can draw on.
- **Tuple:** a fixed list written with parentheses.
- **Unit vector:** an arrow of length 1 carrying only a direction.
- **Vector2:** an (x, y) point or arrow.
