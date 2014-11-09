# DoomRL-server

A nethack.alt.org-inspired frontend for hosting a multiplayer DoomRL server. Players have personal save files, ranks, and player stats, but there is a shared high score list and games can be viewed by spectators.

## Directories

    config/

Holds the configuration used by doomrl when launched via doomrl-server.

    doomrl/

Unpack a DoomRL installation to this directory.

    players/*/

Each one of these is a player-specific DoomRL directory. Most of the contents are symlinks to files in the root doomrl directory. The exceptions are files generated or edited by DoomRL as it runs -- player.wad and score.wad, the backup/, mortem/, and screenshot/ directories, the save file, and log files. There is also a ttyrec/ directory used by DoomRL to store completed game recordings.

    games/

This holds information about games in progress. For each game there's a ttyrec file named for the player. If the player has a game in progress but is not currently playing, the file has a `.save` suffix.

## License

Copyright © 2014 Ben "ToxicFrog" Kelly
Distributed under the MIT License; see the file COPYING for details.

ASCII DOOM logo copyright © 1994 F.P. de Vries.
http://www.gamers.org/~fpv/doomlogo.html

## Disclaimer

This project is not affiliated in any way with Doom or DoomRL.
