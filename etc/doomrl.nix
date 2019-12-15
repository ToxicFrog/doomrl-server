self: super:

let
  # TODO: wrapper script and desktop entry so local users can just run `doomrl`
  # and have it run out of ~/.local/DoomRL/ using the same techniques as the
  # server.
  path = "32/doomrl-linux-x64-0997.tar.gz";
  # path = "33/doomrl-linux-i386-0997.tar.gz";
  # path = "37/doomrl-linux-x64-0997-lq.tar.gz";
  # path = "38/doomrl-linux-i386-0997-lq.tar.gz";
  hash = "127407ssykmnwq6b0l3kxrxvpbgbhwcy3cv3771b7vwlhx59xlfr";
in {
  doomrl = self.stdenv.mkDerivation {
    name = "doomrl";
    src = self.fetchurl {
      url = "https://drl.chaosforge.org/file_download/${path}";
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
    '';
  };
}
