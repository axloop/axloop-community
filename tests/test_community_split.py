"""Policy tests for scripts/check-community-split.py.

Each rejection test starts from a minimal compliant Community tree, adds
exactly one prohibited condition, and asserts a nonzero exit plus a
category-level diagnostic. Sensitive values (the private enterprise
repository, the obsolete boundary slogan, the historical staging tag) are
assembled from neutral fragments so they never appear literally in this
repository.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "scripts" / "check-community-split.py"

PRIVATE_ORG = "ascendant" + "ventures"
PRIVATE_NAME = "axloop-edge" + "-poc"
PRIVATE_REPO = "/".join((PRIVATE_ORG, PRIVATE_NAME))
PRIVATE_URL = "https://" + "/".join(("github.com", PRIVATE_REPO))
OBSOLETE_LOCATION = " ".join(("enterprise", "stays", "in"))
STAGING_TAG = "-".join(("community", "acceptance", "staging", "2026", "08", "29"))

PUBLIC_SITE = "https://www.axloop.ai"
LATEST_RELEASE = "https://github.com/axloop/axloop-community/releases/latest"

README = f"""# AxLoop Community

## First run

1. Check the [latest GitHub Release]({LATEST_RELEASE}).
2. No Community GitHub Release has been published yet.

## Enterprise

For the AxLoop enterprise product, visit [axloop.ai]({PUBLIC_SITE}).
"""

CHANGELOG = """# Changelog

## [Unreleased]

No Community GitHub Release has been published yet.
"""

RELEASES_DOC = f"""# Community releases

The latest install will appear at {LATEST_RELEASE}.
No Community GitHub Release has been published yet.
The historical 2026-08-29 acceptance-staging tag is not a release input.
Release signing material never belongs in Community CI.
"""


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def make_valid_tree(root: Path) -> None:
    write(root, "README.md", README)
    write(root, "CHANGELOG.md", CHANGELOG)
    write(root, "docs/COMMUNITY_RELEASES.md", RELEASES_DOC)


def run_checker(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)],
        capture_output=True,
        text=True,
    )


class CheckerFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_valid_tree(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_checker(self) -> subprocess.CompletedProcess:
        return run_checker(self.root)

    def assert_rejected(self, category: str) -> str:
        result = self.run_checker()
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(category, output)
        for sensitive in (PRIVATE_ORG, PRIVATE_NAME, OBSOLETE_LOCATION, STAGING_TAG):
            self.assertNotIn(sensitive, output)
        return output

    def assert_accepted(self) -> str:
        result = self.run_checker()
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("PASS", output)
        return output

    # --- compliant states -------------------------------------------------

    def test_accepts_clean_funnel_tree(self):
        write(self.root, ".community-release.json", "{}\n")
        write(self.root, "docs/cli.md", "The Community CLI entry point is `axloop radar`.\n")
        write(
            self.root,
            "docs/enterprise.md",
            f"Enterprise capabilities such as signing and acceptance are described at {PUBLIC_SITE}.\n",
        )
        self.assert_accepted()

    def test_accepts_read_only_release_lookup_and_deferred_rename_prose(self):
        write(
            self.root,
            "docs/notes.md",
            "Verify with:\n\n```bash\ngh api repos/axloop/axloop-community/releases\ngit tag --list\n```\n\n"
            "The CLI `radar` to `crawler` rename is deferred and not implemented here.\n",
        )
        self.assert_accepted()

    # --- private repository and obsolete boundary language ----------------

    def test_rejects_private_repo_reference_in_markdown(self):
        write(self.root, "README.md", PRIVATE_URL)
        output = self.assert_rejected("private repository reference")
        self.assertIn("README.md", output)

    def test_rejects_private_repo_slug_without_url(self):
        write(self.root, "docs/boundary.md", f"Source lives in {PRIVATE_REPO}.\n")
        self.assert_rejected("private repository reference")

    def test_rejects_private_repo_reference_in_non_markdown_text(self):
        write(self.root, "config/source.txt", f"origin={PRIVATE_URL}\n")
        self.assert_rejected("private repository reference")

    def test_rejects_private_repo_checkout_in_workflow(self):
        write(
            self.root,
            ".github/workflows/ci.yml",
            f"steps:\n  - uses: actions/checkout@v4\n    with:\n      repository: {PRIVATE_REPO}\n",
        )
        self.assert_rejected("private repository reference")

    def test_rejects_obsolete_location_language(self):
        write(self.root, "docs/boundary.md", OBSOLETE_LOCATION)
        self.assert_rejected("obsolete boundary language")

    def test_rejects_factory_to_github_pointer(self):
        write(
            self.root,
            "docs/boundary.md",
            " ".join((
                "Builds remain in the enterprise",
                "factory",
                "on github.com.",
            )) + "\n",
        )
        self.assert_rejected("obsolete boundary language")

    # --- release publication -----------------------------------------------

    def test_rejects_published_release_metadata(self):
        write(self.root, ".community-release.json", '{"published_at":"2026-09-02"}')
        self.assert_rejected("release publication")

    def test_rejects_release_workflow(self):
        write(self.root, ".github/workflows/release.yml", "name: Publish release")
        self.assert_rejected("release publication")

    def test_rejects_release_publish_command_in_workflow(self):
        write(
            self.root,
            ".github/workflows/ci.yml",
            "name: ci\njobs:\n  a:\n    steps:\n      - run: gh release edit v1 --draft=false\n",
        )
        self.assert_rejected("release publication")

    def test_rejects_release_tag_creation_command(self):
        write(self.root, "scripts/cut.sh", "git tag v0.1.0\ngit push origin --tags\n")
        self.assert_rejected("release publication")

    def test_rejects_release_publish_instruction_in_markdown_code_block(self):
        write(
            self.root,
            "docs/COMMUNITY_RELEASES.md",
            RELEASES_DOC + "\n```bash\ngh release create v0.1.0 --notes 'first'\n```\n",
        )
        self.assert_rejected("release publication")

    def test_rejects_staging_tag_as_release_input(self):
        write(self.root, "release-input.txt", STAGING_TAG)
        self.assert_rejected("staging tag as release input")

    def test_rejects_staging_tag_in_markdown(self):
        write(self.root, "docs/COMMUNITY_RELEASES.md", RELEASES_DOC + f"\nDo not use `{STAGING_TAG}`.\n")
        self.assert_rejected("staging tag as release input")

    # --- signing material in Community CI ---------------------------------

    def test_rejects_signing_material_in_community_ci(self):
        write(self.root, ".github/workflows/ci.yml", "run: openssl pkcs8 -topk8")
        self.assert_rejected("Community CI signing material")

    def test_rejects_signing_key_secret_in_community_ci(self):
        write(
            self.root,
            ".github/workflows/ci.yml",
            "env:\n  SIGNING_KEY: ${{ secrets.COMMUNITY_SIGNING_KEY }}\n",
        )
        self.assert_rejected("Community CI signing material")

    def test_rejects_private_key_material_anywhere(self):
        pem_header = "-----BEGIN " + "PRIVATE KEY-----"
        write(self.root, "keys/dev.pem", pem_header + "\nabc\n")
        self.assert_rejected("Community CI signing material")

    def test_allows_signing_prose_outside_ci(self):
        write(self.root, "docs/policy.md", "PKCS#8 and signing-key material never enter Community CI.\n")
        self.assert_accepted()

    # --- deferred CLI rename ----------------------------------------------

    def test_rejects_deferred_cli_rename(self):
        write(self.root, "README.md", "Run `axloop crawler` instead of the old command.")
        self.assert_rejected("deferred CLI rename")

    def test_rejects_cli_rename_in_markdown_shell_block(self):
        write(self.root, "docs/usage.md", "Start it with:\n\n```bash\naxloop crawler --once\n```\n")
        self.assert_rejected("deferred CLI rename")

    def test_allows_quoted_test_fixture_in_non_shell_fence(self):
        write(
            self.root,
            "docs/design.md",
            "Required rejection case:\n\n```python\n"
            "write(root, \"README.md\", \"Run `axloop crawler` instead of the old command.\")\n"
            "write(root, \".community-release.json\", '{\"published_at\":\"2026-09-02\"}')\n"
            "```\n",
        )
        self.assert_accepted()

    def test_rejects_cli_rename_migration_code(self):
        write(
            self.root,
            "scripts/rename_cli.py",
            "text = open('cli.py').read()\nopen('cli.py', 'w').write(text.replace('radar', 'crawler'))\n",
        )
        self.assert_rejected("deferred CLI rename")

    def test_rejects_cli_rename_in_workflow(self):
        write(self.root, ".github/workflows/ci.yml", "run: sed -i 's/radar/crawler/g' cli.py\n")
        self.assert_rejected("deferred CLI rename")

    # --- copied factory content ---------------------------------------------

    def test_rejects_copied_factory_workflow(self):
        write(self.root, ".github/workflows/community-bundles.yml", "name: bundles\non: push\n")
        self.assert_rejected("copied factory workflow")

    def test_rejects_factory_workflow_language(self):
        write(self.root, ".github/workflows/ci.yml", "run: python tools/community_signing_request.py\n")
        self.assert_rejected("copied factory workflow")

    def test_rejects_src_tree(self):
        write(self.root, "src/axloop/__init__.py", "")
        self.assert_rejected("forbidden implementation tree")

    def test_rejects_tools_tree(self):
        write(self.root, "tools/community_native_build.py", "print('build')\n")
        self.assert_rejected("forbidden implementation tree")

    def test_rejects_packaging_tree(self):
        write(self.root, "packaging/msi/build.wxs", "<Wix/>\n")
        self.assert_rejected("forbidden implementation tree")

    def test_rejects_enterprise_project_file(self):
        write(self.root, "pyproject.toml", "[project]\nname = 'axloop'\n")
        self.assert_rejected("enterprise project file")

    def test_reports_all_violations_before_exiting(self):
        write(self.root, "src/axloop/__init__.py", "")
        write(self.root, "docs/boundary.md", OBSOLETE_LOCATION)
        output = self.assert_rejected("forbidden implementation tree")
        self.assertIn("obsolete boundary language", output)


RELEASE_ARCHIVE = "axloop-community-darwin-arm64-3a7bfeeb.tar.gz"
RELEASE_CHECKSUMS = "axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS"
RELEASE_ARCHIVE_SHA256 = "27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043"

UNPUBLISHED_CLAIM = re.compile(
    r"(?im)(?:\bno\b[^\n]{0,40}\brelease\b[^\n]{0,30}\bpublished\b|"
    r"\bno published release\b|\bnot yet published\b|\bunpublished\b)"
)
AFFIRMATIVE_OTHER_PLATFORM = re.compile(
    r"(?im)(?:\b(?:linux|windows)\b(?:(?!\b(?:no|not)\b)[^.\n]){0,40}"
    r"\b(?:published|available|released)\b|"
    r"\b(?:published|available|released)\b(?:(?!\b(?:no|not)\b)[^.\n]){0,40}"
    r"\b(?:linux|windows)\b)"
)


class VisitorJourneyTests(unittest.TestCase):
    """The real repository documents form one consistent release-discovery contract."""

    def setUp(self) -> None:
        self.readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.guide = (REPO_ROOT / "docs/COMMUNITY_RELEASES.md").read_text(encoding="utf-8")

    def visitor_documents(self) -> dict[str, str]:
        return {
            "README": self.readme,
            "CHANGELOG": self.changelog,
            "Community release guide": self.guide,
        }

    def test_readme_has_stranger_first_run_and_public_funnel(self):
        readme = self.readme
        self.assertIn("First run", readme)
        self.assertIn("https://www.axloop.ai", readme)
        self.assertIn("CHANGELOG.md", readme)
        self.assertIn("docs/COMMUNITY_RELEASES.md", readme)

        self.assertNotRegex(readme, UNPUBLISHED_CLAIM, "README still claims unpublished")
        self.assertNotRegex(
            readme,
            AFFIRMATIVE_OTHER_PLATFORM,
            "README claims an unavailable platform is published",
        )

        self.assertIn("v0.1.0", readme)
        self.assertIn("darwin-arm64", readme)
        self.assertIn(LATEST_RELEASE, readme)
        self.assertIn(RELEASE_ARCHIVE, readme)
        self.assertIn(RELEASE_CHECKSUMS, readme)
        self.assertIn(RELEASE_ARCHIVE_SHA256, readme)
        self.assertIn("bin/axloop-community", readme)
        self.assertIn(PUBLIC_SITE, readme)

    def test_readme_does_not_present_source_checkout_as_install(self):
        lowered = self.readme.lower()
        self.assertNotIn("git clone", lowered)
        self.assertNotIn("pip install", lowered)
        self.assertNotIn("curl ", lowered)
        self.assertNotIn("```", self.readme)

    def test_release_docs_are_honest_and_consistent(self):
        changelog = self.changelog
        release_guide = self.guide

        for label, text in self.visitor_documents().items():
            self.assertNotRegex(text, UNPUBLISHED_CLAIM, f"{label} still claims unpublished")
            self.assertNotRegex(
                text,
                AFFIRMATIVE_OTHER_PLATFORM,
                f"{label} claims an unavailable platform is published",
            )

        self.assertRegex(changelog, r"(?m)^## \[Unreleased\]\s*$")
        self.assertRegex(changelog, r"(?m)^## \[0\.1\.0\] - 2026-09-02\s*$")
        self.assertIn("darwin-arm64", changelog)

        self.assertIn("v0.1.0", release_guide)
        self.assertIn("darwin-arm64", release_guide)
        self.assertIn(LATEST_RELEASE, release_guide)
        self.assertIn("CHANGELOG.md", release_guide)

    def test_documents_contain_no_prohibited_values(self):
        scanned = dict(self.visitor_documents())
        for path in sorted((REPO_ROOT / "docs" / "superpowers").rglob("*.md")):
            scanned[path.relative_to(REPO_ROOT).as_posix()] = path.read_text(encoding="utf-8")
        for label, text in scanned.items():
            lowered = text.lower()
            for sensitive in (PRIVATE_ORG, PRIVATE_NAME, OBSOLETE_LOCATION, STAGING_TAG):
                self.assertNotIn(sensitive, lowered, f"{label} contains a protected value")
            self.assertIsNone(re.search(r"\bcrawler\b", lowered), label)
            self.assertIsNone(re.search(r"utm_[a-z]+=", lowered), label)

    def test_real_repository_passes_checker(self):
        result = run_checker(REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
