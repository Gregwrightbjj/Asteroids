# Asteroids

A Python/Pygame Asteroids game with four weapons, bombs, power-ups, and
three lives. Built from the Boot.dev Asteroids project.

## Run

Install Python 3.13 or newer and `uv`, then run from the project folder:

```bash
uv run main.py
```

The game opens on a controls screen. Press **Enter** to play. During a game,
press **H** to pause and show the controls; press **H** or **Enter** to resume.
Movement, spawning, collisions, and timers stay frozen while help is open.

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
| Enter | Start the game or resume from help |
| Esc | Quit |

Touch a cyan bonus item to gain a shield, or a yellow bonus item to boost
speed. Each effect lasts five seconds after collection. The ship keeps
drifting after you release thrust and reappears on the opposite side when
it leaves the window.

## Study guide

Read [asteroids_guide.md](asteroids_guide.md) for a beginner's explanation of
the whole project. It starts with Python words and symbols, maps all 13
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

The shared start/help screen is drawn in `controls.py`; `main.py` manages
starting, pausing, and resuming. The guide explains both sides of that connection.

## WSL display troubleshooting

If the game runs but only shows a blank taskbar preview with
`[WARN:COPY MODE]`, WSLg's display service may need restarting. Save your
WSL work, run `wsl --shutdown` in **Windows PowerShell**, reopen Ubuntu,
and run the game again.
