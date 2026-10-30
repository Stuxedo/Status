"""Adds new Stuxedo servers to the status page from Cloudflare's DNS. Run daily by .github/workflows/servers-sync.yml.

Every server has an A record <name>.servers.<cc>.stuxedo.net in the stuxedo.net zone. A server that has a
record but no monitor in .githup.yml gets two: "<name>" (its instance page, under Servers) and "<name>
certificates" (its certificates-ok.txt, under Certificates). The region pages read the "<name>" monitor. The
README's list is updated, and a release is written: CHANGELOG.md entry and VERSION.md. The workflow commits,
tags and deploys it.

The country's name comes from Stuxedo/regionpage's assets/regions.js. A server in a country that isn't a region
there yet fails the run (add it with the deploy-stuxedo-server skill). A monitored server with no record is only
warned about, since retiring one is a person's decision.

    CLOUDFLARE_DNS_TOKEN=... python scripts/sync-servers.py      (Zone > DNS > Read, on stuxedo.net)
"""
import datetime, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZONE = "stuxedo.net"
HOST = re.compile(r"^([a-z0-9]+)\.servers\.([a-z]{2})\.stuxedo\.net$")
REGIONS = "https://raw.githubusercontent.com/Stuxedo/regionpage/main/assets/regions.js"


def get(url, headers=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=30) as r:
        return r.read().decode("utf-8")


def cloudflare(path):
    body = json.loads(get("https://api.cloudflare.com/client/v4" + path,
                          {"Authorization": "Bearer " + os.environ["CLOUDFLARE_DNS_TOKEN"]}))
    if not body.get("success"):
        sys.exit(f"Cloudflare: {body.get('errors')}")
    return body["result"]


def dns_servers():
    zone = cloudflare(f"/zones?name={ZONE}")[0]["id"]
    found = set()
    for rec in cloudflare(f"/zones/{zone}/dns_records?type=A&per_page=1000"):
        m = HOST.match(rec["name"])
        if m:
            found.add((m.group(1), m.group(2)))
    return found


def read(path):
    raw = path.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def write(path, text, crlf):
    path.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def add_monitors(t, name, cc, country):
    host = f"https://{name}.servers.{cc}.{ZONE}/"
    srv = list(re.finditer(r"      - name: [a-z0-9]+\n        url: https://[a-z0-9]+\.servers\.[a-z]+\.stuxedo\.net/\n        description: [^\n]+\n", t))
    cert = list(re.finditer(r"      - name: [a-z0-9]+ certificates\n        url: [^\n]+\n        description: [^\n]+\n", t))
    t = t[:cert[-1].end()] + f"      - name: {name} certificates\n        url: {host}certificates-ok.txt\n        description: {name} ({country})\n" + t[cert[-1].end():]
    t = t[:srv[-1].end()] + f"      - name: {name}\n        url: {host}\n        description: {country}\n" + t[srv[-1].end():]
    return re.sub(r"\(slugs ([a-z0-9, ]+)\)", lambda m: f"(slugs {m.group(1)}, {name})", t)


def next_version():
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%y.%m.%d")
    tags = subprocess.run(["git", "tag", "-l", f"v{today}*"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    taken = {(ROOT / "VERSION.md").read_text().strip(), *(t[1:] for t in tags)}
    if today not in taken:
        return today
    return f"{today}-{max(int(v.split('-')[1]) if '-' in v else 0 for v in taken if v.startswith(today)) + 1}"


def main():
    cfg_path = ROOT / ".githup.yml"
    t, crlf = read(cfg_path)
    monitored = set(re.findall(r"      - name: ([a-z0-9]+)\n        url: https://[a-z0-9]+\.servers\.([a-z]+)\.stuxedo\.net/\n", t))
    js = get(REGIONS)
    regions = {r["code"]: r for r in json.loads(js[js.index("{", js.index("REGION_DATA")): js.rindex("}") + 1])["regions"]}
    found = dns_servers()

    for name, cc in sorted(monitored - found):
        print(f"::warning::{name} ({cc}) is monitored but has no DNS record. If it's retired, remove its monitors by hand.")
    new = sorted(found - monitored)
    unknown = [(n, cc) for n, cc in new if cc not in regions]
    for name, cc in unknown:
        print(f"::error::{name}.servers.{cc}.{ZONE}: '{cc}' isn't a region yet. Add it with the deploy-stuxedo-server skill.")
    new = [(n, cc) for n, cc in new if cc in regions]
    for name, cc in new:
        t = add_monitors(t, name, cc, regions[cc]["name"])
        print(f"added {name} and {name} certificates ({regions[cc]['name']})")

    if new:
        write(cfg_path, t, crlf)
        readme, r_crlf = read(ROOT / "README.md")
        extra = "".join(f", {n} in {regions[cc]['name']}" for n, cc in new)
        readme = re.sub(r"(each server's instance page \()([^)]*)(\))", lambda m: m.group(1) + m.group(2) + extra + m.group(3), readme, count=1)
        write(ROOT / "README.md", readme, r_crlf)
        version = next_version()
        lines = "\n".join(f"- **{n}**, the server in {regions[cc]['name']} (`{n}.servers.{cc}.{ZONE}`): its instance page under "
                          f"Servers, and its certificate check (`certificates-ok.txt`) under Certificates. Added automatically "
                          f"from Stuxedo's DNS." for n, cc in new)
        log, log_crlf = read(ROOT / "CHANGELOG.md")
        i = log.index("\n## v") + 1
        write(ROOT / "CHANGELOG.md", log[:i] + f"## v{version}\n\n### Added\n\n{lines}\n\n" + log[i:], log_crlf)
        (ROOT / "VERSION.md").write_text(version + "\n")
        print(f"release v{version}")
        out = os.environ.get("GITHUB_OUTPUT")
        if out:
            with open(out, "a") as f:
                f.write(f"version={version}\n")
    else:
        print("nothing new: every server with a DNS record is monitored")
    if unknown:
        sys.exit(1)


main()
