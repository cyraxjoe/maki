# Maki

The blogging engine behind [blog.joel.mx](https://blog.joel.mx/) ("Introspection").

CherryPy + Mako + SQLAlchemy + PostgreSQL. Posts are written in
reStructuredText and published in English and/or Spanish. There is no web
admin: content is managed from Emacs with the bundled
[maki-mode](emacs/) through a JSON API.

## Development setup

Requires [uv](https://docs.astral.sh/uv/) and Docker (for the dev database).

```sh
docker compose up -d db          # postgres on localhost:5454
uv run python scripts/create_db.py site.cfg
uv run python scripts/default_data.py site.cfg
uv run maki-run site.cfg         # http://localhost:8080
```

Other useful commands:

```sh
uv run maki-shell site.cfg       # REPL with the app config + db loaded
uv run ruff check                # lint
uv run ruff format               # format
```

## Editing from Emacs

The Emacs client lives in [`emacs/`](emacs/):

```elisp
(add-to-list 'load-path "/path/to/maki/emacs")
(require 'maki-mode)
(setq maki-host "http://127.0.0.1:8080")  ;; or the production URL
M-x maki-mode
```

Key bindings: `C-c f` fetch a post (id/url/slug), `C-c n` new post,
`C-c l` set language (new posts), `C-c v` toggle visibility. Saving the
buffer (`C-x C-s`) posts the changes to the server (digest auth).

The default dev credentials are user `joe`, password `samplepasswd`
(see `scripts/default_data.py`).

## Deployment (Nix)

The repo is a flake; the package is built from the uv lockfile via
[uv2nix](https://github.com/pyproject-nix/uv2nix).

```sh
nix build .#maki      # or just: nix build
nix develop           # dev shell with uv + ruff
./release.sh          # build on the server and deploy (see .release.env)
```

The built package exposes the static files at the stable path
`$out/var/lib/static/maki`, which the web server configuration relies on.
