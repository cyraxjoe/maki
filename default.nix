{ }:
let
  pkgs = import <nixpkgs> {};
  python = import ./requirements.nix { inherit pkgs; };
  cherryPy = python.packages."CherryPy";
  inherit(pkgs) makeWrapper;
  inherit(python.__old)  buildPythonApplication;
in buildPythonApplication {
  name = "maki";
  doCheck = false;
  src = ./.;
  buildInputs = [ makeWrapper ];
  postInstall = ''
     echo "post install"
     mkdir -p $out/bin
     makeWrapper "${ cherryPy }/bin/cherryd"  $out/bin/cherryd --prefix PYTHONPATH : "$PYTHONPATH"
  '';
  propagatedBuildInputs = builtins.attrValues python.packages;
}
