import inspect  # load Python tools that can examine a running function, allowing this logger to read the game variables in the function that called it
import json  # load tools that convert dictionaries and lists into JSON, a standard text format used to save structured game information in log files
import math  # load mathematical helpers; this file uses floor() to round elapsed seconds down rather than keeping a decimal fraction
from datetime import datetime  # import the date/time class so each saved game snapshot or event can include when it happened and how many seconds have elapsed
from typing import NotRequired, TypedDict  # import type-hint helpers: TypedDict describes a dictionary's expected fields, and NotRequired marks fields that may be absent


class SpriteInfo(TypedDict):  # describe the named pieces of information saved for one object, such as its position and size; TypedDict is a note about a dictionary's layout, not a blueprint that creates ships or rocks
    type: str  # declare that the type field stores a text string naming the object class, such as Player or Asteroid
    pos: NotRequired[list[float]]  # declare an optional pos field containing a list of decimal numbers for horizontal and vertical position; an object without position can omit it
    vel: NotRequired[list[float]]  # declare an optional vel field containing horizontal and vertical speed values; velocity means movement speed together with its direction
    rad: NotRequired[float]  # declare an optional rad field containing the center-to-edge distance of the circular area used to check whether objects touch
    rot: NotRequired[float]  # declare an optional rot field containing the object's facing angle in degrees; objects without a rotation attribute do not need this field


class GroupInfo(TypedDict):  # describe what is saved for a collection of objects: how many objects it contains and the details of up to ten of them; the description itself does not collect or save anything
    count: int  # declare that count stores an integer, meaning a whole number, recording the total number of game objects in this collection
    sprites: list[SpriteInfo]  # declare that sprites stores a list of object-detail dictionaries; a sprite is a Pygame game object such as a ship, rock, or bullet


__all__ = ["log_state", "log_event"]  # tell Python which names to bring in if another file writes from logger import *; main.py instead asks for these two function names explicitly

_FPS = 60  # assume 60 active game frames per second when deciding how often to log; the leading underscore marks a helper intended for use inside this file
_MAX_SECONDS = 16  # limit state logging to roughly sixteen seconds worth of active frames; this is a frame-count limit rather than a real-time stopwatch
_SPRITE_SAMPLE_LIMIT = 10  # save details for at most ten objects from each collection, keeping log entries small even when many bullets or explosion dots exist

_frame_count = 0  # start the number of active log_state() calls at zero; this counter stops increasing once the state-logging limit is exceeded
_state_log_initialized = False  # remember whether this run has written its first game-state entry; False means the first write should replace the previous run's file
_event_log_initialized = False  # remember whether this run has written its first named event; later events append instead of replacing the file
_start_time = datetime.now()  # save the clock time when Python first loads this logger file; later timestamps subtract it to measure elapsed real-world seconds


def log_state() -> None:  # define the course helper that occasionally saves the calling function's game objects and timing information; -> None means it returns no result value
    global _frame_count, _state_log_initialized  # tell Python to change the variables defined outside this function; without global, assigning these names here would create separate function-only variables instead of remembering progress between calls

    # Stop logging after `_MAX_SECONDS` seconds
    if _frame_count > _FPS * _MAX_SECONDS:  # stop taking snapshots after the active-frame count exceeds 60 times 16; returning early also stops increasing this counter
        return  # stop running this function now and return control to the code that called it; no result value is supplied

    # Take a snapshot approx. once per second
    _frame_count += 1  # increase the active-frame counter by one whenever this function is called before its limit; += means add and save the result back
    if _frame_count % _FPS != 0:  # skip most frames: % calculates a remainder and != means not equal, so only exact multiples of 60 proceed to save a snapshot
        return  # stop running this function now and return control to the code that called it; no result value is supplied

    now = datetime.now()  # read the current local date/time to timestamp this entry and calculate how long it has been since the logger was first loaded

    frame = inspect.currentframe()  # get Python's record of the currently executing function, called an execution frame, so the logger can find which function called it
    if frame is None:  # check whether Python could not provide an execution frame; None means there is no frame object to inspect, so logging must stop safely
        return  # stop running this function now and return control to the code that called it; no result value is supplied

    frame_back = frame.f_back  # read the previous function's execution frame, normally main(), which contains the actual ship, rock collections, and other game variables
    if frame_back is None:  # check whether no calling-function frame exists; stop instead of trying to read variables from a missing object
        return  # stop running this function now and return control to the code that called it; no result value is supplied

    local_vars = frame_back.f_locals.copy()  # copy the calling function's local variable dictionary, which pairs names such as player or asteroids with their current values

    screen_size: list[int] = []  # create an empty list intended to hold integer width/height values once a Pygame drawing surface is found
    game_state: dict[str, object] = {}  # create an empty dictionary mapping text variable names to captured game information; dictionaries store values under named keys for later lookup
    sprite_info: SpriteInfo  # give the temporary snapshot variable an expected dictionary type for checking tools; this annotation alone does not assign a value or create a dictionary

    for key, value in local_vars.items():  # loop through the copied variables; items() gives each variable name as key and its associated game object or other value as value
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):  # look for a Pygame value with a get_size attribute; type identifies its class, str turns that description into text, and hasattr checks that the attribute exists
            screen_size = list(value.get_size())  # call the surface's size method and convert its width/height pair into a list that can be saved with the snapshot

        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:  # recognize collections of game objects by checking whether their class name contains Group, such as a Pygame sprite Group
            sprites_data: list[SpriteInfo] = []  # start an empty list to hold the individual object dictionaries sampled from this collection

            for i, sprite in enumerate(value):  # go through objects in this group one at a time; sprite is the current object and enumerate provides its zero-based index i
                if i >= _SPRITE_SAMPLE_LIMIT:  # check whether ten objects have already been sampled; the following break keeps the log from recording every object in a large group
                    break  # leave only this object-sampling loop, then continue building the group summary and the rest of the log entry

                sprite_info = {"type": sprite.__class__.__name__}  # create a new dictionary containing the current object's class name, such as Asteroid; more fields are added only when that object has the matching attributes

                if hasattr(sprite, "position"):  # check whether this object has a position attribute before trying to read coordinates, because not every kind of game object stores a position
                    sprite_info["pos"] = [  # add a pos entry to this object's dictionary, storing the horizontal and vertical coordinates listed on the next two lines
                        round(sprite.position.x, 2),  # read the current object's horizontal coordinate and round it to two decimal places to keep saved text compact and readable
                        round(sprite.position.y, 2),  # read the current object's vertical coordinate and round it to two decimal places, completing the saved x/y position pair
                    ]

                if hasattr(sprite, "velocity"):  # check that the object has velocity information before recording how quickly it moves horizontally and vertically
                    sprite_info["vel"] = [  # add a vel entry containing the horizontal and vertical movement speeds listed on the next two lines
                        round(sprite.velocity.x, 2),  # record horizontal speed rounded to two decimal places; negative and positive signs indicate opposite horizontal directions
                        round(sprite.velocity.y, 2),  # record vertical speed rounded to two decimal places; on screen, positive vertical movement goes downward
                    ]

                if hasattr(sprite, "radius"):  # check whether this object stores a radius, its center-to-edge size, before adding that size to the saved information
                    sprite_info["rad"] = sprite.radius  # add the object's radius under the short field name rad, recording the size of its circular collision area

                if hasattr(sprite, "rotation"):  # check whether the object stores a rotation attribute, such as the ship's facing angle, before attempting to read it
                    sprite_info["rot"] = round(sprite.rotation, 2)  # save the object's facing angle under rot, rounded to two decimal places to avoid unnecessary extra digits

                sprites_data.append(sprite_info)  # add the completed dictionary for this one object to the list of sampled object details for the group

            group_info: GroupInfo = {"count": len(value), "sprites": sprites_data}  # build the group summary: len(value) counts all objects, while sprites_data contains details for only the limited sample

            game_state[key] = group_info  # store this group summary using the original variable name as its key, so the log can distinguish asteroids, shots, and other collections

        if len(game_state) == 0 and hasattr(value, "position"):  # if nothing has been recorded yet and this variable has a position, record it as a standalone object instead of requiring a group
            sprite_info = {"type": value.__class__.__name__}  # start a standalone object dictionary with its class name; this follows the same saved format as objects sampled from groups

            sprite_info["pos"] = [  # add a pos entry to this object's dictionary, storing the horizontal and vertical coordinates listed on the next two lines
                round(value.position.x, 2),  # save this standalone object's horizontal position rounded to two decimal places
                round(value.position.y, 2),  # save this standalone object's vertical position rounded to two decimal places, completing its position pair
            ]

            if hasattr(value, "velocity"):  # check whether this standalone object has horizontal/vertical speed values before trying to include them in its dictionary
                sprite_info["vel"] = [  # add a vel entry containing the horizontal and vertical movement speeds listed on the next two lines
                    round(value.velocity.x, 2),  # save this standalone object's horizontal movement speed rounded to two decimal places
                    round(value.velocity.y, 2),  # save this standalone object's vertical movement speed rounded to two decimal places, completing its velocity pair
                ]

            if hasattr(value, "radius"):  # check whether this standalone object has a center-to-edge size before trying to include that information
                sprite_info["rad"] = value.radius  # save this standalone object's radius under rad, recording the size used by its circular collision check

            if hasattr(value, "rotation"):  # check whether this standalone object stores a facing angle before attempting to save a rotation value
                sprite_info["rot"] = round(value.rotation, 2)  # save this standalone object's facing angle in degrees under rot, rounded to two decimal places

            game_state[key] = sprite_info  # add the standalone object's dictionary to the game-state dictionary using its original variable name, such as player

    entry: dict[str, object] = {  # start the final log-entry dictionary, combining timing information, surface size, and all the captured game objects and groups
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],  # format the time as hours:minutes:seconds.fraction; [:-3] removes the final three digits so the fraction shows milliseconds instead of microseconds
        "elapsed_s": math.floor((now - _start_time).total_seconds()),  # subtract the logger's initial time from now, convert the duration to seconds, and round down; this real-world duration includes time spent reading help
        "frame": _frame_count,  # save the active-gameplay frame counter; it stops advancing after state logging reaches its limit, even though later events can still be saved
        "screen_size": screen_size,  # include the width/height pair found while inspecting drawing surfaces in the calling function
        **game_state,  # unpack all key/value pairs from game_state into this final dictionary, placing the captured object and group information beside the timing fields
    }

    # New log file on each run
    mode = "w" if not _state_log_initialized else "a"  # choose file mode w to replace the old state log on this run's first write, otherwise choose a to append another entry without deleting earlier ones
    with open("game_state.jsonl", mode) as f:  # open the state log in the chosen mode and refer to it as f; with automatically closes the file when the indented writing block finishes
        f.write(json.dumps(entry) + "\n")  # convert the entry dictionary to JSON text and add a newline so each snapshot occupies one line; jsonl means JSON Lines

    _state_log_initialized = True  # remember that the first state entry has been written, so future calls append to this run's file instead of overwriting it


def log_event(event_type: str, **details: object) -> None:  # define a function that saves one named action; event_type is text and **details collects any additional named arguments into a dictionary
    global _event_log_initialized  # allow this function to change the event-log flag shared by the whole file, preserving the choice between first-write replacement and later appending

    now = datetime.now()  # read the current local date/time to timestamp this entry and calculate how long it has been since the logger was first loaded

    event: dict[str, object] = {  # start the event dictionary containing its time, active-frame number, supplied event name, and any extra details from the caller
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],  # format the time as hours:minutes:seconds.fraction; [:-3] removes the final three digits so the fraction shows milliseconds instead of microseconds
        "elapsed_s": math.floor((now - _start_time).total_seconds()),  # subtract the logger's initial time from now, convert the duration to seconds, and round down; this real-world duration includes time spent reading help
        "frame": _frame_count,  # save the active-gameplay frame counter; it stops advancing after state logging reaches its limit, even though later events can still be saved
        "type": event_type,  # save the caller's event name, such as player_hit or asteroid_split, so later checks can identify what happened
        **details,  # unpack extra named arguments into this dictionary; if no extra details were supplied, this adds no fields
    }

    mode = "w" if not _event_log_initialized else "a"  # replace the previous run's event log on the first event, then append later events so all actions from this run remain recorded
    with open("game_events.jsonl", mode) as f:  # open the event log in the selected replace-or-append mode; with ensures it is automatically closed after the write finishes
        f.write(json.dumps(event) + "\n")  # convert the event dictionary to JSON text and add a newline, storing one named game action per line in game_events.jsonl

    _event_log_initialized = True  # record that this run has already saved an event, so the next event is appended rather than erasing the earlier ones
