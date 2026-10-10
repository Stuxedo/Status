<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stuxedo.com/logo-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stuxedo.com/logo-dark.png"><img src="https://global.media.stuxedo.com/logo-dark.png" height="100" alt="Stuxedo Logo"></picture>
</p>

# Status

### *Live status of Stuxedo's servers and websites, powered by [GitHup](https://githup.stux.group).*

**Status page:** [status.stuxedo.net](https://status.stuxedo.net)

<!-- A live badge: reads the overall status straight from data/summary.json (after the first check). -->
[![Stuxedo status](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FStuxedo%2FStatus%2Fmain%2Fdata%2Fsummary.json&query=%24.status&label=status&style=for-the-badge)](https://status.stuxedo.net)

## Current status

Updated by GitHup whenever the status page is rebuilt (hourly, and when a status changes). The
table fills in after the workflow's first check.

<!-- githup:start -->
<!-- This table is written by GitHup (https://github.com/StuxGroup/GitHup); edits here are overwritten. -->

**All systems operational** · [Live status page](https://status.stuxedo.net/)

| Group | Monitor | Status | Uptime (24 h) | Uptime (7 d) | Uptime (30 d) | Response time (24 h) |
| ----- | ------- | ------ | ------------- | ------------ | ------------- | -------------------- |
| Stuxedo | [Stuxedo](https://stuxedo.com/) | Up | 100.00% | 99.59% | 99.71% | 451 ms |
| Stuxedo | [Stuxedo Media CDN](https://global.media.stuxedo.com/icon.png) | Up | 100.00% | 100.00% | 100.00% | 430 ms |
| Servers | [robo1](https://robo1.servers.uk.stuxedo.net/) | Up | 100.00% | 100.00% | 100.00% | 429 ms |
| Servers | [tiny1](https://tiny1.servers.uk.stuxedo.net/) | Up | 100.00% | 100.00% | 100.00% | 439 ms |
| Servers | [kitt1](https://kitt1.servers.ca.stuxedo.net/) | Up | 100.00% | 100.00% | 100.00% | 243 ms |
| Servers | [mixr1](https://mixr1.servers.es.stuxedo.net/) | Up | 100.00% | 100.00% | 100.00% | 483 ms |
| Servers | [down1](https://down1.servers.us.stuxedo.net/) | Up | 100.00% | 100.00% | 100.00% | 255 ms |
| Certificates | [robo1 certificates](https://robo1.servers.uk.stuxedo.net/certificates-ok.txt) | Up | 100.00% | 100.00% | 100.00% | 423 ms |
| Certificates | [tiny1 certificates](https://tiny1.servers.uk.stuxedo.net/certificates-ok.txt) | Up | 100.00% | 100.00% | 100.00% | 363 ms |
| Certificates | [kitt1 certificates](https://kitt1.servers.ca.stuxedo.net/certificates-ok.txt) | Up | 100.00% | 100.00% | 100.00% | 175 ms |
| Certificates | [mixr1 certificates](https://mixr1.servers.es.stuxedo.net/certificates-ok.txt) | Up | 100.00% | 100.00% | 100.00% | 404 ms |
| Certificates | [down1 certificates](https://down1.servers.us.stuxedo.net/certificates-ok.txt) | Up | 100.00% | 100.00% | 100.00% | 195 ms |
<!-- githup:end -->

## What's monitored

Every 5 minutes (when GitHub runs the schedule late, a run checks up to 4 times, 5 minutes apart, to fill the gap), GitHup checks each monitor in [`.githup.yml`](.githup.yml):

- **Stuxedo:** [stuxedo.com](https://stuxedo.com) and the Stuxedo media CDN
- **Servers:** each server's instance page (robo1 and tiny1 in the UK, kitt1 in Canada, mixr1 in
  Spain, down1 in the United States). The [Stuxedo](https://regionpage.stuxedo.net) and
  [Stux.Cloud](https://regionpage.stux.cloud) region pages read these monitors (by slug) for their
  live server status
- **Certificates:** each server checks daily that every certificate it uses has more than 21
  days left, and publishes `certificates-ok.txt` while it does
- Web hosting has its own status page, [stuxedostatus.com](https://stuxedostatus.com), linked
  under Elsewhere. `status.stuxedo.com` will become the landing page for both

The servers, their certificate checks and the Stuxedo site were checked on
[Stux.Group Status](https://status.stux.group) until 9 October 2026; their history came with them
(`data/<slug>/`).

To add a monitor, add it to the right group there (or a new group). A group can also hold `links:` instead of monitors, for sites that should be listed but not checked.

When something goes down, GitHup opens an Issue on this repository (labelled `githup`,
`incident`, `status` and the monitor's slug) and closes it with the downtime when it recovers.
To announce planned maintenance, open an Issue yourself with the `githup` and `incident` labels
(plus the monitor's slug to link it); it shows on the status page.

## How it works

- **`.github/workflows/status.yml`** runs a GitHup `check` every 5 minutes (with `fill-gaps`, up to 4 checks when the schedule is late) and commits the
  results to `data/` as `github-actions[bot]`. When a status changes, hourly, and on pushes, it
  builds the GitHup status page into `_site` (with `site-dir`), and deploys it with `actions/deploy-pages`.
- **`legal:` in `.githup.yml`** makes GitHup generate the **Boring Legal Stuff** hub at `/legal/`
  with its six sub-pages, a themed `404.html`, a `/sitemap/` page, `sitemap.xml` and `robots.txt`
  (the base URL is `site.url`). Nothing is hand-made, and the footer shows only
  **Powered by GitHup**. This repo's own `CHANGELOG.md` and `VERSION.md` are for this repo only.
- **`data/`** is the monitoring history. Don't edit it by hand.
- **The status table above** is written by GitHup's `readme` mode between the
  `<!-- githup:start -->` and `<!-- githup:end -->` markers. Don't edit inside them.

## Local development

```bash
./dev-server.sh                 # or dev-server.bat on Windows; add a port as the last argument
./dev-server.sh --no-dev-mode   # production rendering
```

`dev-server` generates 90 days of example data, builds the status page into `.dev/public` with
`DEV_MODE` on, with its legal pages, 404 and sitemap, and serves it at
`http://127.0.0.1:8000`. It uses GitHup from `$GITHUP_PATH`, a sibling `../GitHup` checkout, or
a fresh clone in `.dev/GitHup`.

## Hosting

GitHub Pages, deployed by Actions (**Settings → Pages → Source: GitHub Actions**), with the custom
domain `status.stuxedo.net` set in the Pages settings. DNS: a `CNAME` record for `status` (in the
`stuxedo.net` zone, ahead of its `*` wildcard) pointing at `stuxedo.github.io`. The repository is
public, so the page's live refresh can read `data/summary.json` straight from GitHub.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

&copy; 2026 Stux.Group. All rights reserved. This repository is not licensed for reuse or
redistribution, see [LICENSE](LICENSE).

---

*Built & Maintained by <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stuxedo.com/icon-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stuxedo.com/icon-dark.png"><img src="https://global.media.stuxedo.com/icon-dark.png" height="14" alt="Stuxedo" valign="middle"></picture> [Stuxedo](https://github.com/Stuxedo), powered by [GitHup](https://githup.stux.group).
Stuxedo is a part of the <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stux.group/icon-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stux.group/icon-dark.png"><img src="https://global.media.stux.group/icon-dark.png" height="14" alt="Stux.Group" valign="middle"></picture> Stux.Group brand of businesses.*
