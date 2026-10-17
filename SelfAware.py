#!/usr/bin/env python3
import time
import sys
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf


AUDIO_FILE    = "D:/Code/Lyrics/SelfAware/SelfAware.wav"
BLOCKSIZE     = 2048
WAVE_HEIGHT   = 20
WAVE_WIDTH    = 50
SONG_TITLE    = "Self Aware"
SONG_ARTIST   = "Temper City"
SONG_ALBUM    = "Self Aware"
START_SECONDS = 90

ROW_ART_START = 1
ROW_DIVIDER   = ROW_ART_START + WAVE_HEIGHT + 1
ROW_LYRICS    = ROW_DIVIDER + 2

stdout_lock = threading.Lock()

lyrics = [
    ("God, you look so pretty", 0.07),
    ("When you tell me that you love me",  0.09),
    ("I wish that I could lie", 0.09),
    ("But my mind gets in the way", 0.09),
    ("I know you think that I'm", 0.07),
    ("Always way too self-aware",  0.09),
    ("Oh, we could never be together", 0.09),
    ("But it's nice to play pretend", 0.09),
    ("I wish that I could lie", 0.09),
    ("But I'm way too self-aware", 0.09),
]
delays = [1.4, 0.8, 1.8, 0.2, 1.0, 0.9, 0.7, 0.4, 0.7, 0.6]

data, samplerate = sf.read(AUDIO_FILE, dtype="float32")
if data.ndim > 1:
    data = np.mean(data, axis=1)
data = data / np.max(np.abs(data))
start_idx = int(START_SECONDS * samplerate)

P = "\033[38;2;237;28;36m"
S = "\033[38;2;255;120;120m"
D = "\033[38;2;160;20;28m"
G = "\033[38;2;220;90;90m"
R = "\033[0m"

CD = [
    f"        {S}* * * * * * * *{R}         ",
    f"     {S}* {R}{P}. . . . . . . . .{R}{S} *{R}     ",
    f"    {S}*{R}{P}. . . . . . . . . . .{R}{S}*{R}    ",
    f"   {S}*{R}{P}. . .{R} {D}* * * * *{R} {P}. . . .{R}{S}*{R}   ",
    f"  {S}*{R}{P}. . .{R} {D}* *{R} {G}o   o{R} {D}* *{R} {P}. . .{R}{S}*{R}  ",
    f"  {S}*{R}{P}. . .{R} {D}*{R} {G}o{R} {S}(   ){R} {G}o{R} {D}*{R} {P}. . .{R}{S}*{R}  ",
    f"  {S}*{R}{P}. . .{R} {D}* *{R} {G}o   o{R} {D}* *{R} {P}. . .{R}{S}*{R}  ",
    f"   {S}*{R}{P}. . .{R} {D}* * * * *{R} {P}. . . .{R}{S}*{R}   ",
    f"    {S}*{R}{P}. . . . . . . . . . .{R}{S}*{R}    ",
    f"     {S}* {R}{P}. . . . . . . . .{R}{S} *{R}     ",
    f"        {S}* * * * * * * *{R}         ",
    f"                                ",
    f"  {P}{SONG_TITLE:<28}{R}  ",
    f"  {S}{SONG_ARTIST:<28}{R}  ",
    f"  {G}{SONG_ALBUM:<28}{R}  ",
    f"                                ",
    f"                                ",
    f"                                ",
    f"                                ",
    f"                                ",
]
CD_WIDTH = 32

def build_frame(chunk):
    step   = max(1, len(chunk) // WAVE_WIDTH)
    levels = np.abs(chunk[::step])[:WAVE_WIDTH]
    levels = np.pad(levels, (0, max(0, WAVE_WIDTH - len(levels))))
    levels = np.interp(levels, [0, 1], [0, WAVE_HEIGHT]).astype(int)

    red_light = "\033[38;2;255;99;99m"
    red_deep  = "\033[38;2;200;30;30m"
    dark  = "\033[38;2;40;28;34m"
    reset  = "\033[0m"
    CLEAR  = "\033[K"

    WAVE_COL = CD_WIDTH + 3

    buf = ""
    for row_i, row in enumerate(range(WAVE_HEIGHT, 0, -1)):
        screen_row = ROW_ART_START + row_i
        bar_color = red_light if row_i < WAVE_HEIGHT / 2 else red_deep
        wave = "".join(
            (bar_color + "█" if lvl >= row else dark + "█") + reset
            for lvl in levels
        )
        cd_line = CD[row_i] if row_i < len(CD) else ""
        buf += f"\033[{screen_row};1H{cd_line}"
        buf += f"\033[{screen_row};{WAVE_COL}H{wave}{CLEAR}"

    buf += (
        f"\033[{ROW_DIVIDER};1H"
        + "\033[38;2;190;50;50m"
        + "─" * (CD_WIDTH + WAVE_WIDTH + 4)
        + reset
        + "\033[K"
    )
    return buf

def callback(outdata, frames, time_info, status):
    global start_idx
    if status:
        print(status, file=sys.stderr)

    frames = int(frames)
    chunk  = data[start_idx : start_idx + frames]

    if len(chunk) < frames:
        outdata[: len(chunk), 0] = chunk
        outdata[len(chunk):, 0]  = 0
        raise sd.CallbackStop
    else:
        outdata[:, 0] = chunk

    frame_str = build_frame(chunk)
    with stdout_lock:
        sys.stdout.write(frame_str)
        sys.stdout.flush()

    start_idx += frames

def animate_text(text, row, delay=0.1):
    for j, char in enumerate(text):
        with stdout_lock:
            sys.stdout.write(f"\033[{row};{j + 1}H\033[38;2;255;120;120m{char}\033[0m")
            sys.stdout.flush()
        time.sleep(delay)
    with stdout_lock:
        sys.stdout.write(f"\033[{row};{len(text) + 2}H\n")
        sys.stdout.flush()

def sing_song():
    time.sleep(0.5)
    with stdout_lock:
        sys.stdout.write(
            f"\033[{ROW_LYRICS - 1};1H\033[38;2;220;90;90m\033[2mLYRICS\033[0m"
        )
        sys.stdout.flush()

    for i, (lyric, speed) in enumerate(lyrics):
        time.sleep(delays[i])
        animate_text(lyric, ROW_LYRICS + i, speed)

with stdout_lock:
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

lyric_thread = threading.Thread(target=sing_song, daemon=True)

with sd.OutputStream(
    channels=1,
    samplerate=samplerate,
    callback=callback,
    blocksize=BLOCKSIZE,
):
    lyric_thread.start()
    sd.sleep(int((len(data) - start_idx) / samplerate * 1000))

with stdout_lock:
    sys.stdout.write("\033[?25h\n\n\033[0m")
    sys.stdout.flush()