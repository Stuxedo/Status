# Changelog

All notable changes to Stuxedo Server Status are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Date Versioning](https://datevers.ing) since v26.10.23 (`YY.MM.DD`, the UTC release date, with `-1`, `-2`… for later releases the same day); earlier releases used [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v26.11.13-1

### Fixed

- **Registered office country.** The status page's Imprint (`legal.company` in `.githup.yml`) now gives the full registered office, ending in "United Kingdom": 124 City Road, London, EC1V 2NX, England, United Kingdom.

## v26.11.13

### Changed

- **New registered office.** The status page's Imprint (`legal.company` in `.githup.yml`) now shows Stux Group Ltd's new registered office, 124 City Road, London, EC1V 2NX, England (it was 82a James Carter Road, Mildenhall). The company number and "Registered in England and Wales" are unchanged.

## v26.11.12

### Fixed

- **The commit script's push hint** now names the current branch (`test`) and the release tag, and reminds you to open the pull request into `main`. It used to say to push to `main`.

## v26.11.08

### Changed

- **"Checked regularly", not "every 5 minutes".** GitHub runs the 5-minute status schedule best-effort, often much less often, so the page description in `.githup.yml` and the README now say "checked regularly". The README adds that the status page shows the real check rhythm (GitHup v26.11.08). The workflow and script comments call it a best-effort 5-minute schedule. The cron itself is unchanged.

## v26.11.07-2

### Changed

- **Servers sync no longer pushes to `main`.** When it finds a new server it releases and tags it on `test` and opens a `test` → `main` PR, or leaves a notice if one is already open. If it can't open the PR, it leaves a warning with the compare link. The new monitors go live when the PR is merged.
- **CONTRIBUTING says the `stuxedo` slug is an interface.** services.stux.group's Stuxedo badge reads the **Stuxedo** monitor by that slug, so renaming the monitor breaks the badge.
- **All rights reserved.** The License section now reads "Copyright (c) 2026 Stux.Group. All rights reserved. This repository is not licensed for reuse or redistribution", pointing at `LICENSE`.

## v26.11.07-1

### Changed

- **Stuxedo Web Status links point to status.stuxedo.dev**, its new address: the footer link and the Elsewhere link (now named Stuxedo Web Status), the README and the config comment. stuxedostatus.com now redirects to status.stuxedo.com, the landing page, so the Web status workflow reads status.stuxedo.dev only.

## v26.11.07

### Added

- **Stuxedo Web Status's overall state for status.stuxedo.com.** The new **Web status** workflow (`.github/workflows/web-status.yml`, `scripts/web-status.py`) reads the web hosting status page every 5 minutes and saves its state and headline to `data/web-status.json`, committing only when they change. The status landing page shows it as a live badge on its Web Status button. The page is rendered on its server and can't be read cross-site from a browser, so it's read here instead.
- **Stuxedo Web Status (status.stuxedo.dev) is monitored** under Stuxedo, now that it serves over HTTPS.

## v26.11.06-4

### Added

- **Every live Stuxedo site is monitored**, not just stuxedo.com: Stuxedo Status (status.stuxedo.com), the Control Panel, Webmail, Website Builder and Support under Stuxedo; a **Region websites** group (uk, ca, es, fi, us and fr .stuxedo.net); and a **Templates** group (the Region Page, Instance Page, Soonpage and Maintenancepage, their v1 snapshots, and the github.io redirect). Stuxedo Web Status (status.stuxedo.dev) joins once it serves over HTTPS.

## v26.11.06-3

### Changed

- **Work happens on `test`.** Changes reach `main` only through a pull request from `test`, and releases are made and tagged on `test`. CONTRIBUTING has a Branches section, and the README's Versioning section says so.

## v26.11.06-2

### Changed

- **The page is now called Stuxedo Server Status** (it was Stuxedo Status), matching its button on the new Stuxedo Status landing page, which sends you here for the servers or to Stuxedo Web Status for websites and hosting. The README's header, the badge and the scripts use the new name too.

## v26.11.06-1

### Added

- **Stux.Cloud Status** (https://status.stux.cloud/) under Elsewhere: Stux.Cloud's websites and pages. It links back here for the servers behind every Stux.Cloud region.

## v26.11.06

### Added

- **Its own badge icon** as the logo and favicon: Stuxedo's tuxedo cat on a round avatar with a heartbeat badge in the bottom-right corner, in Stuxedo's neon green, instead of the plain brand icon. It's built by `scripts/badge-icons.py` (a copy of StuxGroup/Services' script in Stuxedo's colours) into `assets/img/stuxedo-status-icon.png`, which the Status workflow now copies into the site.

### Changed

- The README's header shows the badge icon and the page's name, **Stuxedo Status**.

## v26.11.05

### Added

- **soci1**, the server in France (`soci1.servers.fr.stuxedo.net`): its instance page under Servers, and its certificate check (`certificates-ok.txt`) under Certificates. The region pages read the `soci1` monitor for its live status.

## v26.10.30-1

### Added

- **New servers are monitored on their own.** The daily **Servers sync** workflow reads Stuxedo's `*.servers.<cc>.stuxedo.net` DNS records from Cloudflare and adds both monitors for any new server (its instance page and its certificate check), then releases and rebuilds the page. New countries and retired servers are still left to a person. It needs the `CLOUDFLARE_DNS_TOKEN` secret (Zone → DNS → Read on stuxedo.net).

### Fixed

- **Termix is checked under mixr2's certificates, not mixr1's.** It moved to mixr2 on 30 October.

## v26.10.30

### Added

- **mixr2**, the server in Finland (`mixr2.servers.fi.stuxedo.net`): its instance page under Servers, and its certificate check (`certificates-ok.txt`) under Certificates. The region pages read the `mixr2` monitor for its live status.

## v26.10.23

### Added

- `tests/version.sh`, which checks that `VERSION.md` is a valid Date Version, a real calendar date not in the future, and the same as the newest entry in this changelog

### Changed

- Switched from Semantic Versioning to [Date Versioning](https://datevers.ing): releases are numbered by their UTC release date as `YY.MM.DD`, with `-1`, `-2`… for later releases the same day. This release follows v1.0.2
- `commit.sh` and `commit.bat` refuse a `VERSION.md` that isn't a valid Date Version or is dated in the future (UTC), and warn when it's dated before today
- `README.md` and `CONTRIBUTING.md` describe Date Versioning and the release steps

## [1.0.2] - 2026-10-09

### Changed

- The status page header shows just the Stuxedo icon (`icon-light.png`) instead of the full logo

## [1.0.1] - 2026-10-09

### Changed

- The logos and icons in the Markdown docs (README and the like) follow GitHub's light or dark theme, using each brand's `logo-light`/`logo-dark` and `icon-light`/`icon-dark` files

## [1.0.0] - 2026-10-09

### Added

- Stuxedo Status (`status.stuxedo.net`), built with [GitHup](https://githup.stux.group): checks every 5 minutes (catching up when GitHub runs the schedule late), incident Issues, and the status page deployed to GitHub Pages by `.github/workflows/status.yml`
- The servers (robo1, tiny1, kitt1, mixr1, down1), their daily certificate checks and the Stuxedo site, moved here from Stux.Group Status with their history and slugs, so the Stuxedo and Stux.Cloud region pages keep working; plus the Stuxedo media CDN
- Links to the web hosting status page (stuxedostatus.com) and Stux.Group Status
- Stuxedo branding (`logo-light.png`, `icon-light.png`, neon `#4BF708` accent) and GitHup's Boring Legal Stuff hub and six legal pages for Stuxedo, plus its 404, sitemap page, `sitemap.xml` and `robots.txt`
- `dev-server.sh` / `dev-server.bat` (example data, DEV_MODE on by default, `--no-dev-mode` for production rendering), and `commit.sh` / `commit.bat` for tagged releases
