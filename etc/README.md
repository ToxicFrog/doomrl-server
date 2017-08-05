## doomrl-server configuration files

These are useful configuration files for doomrl-server related services. Note that most of them require some editing for your specific setup.

    doomrl-server-service.nix
    doomrl-server.nix
    doomrl.nix

NixOS configuration file and package overlays for doomrl-server.

    doomrl-server.conf

Sample configuration file. Copy to `/etc/doomrl-server.conf`.

    doomrl-server.xinetd

xinetd service configuration for doomrl-server over telnet.

    nginx-domrl-server.conf

nginx configuration file for serving the web scoreboard and client.

    thttpd.conf
    thttpd-doomrl.service

thttpd configuration file and unit file, if you'd rather use thttpd than nginx.

    websockify-doomrl.service

systemd unit file for websockify, for the web client.
