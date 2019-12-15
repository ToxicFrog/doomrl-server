# libttysound

This library provides experimental closed caption support to the tty version of DoomRL. It does this by replacing the SDL_mixer library, used for playing sound effects. In tty mode, it adds an additional line at the bottom showing what sounds you hear; in graphical mode, it changes the title bar to reflect what you hear.

It has only been tested on Linux. It might work on OSX (using `DYLD_LIBRARY_PATH`). The graphical mode might work on windows; the text mode probably won't without additional work.

There is currently no support for directionality and distance of sound, but this may be added in a future version.

## Prerequisites

- DoomRL, of course
- a C compiler, such as `gcc`
- `make`
- libSDL (both the library and header files)

## Installation (from binary)

- Install DoomRL wherever you please.
- Download the latest ttysound release and unzip it to your DoomRL directory
  - *If you don't mind resetting your configuration*: overwrite `config.lua` when prompted
  - *If you want to keep your configuration*: do not overwrite `config.lua`; instead, add the following lines at the end:
  ```
  ClosedCaptions = true
  ClosedCaptionStyle = 'fancy+sfx'
  NightmareClosedCaptionStyle = 'full'
  dofile 'cc/config.lua'
  ```
- Edit to taste; see the "Settings" section of this README for other configuration options.

## Installation (from source)

- Clone the repo and build the library:
  - `git clone https://github.com/ToxicFrog/doomrl-server.git`
  - `cd doomrl-server/ttysound`
  - `make DRL_SOUND_CONFIG=path/to/doomRL/soundhq.lua`
  If this works you should have a `ttysound/libSDL_mixer-1.2.so.0` file, along
  with a large pile of closed-caption data files in `cc/`.
- Copy the requisite files into your DoomRL directory:
  - `cp -a cc doomrl_cc* libSDL_mixer-1.2.so.0 /path/to/doomrl/installation`
- Edit `config.lua` and add the following lines at the end:
  ```
  ClosedCaptions = true
  ClosedCaptionStyle = 'fancy+sfx'
  NightmareClosedCaptionStyle = 'full'
  dofile 'cc/config.lua'
  ```
  It is important that they be in that order. (See `Settings` below for other possible values of `ClosedCaptionStyle` and `NightmareClosedCaptionStyle`.)

## Running DoomRL with closed captions

The closed captions library comes with a bunch of launcher scripts, all named `doomrl_cc_<whatever>` (plus a plain `doomrl_cc` that just runs DoomRL in the current terminal). Use one of those instead of whatever launcher script you would normally use.

On windows, you can also just run `doomrl.exe` as normal once closed captions are installed.

*Warning:* Unlike plain DoomRL, you require 80 columns and *26 rows* in the terminal for closed captions to display properly. If you aren't using one of the `doomrl_cc` scripts, make sure you adjust whatever you are using to take that into account.

## Settings

The closed captions library has three configuration settings. *All three of them* should be set before loading `cc/config.lua`, which is the script that actually loads the closed caption data. If you don't load this script, or if you load it before setting the configuration, closed captions will not work.

If any of these settings are set to an invalid value, loading will abort with an error message in the terminal.

### ClosedCaptions

Controls whether closed captions are enabled at all.

- `ClosedCaptions = true` turns on closed captions.
- `ClosedCaptions = false` turns them off, even if `cc/config.lua` is loaded.

### ClosedCaptionStyle

Controls how they are displayed.

- `ClosedCaptionStyle = 'fancy'` uses colourful symbols that match the in-game enemy symbols, and is suitable for use in the terminal.
- `ClosedCaptionStyle = 'plain'` uses monochrome symbols, and is suitable for use in graphical mode (or on terminals that don't support colour).
- `ClosedCaptionStyle = 'raw'` displays raw event IDs and is primarily useful for debugging.
- `ClosedCaptionStyle = 'sfx'` does not display anything on screen, but instead sends special terminal control codes that will be used to play the actual sounds, if you are using a compatible terminal. (At the moment, that just means the doomrl-server web terminal; it will not work with other ttys.)
- `ClosedCaptionStyle = 'fancy+sfx'` is equivalent to `fancy`, but includes the control codes from `sfx` as well, so it will both display fancy closed caption icons and, if possible, play the sounds.
- `ClosedCaptionStyle = 'auto'` is equivalent to `'fancy+sfx'` if `Graphics = 'CONSOLE'` in your main configuration file, and equivalent to `'plain'` otherwise. Note that this is not 100% reliable -- if you are overriding the `Graphics` setting with the `-console` or `-graphics` command line options, *it won't know that*.

`'auto'` is the default.

### NightmareClosedCaptionStyle

Controls how sounds for Nightmare creature variants are displayed.

*This setting is currently ignored.*

- `NightmareClosedCaptionStyle = 'full'` gives each nightmare creature its own set of captions.
- `NightmareClosedCaptionStyle = 'limited'` gives each nightmare creature the captions from the equivalent non-nightmare creature, so you can still "hear" them, but can't distinguish them from ordinary enemies.
- `NightmareClosedCaptionStyle = 'none'` makes nightmare creatures completely silent.

`'full'` is the default.

## Adding custom styles

The text displayed for each sound is stored in the `cc/` directory. Each sound is in its own file, in `cc/<CC style>/<creature type>/<event name>`. The contents of this file will be displayed without modification when the sound is played, including any formatting or colour codes.

Adding a new CC style is just a matter of adding a new directory under `cc/` containing the appropriate files. It is recommended that you start by copying an existing style (`cc/raw/` is a good choice) to make sure you don't miss any files. Make sure you also edit the start of `cc/config.lua`; the `styles` table at the start of the file determines which style names are recognized as valid.
