<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stuxedo.com/logo-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stuxedo.com/logo-dark.png"><img src="https://global.media.stuxedo.com/logo-dark.png" height="80" alt="Stuxedo Logo"></picture>
</p>

# Contributing to Status

Status is Stuxedo's status page, [status.stuxedo.net](https://status.stuxedo.net), built with
[GitHup](https://githup.stux.group). To report an outage, open an Issue. Bugs or ideas for the
status page software belong in [StuxGroup/GitHup](https://github.com/StuxGroup/GitHup/issues).

## Local setup

You need Python 3.11+ and nothing else.

```bash
./dev-server.sh [--no-dev-mode] [port]   # or dev-server.bat on Windows
```

## Project conventions

- **Monitors live in `.githup.yml`.** Its syntax is documented in the
  [GitHup docs](https://githup.stux.group/docs/). Only add sites Stuxedo runs.
- **The status page itself is GitHup's**, including the legal pages and 404. Change how it
  looks or works in GitHup, not here.
- **Brand.** Stuxedo is neon green (`#4bf708`). GitHup takes one accent, so `site.accent` is `#4BF708` and GitHup darkens it on the light theme until it reads; the logo is `logo-light.png`, whose dark outline reads on both themes.
- **Slugs are an interface.** The Stuxedo and Stux.Cloud region pages read the server monitors by slug (`robo1`, `tiny1`, `kitt1`, `mixr1`, `down1`); renaming one breaks their live status.
- **Legal pages.** The `legal:` block in `.githup.yml` drives **Boring Legal Stuff** at `/legal/`.
  Keep it accurate.
- **Don't edit `data/` by hand.** It belongs to GitHup and the workflow.

## Versioning and changelog

- The version lives in `VERSION.md` (a bare version string). Bump it on every release.
- Every release gets a `CHANGELOG.md` entry using `###` subsections in this order: Added,
  Changed, Fixed, Removed, Security, Deprecated. Never a bare bullet list under a version.
- `commit.sh` (bash) and `commit.bat` (Windows) read `VERSION.md`, commit and create the
  annotated `vX.Y.Z` tag. Push with `git push origin main vX.Y.Z`.
