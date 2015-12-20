# libttysound

This library provides experimental subtitle support to the tty version of DoomRL. It does this by replacing the SDL_mixer library; instead of playing the sounds, it displays text on screen describing them.

It does not support the graphical version of DoomRL. It has only been tested on Linux. It might work on OSX (using `DYLD_LIBRARY_PATH`). It probably won't work on windows without additional work.

## Prerequisites

- DoomRL, of course
- a C compiler, such as `gcc`
- `make`
- libSDL (but note that you don't need the SDL headers, or SDL_mixer)

## Installation.

- Install DoomRL wherever you please.
- Copy the following files and directories from the doomrl-server directory into your DoomRL install:
  - `ttysound/`
  - `config/cc/`
  - `config/soundcc.lua`
  - `doomrl_cc_*`

  You should end up with `soundcc.lua` and `cc/` in the same directory as `config.lua`, not in a `config/` subdirectory.
- Build the subtitle library:
  - `cd ttysound`
  - `make`

  If this works you should have a `ttysound/libttysound.so` file, and a `ttysound/libSDL_mixer-1.2.so.0` symlink pointing to it. The latter is what DoomRL will load.
- Edit `config.lua` and add the following lines *at the bottom*:
  - `DeafMode = "symbolic"`
  - `dofile "soundcc.lua"`

  It is important that they be in that order. (See `Settings` below for other possible values of `DeafMode`.)
- Finally, launch DoomRL using one of the `doomrl_cc` scripts rather than the ones that come with DoomRL. If you don't use those scripts, the environment variables you need to set for subtitles to work properly are:

  ```
  LD_LIBRARY_PATH=ttysound/
  SDL_AUDIODRIVER=disk
  SDL_DISKAUDIOFILE=/dev/null
  ```

  *Warning:* Unlike plain DoomRL, you require 80 columns and *26 rows* in the terminal for subtitles to display properly. If you aren't using one of the `doomrl_cc` scripts, make sure you adjust whatever you are using to take that into account.

## Settings

The only configuration possible is whether to use subtitles or not at all, and what style to display them in.

To turn them off completely, simply set `SoundEngine = "NONE"` in the configuration file.

To change the style, change the value of the `DeafMode` setting. At the moment there are three supported styles:

- `"symbolic"`, the default, displays 1-3 character symbols based on the existing monster symbols and visual effects.
- `"plain-symbolic"` is identical to `"symbolic"`, but without colour codes; it's suitable for use in the title bar of the graphical version of DoomRL.
- `"default"` is an alias for `"symbolic"`.
- `"raw"` displays raw event names.
- `"descriptive"` will someday display lengthier, Nethack-style sound descriptions (e.g. "You hear: a clanking noise | a distant scream | an explosion"), but it's still a work in progress and at the moment behaves identically to `"raw"`.

Any unrecognized setting will result in subtitles being disabled.
