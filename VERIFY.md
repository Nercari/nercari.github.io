# VERIFY

Merge evidence for nercari.github.io. Paste the real output of these commands in the PR body. When behavior changes, update this file in the same PR.

## Essential check

The IndexNow ping tests (dry run, no network), the same ones CI runs.

```
python3 -m unittest discover -s tests -q
```
