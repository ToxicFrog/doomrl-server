self: super:

let
  # Download the amd64 LQ (low quality) version, since it doesn't need sound
  # for playing on the server.
  # TODO: wrapper script and desktop entry so local users can just run `doomrl`
  # and have it run out of ~/.local/DoomRL/ using the same techniques as the
  # server.
  # path = "32/doomrl-linux-x64-0997.tar.gz";
  # path = "33/doomrl-linux-i386-0997.tar.gz";
  path = "37/doomrl-linux-x64-0997-lq.tar.gz";
  # path = "38/doomrl-linux-i386-0997-lq.tar.gz";
  hash = "72a5951a94257a81b7e7792e9be4056e3a10d1c1ea91fa69f861701ea1067b0b";

in {
  doomrl = self.stdenv.mkDerivation {
    name = "doomrl";
    src = self.fetchurl {
      url = "https://doom.chaosforge.org/file_download/${path}";
      sha256 = hash;
    };

    libPath = self.stdenv.lib.makeLibraryPath [
      self.SDL
      self.xorg.libX11
      self.zlib
    ];

    phases = [ "unpackPhase" "installPhase" ];
    installPhase = ''
      mkdir -p "$out/opt/"
      cp -a . "$out/opt/doomrl"

      patchelf \
        --set-interpreter $(cat $NIX_CC/nix-support/dynamic-linker) \
        --set-rpath "$libPath" \
        "$out/opt/doomrl/doomrl"

      #mkdir -p "$out/bin"
      #ln -s "$out/opt/doomrl/doomrl" "$out/bin/"
    '';
  };
}
