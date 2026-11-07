import io  # bring in Python's in-memory file tool so generated audio can be loaded without creating or downloading sound files
import math  # bring in sine waves and pi, used to make the changing pitches of the arcade sound effects
import random  # bring in random-number tools so explosions can mix a rough noise sound with their musical tone
import struct  # bring in the tool that packs whole-number audio samples into the two-byte format used by a WAV sound
import wave  # bring in Python's WAV-writing tool so Pygame can read the generated samples as a normal sound file
import pygame  # bring in Pygame's mixer, which plays several short sound effects while the rest of the game continues


EFFECTS = {  # give each event a recipe containing duration in seconds, starting pitch, ending pitch, and the fraction mixed with noise
    "shoot_single": (0.11, 950, 300, 0.02),  # make the standard shot a short high-to-low laser sound
    "shoot_spread": (0.14, 650, 180, 0.15),  # make one broader sound per three-bullet volley, rather than stacking three copies
    "shoot_rapid": (0.06, 1400, 650, 0.02),  # keep rapid-fire shots shorter than their firing interval so they stay crisp
    "shoot_heavy": (0.20, 260, 65, 0.30),  # give the slower heavy weapon a deeper, rougher firing sound
    "rock_hit": (0.15, 190, 45, 0.75),  # mix mostly noise into a short impact when a bullet destroys a rock
    "bomb_drop": (0.10, 280, 180, 0.05),  # confirm that a bomb was actually dropped and one was spent from the supply
    "bomb_blast": (0.55, 100, 25, 0.85),  # use a longer low rumble for the bomb explosion, once per bomb rather than once per destroyed rock
    "ship_hit": (0.30, 450, 65, 0.55),  # make losing a life sound different from an ordinary rock impact
    "shield": (0.28, 450, 1100, 0.00),  # use a clean rising tone when the ship collects a cyan shield item
    "speed": (0.24, 700, 1800, 0.00),  # use a faster, higher rising tone when the ship collects a yellow speed item
}


def make_sound(duration, start_pitch, end_pitch, noise):  # create one playable sound from its recipe; pitches are cycles per second, and noise ranges from zero to one
    rate = 44100  # generate 44,100 samples for each second of audio, giving Pygame a standard-quality source sound to convert if needed
    samples = bytearray()  # collect the sound's encoded samples in memory rather than writing a permanent WAV file
    rng = random.Random(0)  # use a separate repeatable random generator so audio creation does not change the game's rock or bonus-item randomness
    for index in range(int(rate * duration)):  # create one amplitude value for every moment sampled during this sound's duration
        time = index / rate  # convert the sample number to seconds since this sound began
        phase = 2 * math.pi * (start_pitch * time + (end_pitch - start_pitch) * time * time / (2 * duration))  # calculate a wave whose pitch gradually moves from the starting frequency to the ending frequency
        tone = math.sin(phase)  # make a smooth repeating wave with amplitude between minus one and one at this point in the sound
        mixed = tone * (1 - noise) + rng.uniform(-1, 1) * noise  # combine the pitched wave with the recipe's amount of rough noise for impacts and blasts
        envelope = min(1, time / 0.005) * (1 - time / duration) ** 2  # fade in over five milliseconds and fade out toward the end, reducing harsh clicks at sound boundaries
        samples.extend(struct.pack("<h", int(14000 * mixed * envelope)))  # convert the amplitude to a quiet signed 16-bit sample; <h writes two bytes in the order expected by a WAV file
    buffer = io.BytesIO()  # make an in-memory file that will hold the WAV header and the generated samples
    with wave.open(buffer, "wb") as wav:  # write a valid WAV file to memory; with closes the WAV writer after its header and samples are finished
        wav.setnchannels(1)  # generate one audio channel, meaning a mono source sound that the mixer can send to the available speakers
        wav.setsampwidth(2)  # store each sample using two bytes, matching the signed 16-bit numbers packed above
        wav.setframerate(rate)  # tell the WAV reader how many sample values represent one second of this recording
        wav.writeframes(samples)  # put all the generated sample bytes after the WAV header in the in-memory file
    buffer.seek(0)  # move back to the file's beginning so Pygame reads the header before reading its audio samples
    return pygame.mixer.Sound(file=buffer)  # load the finished sound into Pygame; its mixer handles converting the mono WAV to the playback format


def make_music():  # create an original eight-second arcade-style loop from a repeating melody, bass line, and simple synthesized percussion
    rate = 22050  # generate fewer samples per second than the effects, which is enough for this deliberately simple retro-style music
    duration = 8  # use four two-second musical bars so the recording returns naturally to the beginning after eight seconds
    chords = ((57, 60, 64), (53, 57, 60), (55, 59, 62), (52, 56, 59))  # store note numbers for A minor, F major, G major, and E major, giving the original loop a small repeating harmonic progression
    melody = (0, None, 2, None, 1, 2, 1, None, 0, None, 2, 1, None, 1, 2, None)  # choose chord-note positions for sixteen short steps in each bar; None makes a rest instead of another beep
    rng = random.Random(1)  # give percussion its own repeatable noise source so composing music does not consume the game's random choices
    samples = bytearray()  # gather the complete recording's audio bytes before loading it into Pygame once
    for index in range(rate * duration):  # calculate one audio amplitude for each sampled instant in the eight-second recording
        time = index / rate  # convert this sample number into seconds since the beginning of the music loop
        step = int(time / 0.125)  # divide each second into eight short steps, producing a 120-beats-per-minute rhythm with four steps per beat
        chord = chords[step // 16]  # choose one chord for each group of sixteen steps, or one two-second bar
        step_time = time % 0.125  # find the elapsed time inside this short step so each note can fade before the following step
        note = melody[step % 16]  # repeat the sixteen-step melody shape while changing its notes to match the current chord
        lead = 0.0  # begin this sample with a silent melody, leaving rests silent when the pattern contains None
        if note is not None:  # make a melody tone only on the steps where the pattern selected a chord note
            frequency = 440 * 2 ** ((chord[note] + 12 - 69) / 12)  # turn the note number into cycles per second, using A at note 69 as the 440-Hz reference
            pulse = 1 if (step_time * frequency) % 1 < 0.25 else -1  # make a narrow pulse wave, a bright electronic tone associated with early arcade sound chips
            lead = pulse * 0.13 * min(1, step_time / 0.003) * (1 - step_time / 0.125)  # give the melody a soft attack and a fading end so short notes are distinct rather than continuous noise
        beat_time = time % 0.5  # measure the position inside the current half-second beat for the repeating bass and drum hits
        bass_frequency = 440 * 2 ** ((chord[0] - 12 - 69) / 12)  # choose the chord's low root note one octave lower for a steady bass pulse
        bass = math.sin(2 * math.pi * bass_frequency * beat_time) * 0.16 * min(1, beat_time / 0.005) * (1 - beat_time / 0.5)  # make the bass smoother and lower than the bright melody, fading it over each beat
        kick = math.sin(2 * math.pi * (65 * beat_time + 2 * (1 - math.exp(-30 * beat_time)))) * math.exp(-28 * beat_time) * 0.12  # make a short falling-pitch thump at the beginning of each beat
        hat = rng.uniform(-1, 1) * math.exp(-95 * step_time) * 0.025  # use a brief, quiet burst of noise on each step as a simple high-hat-like percussion tick
        edge_fade = min(1, time / 0.01, (duration - time) / 0.01)  # soften the first and last ten milliseconds so repeating the recording avoids a hard cut between nonzero samples
        samples.extend(struct.pack("<h", int(18000 * (lead + bass + kick + hat) * edge_fade)))  # combine the instruments at a deliberately restrained level and encode one signed 16-bit WAV sample
    buffer = io.BytesIO()  # hold the complete loop as a WAV recording in memory rather than adding an external music download
    with wave.open(buffer, "wb") as wav:  # write the same standard WAV structure used for the shorter effects
        wav.setnchannels(1)  # use a mono recording that Pygame can send to the available audio device
        wav.setsampwidth(2)  # encode each amplitude as two bytes, matching the samples packed above
        wav.setframerate(rate)  # describe the recording's sample rate so it plays at the intended speed and pitch
        wav.writeframes(samples)  # write the generated melody, bass, and percussion into the recording
    buffer.seek(0)  # rewind the in-memory file so Pygame starts reading from its WAV header
    return pygame.mixer.Sound(file=buffer)  # load the complete loop once so a dedicated channel can repeat it without regenerating notes during gameplay


class SoundEffects:  # define a manager that owns the generated effects, music loop, shared volume, and mute setting for one game session
    def __init__(self):  # create this game's sound manager after pygame.init has attempted to open the audio device
        self.enabled = pygame.mixer.get_init() is not None  # remember whether Pygame successfully opened an audio device; no device should not prevent the game from running
        self.volume = 0.5  # begin at half of the generated sounds' playback volume, with all effects sharing the same master setting
        self.muted = False  # begin with sound allowed; muting will stop playing effects without forgetting the chosen volume
        self.effects = {}  # keep generated Pygame Sound objects under their event names so effects are built once rather than during every shot
        if not self.enabled:  # handle a computer or WSL session that has no working audio device
            print("Audio device unavailable; continuing without sound.")  # explain the silent mode in the terminal instead of raising an error and closing the game
            return  # finish setup with an empty sound collection; play() below will safely do nothing
        try:  # keep sound-loading failure separate from the rest of the game so graphics and controls can still run
            pygame.mixer.set_num_channels(16)  # allow multiple impacts and bonus sounds to play together without a new playback thread in the game code
            pygame.mixer.set_reserved(2)  # keep channels zero and one free from automatically selected impacts so weapons and music have their own playback slots
            self.shot_channel = pygame.mixer.Channel(0)  # give weapon sounds their own channel so rapid fire cannot occupy all the channels needed for damage and bonuses
            self.music_channel = pygame.mixer.Channel(1)  # reserve a separate playback channel for the continuous background loop
            for name, recipe in EFFECTS.items():  # visit each named recipe once while setting up this game session
                self.effects[name] = make_sound(*recipe)  # pass the recipe's four values as separate arguments and store the resulting playable sound under its event name
            self.music = make_music()  # compose and cache the original arcade loop once while the game starts
            self.change_volume(0)  # apply the initial master volume to effects and the quieter background music without changing its value
            self.music_channel.play(self.music, loops=-1)  # repeat the cached background track until the game exits or the user mutes audio
        except pygame.error as error:  # handle an audio-device or sound-conversion failure reported by Pygame
            self.enabled = False  # switch this manager to silent mode while leaving the rest of the game usable
            pygame.mixer.stop()  # stop any already-created effects if audio setup could not finish successfully
            print(f"Audio unavailable; continuing without sound: {error}")  # leave the reason in the terminal so the user can investigate the audio device later

    def play(self, name):  # play a named event without waiting for it to finish, allowing the game loop to keep moving
        if not self.enabled or self.muted:  # ignore playback requests when no audio device exists or the user has muted effects
            return  # leave this function without changing gameplay or the cached sound settings
        sound = self.effects[name]  # find the generated recording associated with this event name
        if name.startswith("shoot_"):  # recognize the four weapon events by the shared beginning of their names
            self.shot_channel.play(sound)  # play weapon audio on its dedicated channel, replacing an earlier shot there if it is still playing
        else:  # use the remaining playback channels for impacts, collected bonuses, and bomb events
            sound.play()  # ask Pygame to play this effect on a free unreserved channel; this call does not pause the game

    def toggle_mute(self):  # change whether future effects can be heard while keeping the user's volume level for later unmuting
        self.muted = not self.muted  # reverse the current yes/no setting so M alternates between muted and audible playback
        if self.enabled and self.muted:  # stop current effects immediately when entering mute, rather than letting long blasts keep sounding
            pygame.mixer.stop()  # silence active effect channels; the generated Sound objects remain cached and can be played again after unmuting
        elif self.enabled:  # restore the background loop when leaving mute; old impacts and shots are not replayed
            self.music_channel.play(self.music, loops=-1)  # begin the original loop again and keep it repeating while sound is allowed

    def change_volume(self, amount):  # add an adjustment such as 0.1 or -0.1 to the remembered master volume, including while muted
        self.volume = max(0, min(1, round(self.volume + amount, 2)))  # keep volume between zero and one and round away small decimal accumulation errors
        for sound in self.effects.values():  # visit every generated sound so all kinds of effects follow the same master control
            sound.set_volume(self.volume)  # apply the new volume to this effect; changing volume while muted does not automatically unmute the game
        if self.enabled and hasattr(self, "music"):  # apply background volume only after the generated music object exists and the audio device is usable
            self.music.set_volume(self.volume * 0.35)  # keep background music at 35 percent of the effects' master setting so important action sounds stay clear

    def status_text(self):  # return a short label main can draw during gameplay and on the instruction screens
        if not self.enabled:  # distinguish an unavailable audio device from the user's deliberate mute choice
            return "Sound: unavailable"  # tell the player why volume keys cannot produce audible sound in this session
        level = round(self.volume * 100)  # convert the zero-to-one setting into a familiar percentage for display
        return f"Sound: {'muted' if self.muted else str(level) + '%'}  |  M: mute  -/+: volume"  # show the current audible/muted setting together with the keys that control it
