# nercari.github.io

Root site for Nercari's GitHub Pages projects. Holds the root `robots.txt` (with sitemaps for each project site) and a minimal index linking to them.

## IndexNow

The IndexNow key file sits at the site root. After each push to `main`, the
`IndexNow ping` workflow sends the changed page URLs on nercari.github.io to
`api.indexnow.org` only. It needs no secrets. Try it locally without sending:
`python3 scripts/indexnow_ping.py --dry-run --from-git <before> <after>`.
