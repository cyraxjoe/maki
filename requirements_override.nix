{ pkgs, python }:

self: super: {
  "pytest-runner" = python.overrideDerivation super."pytest-runner" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "textile" = python.overrideDerivation super."textile" (old: {
    buildInputs = old.buildInputs ++ [ self."pytest-runner" self."setuptools-scm" ];
  });

  "CherryPy" = python.overrideDerivation super."CherryPy" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "psycopg2" = python.overrideDerivation super."psycopg2" (old: {
    nativeBuildInputs = [ pkgs.postgresql ];
  });
}
