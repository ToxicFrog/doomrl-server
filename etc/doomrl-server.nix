self: super:

let
  server-path = "/srv/doomrl";
in {
  doomrl-server = self.stdenv.mkDerivation {
    name = "doomrl-server";
    src = self.fetchFromGitHub {
      owner = "toxicfrog";
      repo = "doomrl-server";
      rev = "master";
      sha256 = "X8fqk2v02rd7jb8fpxk4ab7c7zzrpvdnc7iklmx71pa8bd3x1kqz";
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
