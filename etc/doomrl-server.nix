self: super:

let
  server-path = "/srv/doomrl";
in {
  doomrl-server = self.stdenv.mkDerivation {
    name = "doomrl-server";
    src = self.fetchFromGitHub {
      owner = "toxicfrog";
      repo = "doomrl-server";
      rev = "e81178c05af3f8878592704231eb90a7e55c7fb1";
      sha256 = "111p1l8266dbxcvazqhgfxravg0kzdff3c75qjdisakxybjf7jnq";
    };

    nativeBuildInputs = with self; [gnumake git lua5_3];
    buildInputs = with self; [SDL];
    deps = with self; [python3 telnet less ncurses nano];

    phases = [ "unpackPhase" "buildPhase" "installPhase" ];

    buildPhase = ''make -C ttysound DRL_SOUND_CONFIG=${self.doomrl}/opt/doomrl/soundhq.lua'';
    installPhase = ''
      mkdir -p "$out/share"
      cp -a . "$out/share/doomrl-server"
      mkdir -p "$out/share/doomrl-server/www/sfx/"
      for sfx in ${self.doomrl}/opt/doomrl/wavhq/*.wav; do
        flac="$(${self.coreutils}/bin/basename "$sfx" | ${self.gnused}/bin/sed -E "s,wav$,flac,")"
        ${self.ffmpeg}/bin/ffmpeg -hide_banner -loglevel error -i "$sfx" "$out/share/doomrl-server/www/sfx/$flac"
      done
      ln -s ${self.doomrl}/opt/doomrl/mp3 "$out/share/doomrl-server/www/music"
    '';
  };
}
