{}:
let
  src = builtins.fetchGit {
    url = "git@github.com:cyraxjoe/maki.git";
    name = "maki-master";
    ref = "master";
  };
in (import "${src}" { }).app
