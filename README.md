# Asteroids

A Python/Pygame Asteroids game with four weapons, bombs, power-ups, three
lives, and original synthesized arcade music and sound effects. Built from
the Boot.dev Asteroids project.

## Run

Install Python 3.13 or newer and `uv`, then run from the project folder:

```bash
uv run main.py
```

The game opens on a controls screen. Press **Enter** to play. During a game,
press **H** to pause and show the controls; press **H** or **Enter** to resume.
Movement, spawning, collisions, and timers stay frozen while help is open.

When you lose the last life, the game stays open and shows your final score.
Press **Enter** to play again or **Esc** to quit. A new round clears every old
game object and resets score, lives, weapons, bombs, and bonus timers. Your
music, mute, and volume settings stay as you left them.

## Controls

| Key | Action |
| --- | --- |
| Left / Right | Rotate |
| Up / Down | Forward / reverse thrust |
| Space (hold) | Shoot |
| 1 | Single shot |
| 2 | Three-shot spread |
| 3 | Rapid fire |
| 4 | Heavy piercing shot |
| B | Drop a bomb (three per game, two-second fuse) |
| H | Pause and show / hide controls |
| M | Mute / unmute music and effects |
| - / + | Lower / raise master volume by 10 percentage points |
| Enter | Start, resume from help, or play again after game over |
| Esc | Quit |

Touch a cyan bonus item to gain a shield, or a yellow bonus item to boost
speed. Each effect lasts five seconds after collection. The ship keeps
drifting after you release thrust and reappears on the opposite side when
it leaves the window.

## Audio

An original eight-second chiptune loop plays in the background, with distinct
sounds for all four weapons, rock hits, bomb drops/blasts, ship damage, and
collecting shield/speed items. The game synthesizes them in memory at startup;
no downloaded music, sound files, or additional Python packages are needed.

Music stays quieter than the action effects. **M** immediately mutes both;
press it again to restart the music and allow new effects. **-** lowers master
volume and **+** raises it; the unshifted **=** key and keypad +/- also work.
These keys work on the start screen, while paused, and during play. Changing
volume while muted remembers the setting without unmuting. Music continues
while reading paused help or the final-score screen. Audio settings stay the
same when Enter starts another round and reset only when the program is relaunched.

If an audio device cannot be opened, the game continues silently and shows
**Sound: unavailable** instead of preventing you from playing.

## Study guide

Read [asteroids_guide.md](asteroids_guide.md) for a beginner's explanation of
the whole project. It starts with Python words and symbols, maps all 14
Python files, gives each file its own detailed chapter, and follows actual
calls from keyboard input through movement, bullet hits, bombs, bonuses,
scoring, and drawing. Each file chapter covers its job and purpose, imports,
stored values, functions in source order, connections, a worked example,
and an explained question.

The complete contents links to those chapters and individual features. The
guide also includes diagrams, startup and pause behavior, course logs,
current limitations, where to make changes, a value-ownership table, a
Python/Pygame/project-code reference, and a method for tracing problems.
A suggested reading order and prediction exercises let you check your
understanding against the code.

The start/help and game-over panels are drawn in `controls.py`; `main.py`
manages starting, pausing, resuming, and resetting rounds. The guide explains
both sides of that connection.

## WSL display troubleshooting

If the game runs but only shows a blank taskbar preview with
`[WARN:COPY MODE]`, WSLg's display service may need restarting. Save your
WSL work, run `wsl --shutdown` in **Windows PowerShell**, reopen Ubuntu,
and run the game again.

If graphics work but the game shows **Sound: unavailable**, Ubuntu also needs
its native PulseAudio client library to reach WSLg's audio server. This machine
was missing `libpulse0`; installing it restored Pygame playback. On another
Ubuntu setup with the same missing-library error, install it with
`sudo apt install libpulse0` and relaunch the game.
