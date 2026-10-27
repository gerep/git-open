import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "git-open"


class GitOpenTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.capture = self.root / "opened-url"
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        for name in ("open", "xdg-open"):
            opener = bin_dir / name
            opener.write_text('#!/bin/sh\nprintf "%s" "$1" > "$CAPTURE"\n')
            opener.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}",
                        CAPTURE=str(self.capture), GIT_CONFIG_NOSYSTEM="1",
                        GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-q")
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.test",
                 "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "test")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("config", "remote.origin.url", "git@github.com:owner/repo.git")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env,
                              check=True, capture_output=True, text=True)

    def run_open(self, *args, cwd=None):
        self.capture.unlink(missing_ok=True)
        return subprocess.run(["bash", str(SCRIPT), *args], cwd=cwd or self.repo,
                              env=self.env, capture_output=True, text=True)

    def test_provider_urls(self):
        cases = [
            ("git@github.com:owner/repo.git", [], "https://github.com/owner/repo/tree/main"),
            ("https://github.com/owner/repo.name", ["main"], "https://github.com/owner/repo.name/tree/main"),
            ("git@bitbucket.org:owner/repo.name.git", ["main"], "https://bitbucket.org/owner/repo.name/branch/main"),
            ("https://gitlab.example.org/group/repo.git", ["main"], "https://gitlab.example.org/group/repo/-/tree/main"),
            ("ssh://git@gitlab.example.org:2222/group/sub/repo.git", ["main"], "https://gitlab.example.org/group/sub/repo/-/tree/main"),
            ("https://user:secret@github.com/owner/repo.git", ["main", "README.md"], "https://github.com/owner/repo/blob/main/README.md"),
            ("git@gitlab.com:group/repo.git", ["main", "README.md"], "https://gitlab.com/group/repo/-/blob/main/README.md"),
            ("git@bitbucket.org:owner/repo.git", ["main", "README.md"], "https://bitbucket.org/owner/repo/src/main/README.md"),
            ("git@codeberg.org:owner/repo.git", ["main", "README.md"], "https://codeberg.org/owner/repo/src/branch/main/README.md"),
            ("http://gitlab.example.org:8080/group/repo.git", ["main"], "http://gitlab.example.org:8080/group/repo/-/tree/main"),
        ]
        for remote, args, expected in cases:
            with self.subTest(remote=remote, args=args):
                self.git("config", "remote.origin.url", remote)
                result = self.run_open(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.capture.read_text(), expected)

    def test_encoding(self):
        self.git("update-ref", "refs/remotes/origin/feature/a#b", "HEAD")
        result = self.run_open("feature/a#b", "docs/a b#é.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.capture.read_text(),
                         "https://github.com/owner/repo/blob/feature/a%23b/docs/a%20b%23%C3%A9.md")

    def assert_failure(self, result, message):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertFalse(self.capture.exists())

    def test_branch_match_is_exact(self):
        self.assert_failure(self.run_open("ma.n"), "git fetch origin")

    def test_missing_origin(self):
        self.git("config", "--unset", "remote.origin.url")
        self.assert_failure(self.run_open(), "There is no origin remote")

    def test_outside_repository(self):
        self.assert_failure(self.run_open(cwd=self.root), "not a git repository")

    def test_detached_head(self):
        self.git("checkout", "--detach", "-q")
        self.assert_failure(self.run_open(), "Detached HEAD")
        self.assertEqual(self.run_open("main").returncode, 0)

    def test_unsupported_host(self):
        self.git("config", "remote.origin.url", "https://example.org/owner/repo.git")
        self.assert_failure(self.run_open(), "Unsupported Git host")

    def test_invalid_arguments(self):
        for args in [("main", "file", "extra"), ("main", ""), ("main", "/absolute"), ("bad..branch",)]:
            with self.subTest(args=args):
                self.assert_failure(self.run_open(*args), "git-open:")

    def test_help_outside_repository(self):
        result = self.run_open("--help", cwd=self.root)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)
        self.assertFalse(self.capture.exists())
