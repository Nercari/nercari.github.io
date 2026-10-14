import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import indexnow_ping as ip


class Ping(unittest.TestCase):
    def test_key_file(self):
        key = ip.read_key()
        self.assertRegex(key, r"^[0-9a-f]{32}$")

    def test_path_mapping(self):
        self.assertEqual(ip.path_to_url("index.html"), "https://nercari.github.io/")
        self.assertEqual(ip.path_to_url("robots.txt"), "https://nercari.github.io/robots.txt")
        self.assertEqual(ip.path_to_url("a/index.html"), "https://nercari.github.io/a/")
        for p in ("README.md", "scripts/indexnow_ping.py", ".github/workflows/x.yml", ip.read_key() + ".txt"):
            self.assertIsNone(ip.path_to_url(p))

    def test_rejects_other_hosts(self):
        for u in ("https://evil.example/", "http://nercari.github.io/", "https://nercari.github.io.evil.example/"):
            with self.assertRaises(SystemExit):
                ip.check_urls([u])

    def test_request_goes_only_to_endpoint(self):
        req = ip.build_request("0" * 32, ["https://nercari.github.io/"])
        self.assertEqual(req.full_url, "https://api.indexnow.org/indexnow")
        body = json.loads(req.data)
        self.assertEqual(body["host"], "nercari.github.io")
        self.assertEqual(body["keyLocation"], "https://nercari.github.io/" + "0" * 32 + ".txt")

    def test_dry_run_sends_nothing(self):
        called = []
        orig, ip.send = ip.send, lambda r: called.append(r)
        try:
            self.assertEqual(ip.main(["x", "--dry-run", "https://nercari.github.io/"]), 0)
        finally:
            ip.send = orig
        self.assertEqual(called, [])

    def test_bad_sha_rejected(self):
        with self.assertRaises(SystemExit):
            ip.changed_urls("HEAD;rm", "abc1234")


if __name__ == "__main__":
    unittest.main()
