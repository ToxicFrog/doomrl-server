self: super:

let
  server-path = "/srv/doomrl";
in {
  doomrl-server = self.stdenv.mkDerivation {
    name = "doomrl-server";
    src = self.fetchFromGitHub {
      owner = "toxicfrog";
      repo = "doomrl-server";
      rev = "368c685f35850e86261c891b2e73a680e8077eb4";
      sha256 = "1cfp1l8266dbxcvazqhgfxravg0kzdff3c75qjdisakxybjf7jnq";
    };

    nativeBuildInputs = with self; [gnumake];
    buildInputs = with self; [SDL];
    deps = with self; [python3 telnet less];

    phases = [ "unpackPhase" "buildPhase" "installPhase" ];

    buildPhase = ''make -C ttysound'';
    installPhase = ''
      # ls -ltrAh
      # pwd
      # echo "out=$out"
      # stat $out
      mkdir -p $out/share/
      cp -a . "$out/share/doomrl-server"
    '';
  };
}
