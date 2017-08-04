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
  - `DeafMode = "symbolic"`
  - `dofile "soundcc.lua"`

  It is important that they be in that order. (See `Settings` below for other possible values of `DeafMode`.)
- Finally, launch DoomRL using one of the `ttysound/doomrl_cc` scripts rather than the ones that come with DoomRL. If you don't use those scripts, the environment variables you need to set for closed captions to work properly are:

  ```
  LD_LIBRARY_PATH=ttysound/
  SDL_AUDIODRIVER=disk
  SDL_DISKAUDIOFILE=/dev/null
  ```

  *Warning:* Unlike plain DoomRL, you require 80 columns and *26 rows* in the terminal for closed captions to display properly. If you aren't using one of the `doomrl_cc` scripts, make sure you adjust whatever you are using to take that into account.

  The `doomrl_cc_<terminal>` scripts will launch DoomRL in tty mode in the given terminal. The plain `doomrl_cc` script will launch it in whatever mode is the default (graphical or tty) in the current terminal; you can also override this with the `-console` and `-graphics` command line options, same as running DoomRL directly. The closed caption library will automatically detect whether you're running it in graphical or tty mode and adapt accordingly.

## Settings

The only configuration possible is whether to use closed captions or not at all, and what style to display them in.

To turn them off completely, simply set `DeafMode = false` in the configuration file.

To change the style, change the value of the `DeafMode` setting. Currently, the following styles are supported:

- `"symbolic"`, the default, displays 1-3 character symbols based on the existing monster symbols and visual effects.
- `"plain-symbolic"` is identical to `"symbolic"`, but without colour codes; it's suitable for use in the title bar of the graphical version of DoomRL.
- `"default"` and `"tty"` are aliases for `"symbolic"`.
- `"titlebar"` and `"sdl"` are aliases for `"plain-symbolic"`.
- `"raw"` displays raw event names.
- `"descriptive"` will someday display lengthier, Nethack-style sound descriptions (e.g. "You hear: a clanking noise, a distant scream, an explosion"), but it's still a work in progress and at the moment behaves identically to `"raw"`.

Any unrecognized setting will result in closed captions being disabled.

## Adding custom styles

The text displayed for each sound is stored in the `config/cc/` directory (`cc/` once installed). Each sound is in its own file, in `config/cc/<CC style>/<creature type>/<event name>`. The contents of this file will be displayed without modification when the sound is played, including any formatting or colour codes.

Adding a new CC style is just a matter of adding a new directory under `cc/` containing the appropriate files. It is recommended that you start by copying an existing style (`cc/raw/` is a good choice) to make sure you don't miss any files. Make sure you also edit the start of `soundcc.lua`; the `styles` table at the start of the file determines which style names are recognized as valid.
