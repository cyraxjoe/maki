{ }:
let
  sources = import ./nix/sources.nix {};
  pkgs = import sources.nixpkgs {};
  poetry2nix = pkgs.callPackage sources.poetry2nix { inherit pkgs; } ;
  python = pkgs.python310;
  projectDir = ./.;
  app = (poetry2nix.mkPoetryApplication {
    inherit python projectDir;
    # creat a symlink for a constant path for the static files (in case that we change python versions)
    postInstall = ''
       mkdir -p  $out/var/lib/static
       ln -s $out/lib/${ python.libPrefix }/site-packages/maki/static  $out/var/lib/static/maki
    '';
  }).dependencyEnv.overrideAttrs (old: {name = "maki-0.4.0"; });
  env = poetry2nix.mkPoetryEnv {
    editablePackageSources = {
        maki = ./.;
    };
    inherit python projectDir;
  };
in {
  inherit app env;
  shell = pkgs.mkShell { buildInputs = [ env pkgs.glibcLocales ]; };
}
