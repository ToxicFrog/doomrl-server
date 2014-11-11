# DoomRL-server

A nethack.alt.org-inspired frontend for hosting a multiplayer DoomRL server. Players have personal save files, ranks, and player stats, but there is a shared high score list and games can be viewed by spectators.

## Installation

Before you can run it, DoomRL-server has a number of requirements:

- Python 3.x
- `stty`
- `ttyrec`, `ttytime`, and `ttyplay`
- `reset`
- `less`
- `nano`
- and DoomRL itself.

`stty`, `nano` and `less` are commonly installed by default. `reset` is likely to be as well, and if not is generally part of curses (the `ncurses-utils` package on SUSE, for example). `ttyrec` may need to be specifically installed.

DoomRL should be unpacked into doomrl-server's `doomrl/` directory (so that `doomrl/doomrl` is the doomrl binary itself). The sound files are not used, so the "low-quality" version of DoomRL is sufficient.

DoomRL-server does no networking of its own; it expects to get user input via stdin and communicate with them via stdout. Thus, it is intended to be used as a user shell or as an inetd daemon.

In either case, it is recommended (as with any daemon that doesn't require special privileges) that you create a user for it:

    # useradd -g nobody -d /var/lib/doomrl -M -N -r -s /var/lib/doomrl/doomrl-server doomrl

You can then install doomrl-server to that user's home directory, unpack a fresh DoomRL install there, and set permissions appropriately:

    # git clone https://github.com/toxicfrog/doomrl-server /var/lib/doomrl
    # tar xzf doomrl-linux-x64-0997-lq.tar.gz --strip-components=1 -C /var/lib/doomrl/doomrl/
    # chown -R doomrl:nogroup /var/lib/doomrl

At this point, anyone logging as "doomrl" (for example, over telnet) will end up running the doomrl-server shell. If you would rather not permit this, you can also run it as an inetd service; a sample xinetd configuration file is provided as `doomrl-server.xinetd`. Note that the xinetd configuration uses telnetd to launch doomrl-server, as it handles setting up the terminal correctly; without this doomrl is unlikely to work.

## Configuration

There's not much to configure. It assumes that the directory containing the doomrl-server script is the root of the doomrl-server install; if this is incorrect, set the environment variable `DOOMRL_SERVER` appropriately.

Apart from that, the only thing to do is edit the DoomRL configuration files in `config/`; these override the default configs that come with DoomRL, which will be copied into each player's user directory. The default values should be fine, but you may want to look them over (for example, to enable a custom mod server). The `controls.lua`, `colours.lua`, and `user.lua` files are editable by the user via the `config` command; the `config.lua` file is appended to by doomrl-server at user registration time but otherwise static.

## Directories

    config/

Holds the configuration used by doomrl when launched via doomrl-server.

    doomrl/

Unpack a DoomRL installation to this directory. In combination with the config directories, it will be used as the basis for the per-player doomrl directories.

    players/*/

Each one of these is a player-specific DoomRL directory. Most of the contents are symlinks to files in the root doomrl directory. The exceptions are files generated or edited by DoomRL as it runs -- player.wad and score.wad, the backup/, mortem/, and screenshot/ directories, the save file, and log files. There is also a ttyrec/ directory used by DoomRL to store completed game recordings.

    games/

This holds information about games in progress. For each game there's a ttyrec file named for the player. If the player has a game in progress but is not currently playing, the file has a `.save` suffix.

## Future Work

Generation of a static web interface for high score lists and mortem/ttyrec files in `www/`.

## License

Copyright © 2014 Ben "ToxicFrog" Kelly
Distributed under the MIT License; see the file COPYING for details.

ASCII DOOM logo copyright © 1994 F.P. de Vries.
http://www.gamers.org/~fpv/doomlogo.html

## Disclaimer

This project is not affiliated in any way with Doom or DoomRL.
