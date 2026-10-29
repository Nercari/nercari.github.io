# VERIFY

Merge evidence for nercari.github.io. Paste the real output of these commands in the PR body. When behavior changes, update this file in the same PR.

## Essential check

A syntax check of every Python file, then the IndexNow ping and merge-gate tests (dry run, no network). Offline; under a minute.

```
python3 -m compileall -q .
python3 -m unittest discover -s tests -q
python -m unittest tests.test_merge_gate -q
```
