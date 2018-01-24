# libttysound

This library provides experimental closed caption support to the tty version of DoomRL. It does this by replacing the SDL_mixer library, used for playing sound effects. In tty mode, it adds an additional line at the bottom showing what sounds you hear; in graphical mode, it changes the title bar to reflect what you hear.

It has only been tested on Linux. It might work on OSX (using `DYLD_LIBRARY_PATH`). The graphical mode might work on windows; the text mode probably won't without additional work.

There is currently no support for directionality and distance of sound, but this may be added in a future version.

## Prerequisites

- DoomRL, of course
- a C compiler, such as `gcc`
- `make`
- libSDL (both the library and header files)

## Installation.

- Install DoomRL wherever you please.

- Copy the following files and directories from the doomrl-server directory into your DoomRL install:
  - `ttysound/`
  - `config/cc/`
  - `config/soundcc.lua`

  You should end up with `soundcc.lua` and `cc/` in the same directory as `config.lua`, not in a `config/` subdirectory.

- Build the library:
  - `cd ttysound`
  - `make`

  If this works you should have a `ttysound/libttysound.so` file, and a `ttysound/libSDL_mixer-1.2.so.0` symlink pointing to it. The latter is what DoomRL will load.
- Edit `config.lua` and add the following lines *at the bottom*:
  ```
  ClosedCaptions = true
  ClosedCaptionStyle = 'fancy'
  NightmareClosedCaptionStyle = 'full'
  dofile 'soundcc.lua'
  ```
  It is important that they be in that order. (See `Settings` below for other possible values of `ClosedCaptionStyle` and `NightmareClosedCaptionStyle`.)

- Finally, launch DoomRL using one of the `ttysound/doomrl_cc` scripts rather than the ones that come with DoomRL. If you don't use those scripts, the environment variables you need to set for closed captions to work properly are:

  ```
  LD_LIBRARY_PATH=ttysound/
  SDL_AUDIODRIVER=disk
  SDL_DISKAUDIOFILE=/dev/null
  ```

  *Warning:* Unlike plain DoomRL, you require 80 columns and *26 rows* in the terminal for closed captions to display properly. If you aren't using one of the `doomrl_cc` scripts, make sure you adjust whatever you are using to take that into account.

  The `doomrl_cc_<terminal>` scripts will launch DoomRL in tty mode in the given terminal. The plain `doomrl_cc` script will launch it in whatever mode is the default (graphical or tty) in the current terminal; you can also override this with the `-console` and `-graphics` command line options, same as running DoomRL directly. The closed caption library will automatically detect whether you're running it in graphical or tty mode and adapt accordingly.

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
- `ClosedCaptionStyle = 'auto'` is equivalent to `'fancy'` if `Graphics = 'CONSOLE'` in your main configuration file, and equivalent to `'plain'` otherwise. Note that this is not 100% reliable -- if you are overriding the `Graphics` setting with the `-console` or `-graphics` command line options, *it won't know that*.

`'auto'` is the default.

### NightmareClosedCaptionStyle

Controls how sounds for Nightmare creature variants are displayed.

- `NightmareClosedCaptionStyle = 'full'` gives each nightmare creature its own set of captions.
- `NightmareClosedCaptionStyle = 'limited'` gives each nightmare creature the captions from the equivalent non-nightmare creature, so you can still "hear" them, but can't distinguish them from ordinary enemies.
- `NightmareClosedCaptionStyle = 'none'` makes nightmare creatures completely silent.

`'full'` is the default.

## Adding custom styles

The text displayed for each sound is stored in the `cc/` directory. Each sound is in its own file, in `cc/<CC style>/<creature type>/<event name>`. The contents of this file will be displayed without modification when the sound is played, including any formatting or colour codes.

Adding a new CC style is just a matter of adding a new directory under `cc/` containing the appropriate files. It is recommended that you start by copying an existing style (`cc/raw/` is a good choice) to make sure you don't miss any files. Make sure you also edit the start of `cc/config.lua`; the `styles` table at the start of the file determines which style names are recognized as valid.
