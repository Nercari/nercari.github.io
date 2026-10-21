# Review guide

## Hard stops
- Stop if the IndexNow ping sends to a host other than `api.indexnow.org`, or for URLs off `nercari.github.io` (`scripts/indexnow_ping.py`, `check_urls`).
- Stop if a PR adds a secret. The ping needs none (README.md).
- Stop on a push to main outside the PR flow, or a force-push (HQ block in AGENTS.md).

## Fragile files
- `8b7e6f8f675aa09ea5faf87e2e5a63fe.txt`: the IndexNow key file. `read_key` needs exactly one root `.txt` named like its content.
- `scripts/indexnow_ping.py`: it builds `keyLocation` from the key name. It refuses redirects.
- `.github/workflows/indexnow.yml`: it pings after each push to `main`.
- `robots.txt`: it lists the sitemap of each project site.

## Tests that must pass
- `python -m unittest discover -s tests -q`: OK (run).
- `python scripts/indexnow_ping.py --dry-run --from-git <before> <after>`: sends nothing.
