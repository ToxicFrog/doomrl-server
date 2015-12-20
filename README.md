# DoomRL-server

A nethack.alt.org-inspired frontend for hosting a multiplayer DoomRL server. Players have personal save files, ranks, and player stats, but there is a shared high score list and games can be viewed by spectators.

It has optional support for a web-based scoreboard and subtitles, too.

## Installing doomrl-server

Before you can run it, DoomRL-server has a number of requirements:

- Python 3.3+
- `ttyrec`, `ttytime`, and `ttyplay`
- `reset`
- `less`
- `nano`
- and DoomRL itself.

Python, `nano`, and `less` are commonly installed by default. `reset` is likely to be as well, and if not is generally part of curses (the `ncurses-utils` package on SUSE, for example). `ttyrec` may need to be specifically installed.

DoomRL should be unpacked into doomrl-server's `doomrl/` directory (so that `doomrl/doomrl` is the doomrl binary itself). The sound files are not used, so the "low-quality" version of DoomRL is sufficient.

DoomRL-server does no networking of its own; it expects to get user input via stdin and communicate with them via stdout. Thus, it is intended to be used as a user shell or as an inetd daemon.

In either case, it is recommended (as with any daemon that doesn't require special privileges) that you create a user for it:

    # useradd -g nobody -d /var/lib/doomrl -M -N -r -s /var/lib/doomrl/doomrl-server doomrl

You can then install doomrl-server to that user's home directory, unpack a fresh DoomRL install there, and set permissions appropriately:

    # git clone https://github.com/toxicfrog/doomrl-server /var/lib/doomrl
    # tar xzf doomrl-linux-x64-0997-lq.tar.gz --strip-components=1 -C /var/lib/doomrl/doomrl/
    # chown -R doomrl:nogroup /var/lib/doomrl

At this point, anyone logging as "doomrl" (for example, over telnet) will end up running the doomrl-server shell. If you would rather not permit this, you can also run it as an inetd service; a sample xinetd configuration file is provided as `doomrl-server.xinetd`. Note that the xinetd configuration uses telnetd to launch doomrl-server, as it handles setting up the terminal correctly; without this doomrl is unlikely to work.

### Configuration

doomrl-server assumes that the directory containing the `doomrl-server` script is the root of the doomrl-server install; if this is incorrect, set the environment variable `DOOMRL_SERVER` appropriately.

The DoomRL configuration files are located in `config/`; these override the default configs that come with DoomRL, which will be copied into each player's user directory. The default values should be fine, but you may want to look them over (for example, to enable a custom mod server). The `controls.lua`, `colours.lua`, and `user.lua` files are editable by the user via the `config` command; the `config.lua` file is appended to by doomrl-server at user registration time but otherwise static. Other files in that directory (such as `soundcc.lua`) are not user editable.


## Enabling subtitle support

`doomrl-server` supports subtitles, via loading a custom audio library. This support is automatically activated if the library is present. The library is included in the doomrl-server distribution.

To build it, you'll need a C compiler and `make` installed. (It has no library dependencies). Once you have those:

    $ cd ttysound; make

No further setup is needed (but some configuration settings are available; see below).

For information on using subtitle support stand-alone (i.e. not as part of doomrl-server), see `ttysound/README.md`.

### Configuration

In the config files that ship with doomrl-server, subtitle support, if available, is activated via the `DeafMode` setting (by analogy to `ColorBlindMode`). Setting it to `"raw"` or `"symbolic"` will enable different representations of sound. Setting it to `"default"` will select the default setting for this server. Any other value will disable subtitles.

To change the default setting for new users, edit `user.lua`. To change the default setting for this server (i.e. what users get when they select `"default"`), edit `soundcc.lua`.

If you want to change the way sounds are actually displayed in game, the subtitle files are in `config/cc`. Each sound is in its own file, in `config/cc/<subtitle type>/<creature type>/<event name>`. If you want to add a completely new subtitle type, make sure to also edit `soundcc.lua` -- the first few lines are what determine which subtitle types are recognized as valid.


## Web Scoreboard

After every completed game (successful or otherwise :), doomrl-server updates a static web scoreboard in `www/`. This site lists scores (both overall and per player) and allows people to download mortem files and ttyrecs. doomrl-server doesn't serve the scoreboard; it's up to you to provide the web server. Sample configuration files for thttpd are provided.

### Configuration

The scoreboard homepage is prefaced with the contents of the `webmotd` file. You may want to edit this to include things like the name of your server and a `telnet://` link to the actual doomrl-server instance.

If you're using thttpd as the web server, sample configuration files are also provided. `thttp.conf` is the configuration file for the web server itself; `thttpd-doomrl.service` is a systemd service file for running it. You should read and edit both of them, as they make some assumptions that may not be correct (for example, they assume that doomrl-server is installed in `/var/lib/doomrl/`, and that you want to serve the scoreboard on port 8666).


## Directories

    config/

Holds the configuration used by doomrl when launched via doomrl-server.

    doomrl/

Unpack a DoomRL installation to this directory. In combination with the config directories, it will be used as the basis for the per-player doomrl directories.

    players/*/

Each one of these is a player-specific DoomRL directory. Most of the contents are symlinks to files in the root doomrl directory, or (for files that DoomRL writes, or that the player can customize) copies of same.

    players/*/saves/

Games in progress, each one named for that game.

    players/*/archive/

Archived mortem and ttyrec files and the server scores file for that player.

    games/

This holds information about games in progress. For each game there's a ttyrec file named for the player. If the player has a game in progress but is not currently playing, the file has a `.<name>` suffix, where `name` is the name given to that game by the player.

    www/

Holds the static web scoreboard. Regenerated every time a game is finished.

## Special files

    players/*

If a file exists in the players directory, it will block players of that name from being created. The server comes with a `guest` file.

    motd

The contents if this file, if present in the root directory of the server, will be displayed to each user upon connection. The default contains a DOOM banner.

    maintenance

If this file exists in the root directory of the server, new connections will be shown its contents and then disconnected; existing connections will be treated similarly after their current command completes. Note that the 'current command' may take a very long time to complete, if the user is playing DoomRL or watching a long replay (or has gone AFK); don't expect this to get all users off the server promptly. (To return to normal operation, just delete or rename the file).

    debug

If a file named `debug` exists in a *player's* directory, that player has debug privileges: they will see full stack traces and debug messages from the server. If such a file exists in the *server's* root directory, all players have debug privileges.

## Importing scores from offline

DoomRL-server doesn't read the score.wad file directly; rather, after each game, it extracts the scoreline for that game, adds some additional info to it, and stores in in `players/$PLAYER/archive/scores`. Similarly, postmortems are renamed to make them easier for the server to find. Thus, importing a player is a bit more complicated than just copying the files into place; to automate this, the `import-player` script is available.

To use it, register the player, and then, *from the root of your doomrl-server install*, run `import-player <name> <player.wad> <score.wad> <mortem/>`. The `player.wad` file is the only mandatory part, and contains user progression, unlock and achievement information. `score.wad` contains the player's high score list. `mortem/` can only be imported if `score.wad` is as well, and will attempt to import all of the mortem files and match them up with high score list entries.

In the latter case, it may not always be able to narrow it down to a single high score entry. In that case, you will get a `writing duplicate scorelines, please edit and correct` message. Open the `players/<name>/archive/scores` file, find the duplicate entries, and read the corresponding mortem files to figure out which is the correct one (if possible) and delete the rest.

## Future Work

`wins` command to list winning games only.

Archive ttyrecs compressed and decompress on demand.

Let players upload and download their score.wad/player.wad/mortem files without admin intervention.

"There are %d other players online" banner?

## License

Copyright © 2014 Ben "ToxicFrog" Kelly
Distributed under the MIT License; see the file COPYING for details.

ASCII DOOM logo copyright © 1994 F.P. de Vries.
http://www.gamers.org/~fpv/doomlogo.html

## Disclaimer

This project is not affiliated in any way with Doom or DoomRL.
