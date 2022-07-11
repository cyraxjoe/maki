{ }:
let
  sources = import ./nix/sources.nix {};
  pkgs = import sources.nixpkgs {};
  poetry2nix = pkgs.callPackage sources.poetry2nix { inherit pkgs; } ;
  python = pkgs.python310;
  projectDir = ./.;
  app = poetry2nix.mkPoetryApplication {
    inherit python projectDir;
  };
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
