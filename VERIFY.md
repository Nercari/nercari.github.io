# VERIFY

Merge evidence for nercari.github.io. Paste the real output of these commands in the PR body. When behavior changes, update this file in the same PR.

## Essential check

A syntax check of every Python file. The IndexNow ping tests are unit tests: they run locally, not in the gate (Pedro, 2026-10-24). Offline; under a minute.

```
python3 -m compileall -q .
```
