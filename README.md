# DoomRL-server

A `nethack.alt.org`-inspired frontend for hosting a multiplayer DoomRL server. Features:

- per-player game settings, save files, and unlocks
- multiple save files per player
- shared scoreboard
- games in progress can be spectated
- mortems and recordings of finished games are saved for later viewing
- closed caption support (also usable without the server; see `ttysound/README.md`)
- a web interface that lets people view the scoreboard, spectate, and even play the game from their browser



## Installing doomrl-server

If you're running NixOS, there are overlays and a service configuration in `etc/`. See `etc/README.md` for details.

If you aren't, read on.

`doomrl-server` expects to run as a user shell or inetd service, getting input on stdin and replying on stdout; it contains no netcode and doesn't run as a daemon. The easiest configuration is just to create a `doomrl` user with `doomrl-server` as the shell, then set up something that lets people log in as that user (using passwordless ssh, perhaps). If you want to get more complicated you can add telnet support (via `xinetd`) and even a web client (which requires telnet support set up), which probably has the lowest barrier to entry for users.

Throughout these instructions I'm going to assume that:
- you want DoomRL installed in /opt/doomrl, and doomrl-server in /usr/src/doomrl-server
- you want doomrl-server user data stored in /srv/doomrl
- you're using nginx as the web server and systemd as your init system

### Prerequisites

- DoomRL
- `python3`, `less`, and `nano`
- `xinetd` and `telnetd` (for telnet access)
- a simple static web server like `nginx` (for the web scoreboards)
- `websockify` (for the web client)

Most of these you should be able to install with your package manager. DoomRL you can [download from chaosforge](https://drl.chaosforge.org/downloads). Go ahead and unpack it to `/opt/doomrl`:

    $ mkdir /opt/doomrl
    $ curl https://drl.chaosforge.org/file_download/37/doomrl-linux-x64-0997-lq.tar.gz \
        | tar xz --strip-components=1 -C /opt/doomrl

We use the LQ (Low Quality) version here because the server doesn't play music, and thus doesn't need the extra ~100MB of soundtrack. The `--strip-components` results in DoomRL being unpacked directly into `/opt/doomrl`, i.e. the game binary is `/opt/doomrl/doomrl`, not `/opt/doomrl/doomrl-linux-x64-0997-lq/doomrl`.

### Using it as a shell

Just download doomrl-server:

    $ git clone https://github.com/toxicfrog/doomrl-server /usr/src/doomrl-server

Create a user for it:

    $ useradd -g nobody -d /srv/doomrl -M -N -r -s /usr/src/doomrl-server doomrl
    $ chown -R doomrl:nogroup /srv/doomrl

And set up the configuration file, editing it if necessary:

    $ cp /usr/src/doomrl-server/etc/doomrl-server.conf /etc
    $ nano /etc/doomrl-server.conf

And you're done! Anyone logging in as `doomrl` will run the doomrl server as their shell. `/srv/doomrl` will be created, if it doesn't already exist, the first time the server runs. You should be able to test this with `sudo -u doomrl /usr/src/doomrl-server/doomrl-server` -- it should give you a DooM banner and a `guest>` prompt.

### Setting up telnet access

It's convenient if users can just `telnet yourserver.net 3666` and play doomrl. For this we use xinetd (to accept the connection) and telnetd (to perform initial negotiation and set up the terminal).

There's an xinetd configuration file in `etc/`, so this is probably as simple as:

    $ cp /usr/src/doomrl-server/etc/doomrl-server.xinetd /etc/xinetd.d
    $ nano /etc/xinetd.d/doomrl-server.xinetd
    $ systemctl restart xinetd

Test it with `telnet localhost 3666` (assuming you haven't edited the port) and you should get the banner and guest prompt as before.

### Setting up the web server

doomrl-server writes HTML scoreboards and postmortems to `$user_dir/www/`. These are static HTML (+ a bit of javascript) and require no server-side support; you can just point anything that can serve static HTML at them and away it goes. Sample configurations are provided in `etc/` for nginx and thttpd.

### Setting up the web client

The web client is automatically included in the generated HTML. For it to work, you need to run `websockify` to connect a websocket to the doomrl-server xinetd service; as with nginx, there's a sample service configuration (`etc/websockify-doomrl.service`).

If you're running doomrl-server telnet and websocket on ports other than the default (3666 and 3667 respectively), in addition to editing the websockify service file, you'll need to edit `DOOMRL_WS_PORT` in `www/replay.html` and `www/tty.html`.



## Configuring doomrl-server

doomrl-server doesn't have much configuration except the paths contained in `/etc/doomrl-server.conf`. What it does have is read from `$user_path` if it exists, and from `$data_path` otherwise -- so you can override the defaults that come with doomrl-server by creating files in `$user_path`.

### Banners

The `motd` and `webmotd` files contain the banners printed when a user logs in over telnet (or using the web client) and when a user views the scoreboard in their browser, respectively. The default banner is just a DooM logo and links to the DoomRL and doomrl-server websites. You can customize these for your site by creating `/srv/doomrl/motd` and `/srv/doomrl/webmotd` files containing the banners you want.

### Maintenance and debug mode

If want to temporarily bring the server down for maintenance, creating the file `/srv/doomrl/maintenance` will prevent new connections, instead printing the contents of the file and disconnecting the user. Note that this will *not* disconnect currently playing users.

The file `/srv/doomrl/debug`, if it exists, will put the server in debug mode. Mostly, this just means if something goes wrong, the user will get a full stack trace. You can also create the file `/srv/doomrl/players/<player name>/debug` to enable debug mode only for some players.

The `rebuild` command (which forces an immediate rebuild of the web scoreboard) is also limited to users with debug privileges.

### DoomRL configuration files

DoomRL configuration files are located in `/usr/src/doomrl-server/config/`. Of these, the files `controls.lua`, `colours.lua`, and `user.lua` are copied at player registration time and can be edited by the player afterwards; the other files are read-only. The defaults should be fine for most purposes, but you might want to edit them to, say, enable a custom mod server.

If you want to override any of these files, you need to copy *the entire `config/` directory* into `/srv/doomrl`; copying just some of the files will break user registration.

TODO: instructions on regenerating user symlinks when you move configuration files around.

### Closed captions

`doomrl-server` supports closed captions, via loading a custom audio library. This support is automatically activated if the library is present. The library is included in the doomrl-server distribution.

To build it, you'll need a C compiler, `make`, and `libSDL` (including the development headers) installed. Once you have those, just `make -C /usr/src/doomrl-server/ttysound` and it'll build the library. To remove it, `rm /usr/src/doomrl-server/ttysound/libttysound.so`.

No further setup is needed (but some configuration settings are available; see below).

For information on using closed caption support stand-alone (i.e. not as part of doomrl-server), see `ttysound/README.md`.

#### Configuration

In the config files that ship with doomrl-server, CC support, if available, is activated via the `DeafMode` setting (by analogy to `ColorBlindMode`). Setting it to `"default"` will select the default setting for this server. Other values select different CC styles or disable CC entirely.

To change the default setting for new users, edit `user.lua`. To change the default setting for this server (i.e. what users get when they select `"default"`), edit `soundcc.lua`.

For more information on valid values for `DeafMode` and adding or editing CC styles, see `ttysound/README.md`


## Directory layout

    $data_path/config/
    $user_path/config/

Holds the configuration used by doomrl when launched via doomrl-server.

    $user_path/players/*/

Each one of these is a player-specific DoomRL directory. Most of the contents are symlinks to files in `$data_path` and `$doom_path`.

    $user_path/players/*/saves/

Games in progress, each one named for that game.

    $user_path/players/*/archive/

Archived mortem and ttyrec files and the server scores file for that player.

    $user_path/www/

Holds the static web scoreboard. Regenerated every time a game is finished.



## Importing scores from offline

DoomRL-server doesn't read the score.wad file directly; rather, after each game, it extracts the scoreline for that game, adds some additional info to it, and stores in in `players/$PLAYER/archive/scores`. Similarly, postmortems are renamed to make them easier for the server to find. Thus, importing a player is a bit more complicated than just copying the files into place; to automate this, the `import-player` script is available.

To use it, register the player, and then, *from the root of your doomrl-server install*, run `import-player <name> <player.wad> <score.wad> <mortem/>`. The `player.wad` file is the only mandatory part, and contains user progression, unlock and achievement information. `score.wad` contains the player's high score list. `mortem/` can only be imported if `score.wad` is as well, and will attempt to import all of the mortem files and match them up with high score list entries.

In the latter case, it may not always be able to narrow it down to a single high score entry. In that case, you will get a `writing duplicate scorelines, please edit and correct` message. Open the `players/<name>/archive/scores` file, find the duplicate entries, and read the corresponding mortem files to figure out which is the correct one (if possible) and delete the rest.



## Future Work

`wins` command to list winning games only.

Archive ttyrecs compressed and decompress on demand.

Let players upload and download their score.wad/player.wad/mortem files without admin intervention.

"There are %d other players online" banner?

Properly handle OSError when (e.g.) playing ttyrecs, since sometimes we see that before we see the SIGHUP from the user disconnecting.

`savescum` command to restore old save files (probably marking those games non-scoring or storing them in a separate scores file).

Sound support in the web client: stream music and sound effects to the browser, either by generating an actual audio stream, or by sending the browser links to mp3 or ogg files to play in TTY comments (i.e. ESC ] 5 0 ; # + <comment text> ESC) -- the latter has the advantage that it'll be recorded in the ttyrec and can thus be replayed in a sound-capable terminal.



## License

Copyright © 2014 Ben "ToxicFrog" Kelly
Distributed under the MIT License; see the file COPYING for details.

ASCII DOOM logo copyright © 1994 F.P. de Vries.
http://www.gamers.org/~fpv/doomlogo.html



## Disclaimer

This project is not affiliated in any way with Doom or DoomRL.
