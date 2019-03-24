# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix --default-overrides --python-version 3.6 -r requirements.txt -E postgresql
#

{ pkgs ? import <nixpkgs> {}
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python36;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            sed -i               -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"                  $out/${pkgs.python35.sitePackages}/pip/req/req_install.py
          '';
        });
      };
  };

  commonBuildInputs = with pkgs; [ postgresql ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreter = pythonPackages.buildPythonPackage {
        name = "python36-interpreter";
        buildInputs = [ makeWrapper ] ++ (builtins.attrValues pkgs);
        postBuild = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter}               $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "               (builtins.attrValues pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -f $prog ]; then
                  ln -s $prog $out/bin/`basename $prog`
                fi
              done
            fi
          done
          for prog in "$out/bin/"*; do
            wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
          done
          pushd $out/bin
          ln -s ${pythonPackages.python.executable} python
          ln -s ${pythonPackages.python.executable}               python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };
    in {
      __old = pythonPackages;
      inherit interpreter;
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs //                                            { meta = drv.meta; });
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {

    "CherryPy" = python.mkDerivation {
      name = "CherryPy-7.1.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ae/0a/1e47566e3e63142f1c676221f0e9ce41d4045773af98cb6b206b366702cc/CherryPy-7.1.0.tar.gz"; sha256 = "64dca80ccadae4ed8e4ea94119bf76ed9746743c2bd57ec40af534680cbef021"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.cherrypy.org";
        license = licenses.bsdOriginal;
        description = "Object-Oriented HTTP framework";
      };
    };



    "Mako" = python.mkDerivation {
      name = "Mako-1.0.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/7a/ae/925434246ee90b42e8ef57d3b30a0ab7caf9a2de3e449b876c56dcb48155/Mako-1.0.4.tar.gz"; sha256 = "fed99dbe4d0ddb27a33ee4910d8708aca9ef1fe854e668387a9ab9a90cbf9059"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."MarkupSafe"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.makotemplates.org/";
        license = licenses.mit;
        description = "A super-fast templating language that borrows the  best ideas from the existing templating languages.";
      };
    };



    "MarkupSafe" = python.mkDerivation {
      name = "MarkupSafe-0.23";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/c0/41/bae1254e0396c0cc8cf1751cb7d9afc90a602353695af5952530482c963f/MarkupSafe-0.23.tar.gz"; sha256 = "a4ec1aff59b95a14b45eb2e23761a0179e98319da5a7eb76b56ea8cdc7b871c3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/markupsafe";
        license = licenses.bsdOriginal;
        description = "Implements a XML/HTML/XHTML Markup safe string for Python";
      };
    };


    "Pygments" = python.mkDerivation {
      name = "Pygments-2.1.3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/b8/67/ab177979be1c81bc99c8d0592ef22d547e70bb4c6815c383286ed5dec504/Pygments-2.1.3.tar.gz"; sha256 = "88e4c8a91b2af5962bfa5ea2447ec6dd357018e86e94c7d14bd8cacbc5b55d81"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pygments.org/";
        license = licenses.bsdOriginal;
        description = "Pygments is a syntax highlighting package written in Python.";
      };
    };



    "SQLAlchemy" = python.mkDerivation {
      name = "SQLAlchemy-1.0.14";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/aa/cb/e3990b9da48facbe48b80a281a51fb925ff84aaaca44d368d658b0160fcf/SQLAlchemy-1.0.14.tar.gz"; sha256 = "da4d1a39c1e99c7fecc2aaa3a050094b6aa7134de7d89f77e6216e7abd1705b3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.sqlalchemy.org";
        license = licenses.mit;
        description = "Database Abstraction Library";
      };
    };



    "Unidecode" = python.mkDerivation {
      name = "Unidecode-0.4.19";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/5a/73/053be0fafe387d41ce705585412808093f5a333aaa71cabbab641f677c11/Unidecode-0.04.19.tar.gz"; sha256 = "51477646a9169469e37e791b13ae65fcc75b7f7f570d0d3e514d077805c02e1e"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "";
        license = licenses.gpl2Plus;
        description = "ASCII transliterations of Unicode text";
      };
    };



    "atomize" = python.mkDerivation {
      name = "atomize-0.2.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/e3/8a/60c7dbcca21c51dff6df932a10c4b2d453ea474428c64021dd5ba609f8d5/atomize-0.2.0.tar.gz"; sha256 = "93791ce9d4087223f1a3a59f98aa0134e9281407ce4cb1bd5489c0fd41e4ef64"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://code.google.com/p/atomize/";
        license = "Eclipse Public License 1.0";
        description = "A simple Python package for easily generating Atom feeds";
      };
    };



    "beautifulsoup4" = python.mkDerivation {
      name = "beautifulsoup4-4.5.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/86/ea/8e9fbce5c8405b9614f1fd304f7109d9169a3516a493ce4f7f77c39435b7/beautifulsoup4-4.5.1.tar.gz"; sha256 = "3c9474036afda9136aac6463def733f81017bf9ef3510d25634f335b0c87f5e1"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.crummy.com/software/BeautifulSoup/bs4/";
        license = licenses.mit;
        description = "Screen-scraping library";
      };
    };



    "docutils" = python.mkDerivation {
      name = "docutils-0.12";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/37/38/ceda70135b9144d84884ae2fc5886c6baac4edea39550f28bcd144c1234d/docutils-0.12.tar.gz"; sha256 = "c7db717810ab6965f66c8cf0398a98c9d8df982da39b4cd7f162911eb89596fa"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docutils.sourceforge.net/";
        license = licenses.publicDomain;
        description = "Docutils -- Python Documentation Utilities";
      };
    };



    "psycopg2" = python.mkDerivation {
      name = "psycopg2-2.7.7";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/63/54/c039eb0f46f9a9406b59a638415c2012ad7be9b4b97bfddb1f48c280df3a/psycopg2-2.7.7.tar.gz"; sha256 = "f4526d078aedd5187d0508aa5f9a01eae6a48a470ed678406da94b4cd6524b7e"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://initd.org/psycopg/";
        license = licenses.lgpl2;
        description = "psycopg2 - Python-PostgreSQL Database Adapter";
      };
    };



    "pytest-runner" = python.mkDerivation {
      name = "pytest-runner-4.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/15/0a/1e73c3a3d3f4f5faf5eacac4e55675c1627b15d84265b80b8fef3f8a3fb5/pytest-runner-4.4.tar.gz"; sha256 = "00ad6cd754ce55b01b868a6d00b77161e4d2006b3918bde882376a0a884d0df4"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-runner";
        license = licenses.mit;
        description = "Invoke py.test as distutils command with dependency resolution";
      };
    };



    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.2.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/54/85/514ba3ca2a022bddd68819f187ae826986051d130ec5b972076e4f58a9f3/setuptools_scm-3.2.0.tar.gz"; sha256 = "52ab47715fa0fc7d8e6cd15168d1a69ba995feb1505131c3e814eb7087b57358"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
      };
    };



    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz"; sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };



    "textile" = python.mkDerivation {
      name = "textile-2.3.16";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/1e/e1/41d080eb133547a1a5ca984e1db11d014ea4524d4fa879f3222dcf9fc533/textile-2.3.16.tar.gz"; sha256 = "6f151c1a4119fc5f795b59efdb4a35998718b1a55c2d882e54785a189cfb5907"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/textile/python-textile";
        license = licenses.bsdOriginal;
        description = "Textile processing for python.";
      };
    };

  };
  localOverridesFile = ./requirements_override.nix;
  overrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
    (let src = pkgs.fetchgit { url = "https://github.com/garbas/nixpkgs-python.git"; sha256 = "0v4gxikwh4362s40an68kj7dyiib1bcq5bn9m5j7h93yniz3zkd3"; rev = "403bb1d312b1cfd82663208d7e9ae48c8ff2614a"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [overrides] else [] ) ++ commonOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )
