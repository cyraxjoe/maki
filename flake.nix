{
  description = "Maki — the blogging engine behind blog.joel.mx";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
      ...
    }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
      overlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };

      mkPythonSet =
        pkgs:
        (pkgs.callPackage pyproject-nix.build.packages {
          python = pkgs.python313;
        }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay
            ]
          );
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonSet = mkPythonSet pkgs;
          venv = pythonSet.mkVirtualEnv "maki-env" workspace.deps.default;
          maki = pkgs.symlinkJoin {
            name = "maki-${pythonSet.maki.version}";
            paths = [ venv ];
            # Stable path to the static files for the web server config,
            # independent of the python version inside the venv.
            postBuild = ''
              mkdir -p $out/var/lib/static
              ln -s ${venv}/${pkgs.python313.sitePackages}/maki/static \
                    $out/var/lib/static/maki
            '';
          };
        in
        {
          inherit maki;
          default = maki;
        }
      );

      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          # Impure uv-managed shell: uv creates/updates .venv from uv.lock.
          default = pkgs.mkShell {
            packages = [
              pkgs.python313
              pkgs.uv
            ] ++ lib.optionals pkgs.stdenv.isLinux [ pkgs.glibcLocales ];
            env = {
              UV_PYTHON = pkgs.python313.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
            };
          };
        }
      );
    };
}
