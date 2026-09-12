# Maki — agent guide

CherryPy blog engine behind blog.joel.mx ("Introspection"). Python 3.13,
SQLAlchemy 2 + PostgreSQL, Mako templates, posts written in
reStructuredText, bilingual EN/ES. Managed with uv; deployed with Nix
(flake + uv2nix).

## Invariants — do not break these

- **DB schema**: the production database predates this codebase's
  refreshes. Never change `maki/db/models.py` in a way that alters the
  emitted schema without an explicit migration plan.
- **JSON API**: it is the contract for the Emacs client in `emacs/`
  (digest auth): `GET /posts/` (list), `GET /posts/<id>` and
  `/posts/<slug>?by=slug`, `POST /posts/add/`, `POST /posts/update/<id>`,
  `POST /posts/visibility`. Field names and response shapes in
  `maki/views/post.py` (class `JSON`) must stay stable.
- **Public URLs**: `/`, `/posts/<slug>`, `/posts/?cat=<slug>`,
  `/feed/[<category>]`, `/lang/<code>` — indexed by search engines and
  feed readers.
- **Visual identity**: dark `#222` background, orange `#E5AC26` accent
  (CSS custom properties in `maki/static/css/maki.css`), "Introspection"
  banner, monokai pygments. No JavaScript on the public site.

## Architecture

- `maki/scaffold.py` — the core trick: `Controller` builds per-MIME
  "branches" from its `__views__` classes, and
  `maki/dispatcher.py::ContentTypeDispatcher` picks the branch by the
  request's Accept header. That's how `/posts/1` serves HTML to browsers
  and JSON (with digest auth) to the Emacs client from one URL tree.
- `maki/controllers/` — business logic (no cherrypy handlers);
  `maki/views/` — the exposed HTML/XML/JSON handlers that call into
  controllers via `self.ctrl`.
- `maki/ctools/` — CherryPy tools (mako rendering, i18n, db-session
  cleanup) registered via `maki/bindutils.py`; `maki/cplugins/` — engine
  plugins (db engine startup). Loaded by `scaffold.setup()` at import
  time of the `maki` package (import order in `maki/__init__.py` is
  deliberate and fragile).
- `maki/db/__init__.py` — one global scoped session `db.ses`; removed
  per-request by the `removedbs` tool. Legacy Query API
  (`db.ses.query(...)`) is the house style.
- Templates in `maki/templates/` (Mako): `_base.mako` → `_layout.mako`
  (header/sidebar/footer) → pages. Error pages render outside the
  request via `maki/errors.py` + `maki/utils/makoutils.py`.
- Config `site.cfg` is a CherryPy config file: values are Python
  expressions (it can call e.g. `os.environ.get`).

## Gotchas

- i18n is a hand-rolled STRINGS dict in `maki/i18n.py`. Any new
  user-visible string in templates needs `_("...")` plus an `es` entry
  there.
- Posts content is rST rendered at view time in
  `maki/templates/post/show.mako` (docutils + pygments, short class
  names styled by `maki/static/css/pygments/monokai.css`).
- The Post model versions content: `Post.revisions` (list of
  `PostRevision`); `post.title/content/...` proxy to the latest
  revision. Appending a revision re-derives `post.slug` from the title.
- psycopg 3 does not coerce strings to ints like psycopg2 did — cast
  request params before using them in queries.
- Date formatting (`maki/i18n.py::fmt_date`) calls `locale.setlocale`
  with `en_US.UTF-8` / `es_MX.UTF-8`; those locales must exist on the
  host (nix devshell ships glibcLocales on Linux).
- `emacs/maki-url-auth.el` patches Emacs' url-auth digest HA2 caching
  bug; without it POSTs from Emacs get 401.

## Commands

```sh
docker compose up -d db                        # dev postgres :5454
uv run python scripts/create_db.py site.cfg    # create schema
uv run python scripts/default_data.py site.cfg # seed langs/format/user
uv run maki-run site.cfg                       # serve :8080
scripts/smoke.sh                               # smoke test running server
uv run ruff check && uv run ruff format        # lint / format
nix build                                      # production package
```

## Deployment

Production is a NixOS host running the app via `cherryd` and a systemd
unit, with its own NixOS-managed copy of `site.cfg` (unix-socket
postgres; on the first deploy of >= 0.5.0 its sqlalchemy url scheme must
change from `postgresql://` to `postgresql+psycopg://`). `./release.sh` builds the flake from GitHub master *on the
target host* (right platform, no store signing needed), installs into
the app's nix profile and restarts the service — push to GitHub before
releasing. The host specifics (ssh destination, profile path, unit
name) are deliberately not committed: they live in the untracked
`.release.env` read by `release.sh`. Restoring a production DB backup
into the dev db needs the production db role to exist first (create the
role named in the dump's `OWNER TO` statements, with `LOGIN`). The dump
carries the production digest hash for `joe`, so afterwards reset it to
the dev password or `scripts/smoke.sh` and the Emacs client get 401:
`update users set ha1 = md5('joe:Maki blog:samplepasswd') where name = 'joe';`

Dev credentials: `joe` / `samplepasswd`. Verify template/CSS work with a
real browser render, and JSON API changes against `emacs/maki-mode.el`
(there is a batch-mode pattern: stub `read-string`/`read-passwd`, call
`maki-get-post`, `maki-post-save`).
