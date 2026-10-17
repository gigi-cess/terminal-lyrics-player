# Terminal Lyrics Player

Terminal audio player that shows a live, audio-reactive waveform beside CD-style album art, with lyrics.

Plays a local audio file and shows its lyrics in the terminal, with a waveform that responds to the audio in real time.

Song Title: Self Aware
Song Artist: Temper City

### How it works

- Plays the audio through `sounddevice` starting at a set offset (`START_SECONDS`).
- Draws a waveform from the audio level of each block of samples.
- Types each lyric at a timed delay so it lines up with the song.

### Requirements

- Python 3.8+
- `pip install numpy sounddevice soundfile`
- A terminal with ANSI color support (Windows Terminal, macOS Terminal, most Linux terminals)

### Usage

1. Add your own WAV file to the project folder, for example `your-song.wav`. Audio files aren't included in this repo.
2. Set `AUDIO_FILE` in `terminal_lyrics_player.py` to match the filename.
3. Edit the `lyrics`, `delays`, and song metadata (`SONG_TITLE`, `SONG_ARTIST`, `SONG_ALBUM`) to match your song.
4. Run `python terminal_lyrics_player.py` and press `Ctrl+C` to stop.

### Notes

- Audio files and full lyrics are copyrighted. Don't commit them to the repo. Use your own licensed files, or short example lines only.
- Timing values are hand-tuned for one song and will need adjusting for others.
- All songs, lyrics, and other copyrighted material mentioned or used belong to their rightful owners.
