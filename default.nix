{ pkgs ? (import ./nixpkgs.nix {}).pkgs }:
let
  inherit(pkgs) poetry2nix;

  python = pkgs.python38;

  projectDir = ./.;

  overrides = poetry2nix.overrides.withDefaults (
    self: super: {
      # disable the removal of pyproject.toml, required because of setuptools_scm
      # in the following packages.
      jaraco-functools = super.jaraco-functools.overridePythonAttrs (
        old: {
          dontPreferSetupPy = true;
        }
      );

      tempora = super.tempora.overridePythonAttrs (
        old: {
          dontPreferSetupPy = true;
        }
      );

      portend = super.portend.overridePythonAttrs (
        old: {
          dontPreferSetupPy = true;
        }
      );

    }
  );

  app = poetry2nix.mkPoetryApplication {
    inherit python projectDir overrides;
  };

  env = poetry2nix.mkPoetryEnv {
    editablePackageSources = {
        maki = ./.;
    };
    inherit python projectDir overrides;
  };
in {
  app = app.dependencyEnv.overrideAttrs (
    old:  {
      name = "maki-${ app.version }";
    }
  );
  shell = pkgs.mkShell {
    buildInputs = [ env pkgs.glibcLocales ];
  };
}
