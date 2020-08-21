{}:
let
  src = builtins.fetchGit {
    name = "nixpkgs-unstable-2020-08-20";
    url = https://github.com/nixos/nixpkgs-channels;
    ref = "nixos-unstable";
    # rev for nixos-unstable as of 2020-08-20
    # `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
    rev = "1e3f09feaa5667be4ed6eca96a984b4642420b83";
  };
  pkgs = import "${ src }" {};
in
  { inherit src pkgs; }
