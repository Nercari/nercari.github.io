"""Ping IndexNow with changed nercari.github.io URLs. Standard library only.

WARDEN-CHECK: network egress script. Sends only to https://api.indexnow.org/indexnow,
refuses redirects, only submits https://nercari.github.io/ URLs, reads the public key
from the <key>.txt file at the repo root, needs no secrets.

Usage:
  python3 scripts/indexnow_ping.py [--dry-run] --from-git <before_sha> <after_sha>
  python3 scripts/indexnow_ping.py [--dry-run] <url> [<url> ...]
"""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = "nercari.github.io"
BASE = f"https://{HOST}/"
ROOT = Path(__file__).resolve().parent.parent
KEY_RE = re.compile(r"^[0-9a-f]{32}$")
PAGE_SUFFIXES = (".html", ".xml", ".txt")


def read_key(root=ROOT):
    found = [p for p in root.glob("*.txt") if KEY_RE.match(p.stem) and p.read_text().strip() == p.stem]
    if len(found) != 1:
        raise SystemExit(f"expected exactly one IndexNow key file at the root, found {len(found)}")
    return found[0].stem


def path_to_url(path):
    if not path.endswith(PAGE_SUFFIXES) or path.startswith((".", "scripts/", "tests/")) or KEY_RE.match(Path(path).stem):
        return None
    if path == "index.html":
        return BASE
    if path.endswith("/index.html"):
        return BASE + path[: -len("index.html")]
    return BASE + path


def changed_urls(before, after, root=ROOT):
    for sha in (before, after):
        if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            raise SystemExit(f"not a commit sha: {sha!r}")
    if set(before) == {"0"}:
        out = subprocess.run(["git", "ls-tree", "-r", "--name-only", after], cwd=root, capture_output=True, text=True, check=True).stdout
    else:
        out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AMR", before, after], cwd=root, capture_output=True, text=True, check=True).stdout
    return sorted({u for u in (path_to_url(p) for p in out.split()) if u})


def check_urls(urls):
    bad = [u for u in urls if not u.startswith(BASE)]
    if bad:
        raise SystemExit("refusing URLs off " + HOST + ": " + ", ".join(bad))
    return sorted(set(urls))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        raise urllib.error.HTTPError(a[0].full_url, a[2], "redirect refused", a[4], None)


def build_request(key, urls):
    body = {"host": HOST, "key": key, "keyLocation": f"{BASE}{key}.txt", "urlList": urls}
    return urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), method="POST",
                                  headers={"Content-Type": "application/json; charset=utf-8"})


def send(req):
    assert req.full_url == ENDPOINT
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(req, timeout=20) as r:
        return r.status


def main(argv):
    args = argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if args[:1] == ["--from-git"] and len(args) == 3:
        urls = changed_urls(args[1], args[2])
    elif args and not args[0].startswith("-"):
        urls = check_urls(args)
    else:
        print(__doc__.strip().split("Usage:")[1])
        return 2
    if not urls:
        print("no changed page URLs; nothing to ping")
        return 0
    key = read_key()
    req = build_request(key, urls)
    print(("DRY RUN, would POST to " if dry else "POST ") + ENDPOINT)
    print("\n".join(urls))
    if dry:
        return 0
    status = send(req)
    print(f"IndexNow answered HTTP {status}")
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
