# Changelog

All notable changes to Stuxedo Status are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
