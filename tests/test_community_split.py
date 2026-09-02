"""Boundary tests for scripts/check-community-split.py.

Each rejection test starts from a minimal valid Community tree, adds exactly
one forbidden condition, and asserts a nonzero exit plus a diagnostic that
names the violated rule.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "scripts" / "check-community-split.py"

README = """# AxLoop Community

Community artifacts and GitHub Releases live here: https://github.com/axloop/axloop-community.
Enterprise stays in https://github.com/ascendantventures/axloop-edge-poc.
No Community release has been published from this repository yet.
"""

RELEASES_DOC = """# Community releases

No Community release has been published from this repository yet. The enterprise
Aug 29 staging draft tagged `community-acceptance-staging-2026-08-29` must not be
used, copied, retagged, attached, or published.

The CLI `radar`→`crawler` rename (radar→crawler) is later and is not part of this split.
PKCS#8 never enters this repository or CI.
"""

DRAFT_ONLY_WORKFLOW = """name: community-draft-release
on:
  workflow_dispatch:
    inputs:
      tag:
        description: New Community-local release tag
        required: true
permissions:
  contents: write
jobs:
  attach:
    runs-on: ubuntu-latest
    steps:
      - name: Create draft release
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release create "${{ inputs.tag }}" --draft --repo "${{ github.repository }}" --notes "draft"
      - name: Attach accepted artifacts
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release upload "${{ inputs.tag }}" handoff/*.tar.gz --repo "${{ github.repository }}"
"""


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_valid_tree(root: Path) -> None:
    write(root, "README.md", README)
    write(root, "docs/COMMUNITY_RELEASES.md", RELEASES_DOC)


def run_checker(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)],
        capture_output=True,
        text=True,
    )


class CommunitySplitCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_valid_tree(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def assert_rejected(self, rule: str) -> subprocess.CompletedProcess:
        result = run_checker(self.root)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(rule, output)
        return result

    def assert_accepted(self) -> subprocess.CompletedProcess:
        result = run_checker(self.root)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("PASS", output)
        return result

    def test_rejects_enterprise_src_copy(self):
        write(self.root, "src/axloop/__init__.py", "")
        self.assert_rejected("enterprise-tree")

    def test_rejects_enterprise_tools_copy(self):
        write(self.root, "tools/community_native_build.py", "print('build')\n")
        self.assert_rejected("enterprise-tree")

    def test_rejects_enterprise_project_file_copy(self):
        write(self.root, "pyproject.toml", "[project]\nname = 'axloop'\n")
        self.assert_rejected("enterprise-project-file")

    def test_rejects_factory_workflow_copy(self):
        write(self.root, ".github/workflows/community-bundles.yml", "name: bundles\non: push\n")
        self.assert_rejected("factory-workflow")

    def test_rejects_release_publish_step(self):
        workflow = DRAFT_ONLY_WORKFLOW + (
            "      - name: Publish\n"
            "        run: gh release edit \"${{ inputs.tag }}\" --draft=false\n"
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("release-publish")

    def test_rejects_draft_false_in_workflow(self):
        workflow = DRAFT_ONLY_WORKFLOW + (
            "      - uses: softprops/action-gh-release@v2\n"
            "        with:\n"
            "          draft: false\n"
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("release-publish")

    def test_rejects_release_create_without_draft(self):
        workflow = DRAFT_ONLY_WORKFLOW.replace(" --draft", "")
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("release-publish")

    def test_rejects_aug_29_tag_as_input(self):
        workflow = DRAFT_ONLY_WORKFLOW.replace(
            "        required: true\n",
            "        required: true\n        default: community-acceptance-staging-2026-08-29\n",
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("staging-tag")

    def test_allows_aug_29_tag_disclaimer_in_markdown(self):
        # The valid fixture already disclaims the tag in docs/COMMUNITY_RELEASES.md.
        self.assert_accepted()

    def test_rejects_radar_to_crawler_change(self):
        write(
            self.root,
            "scripts/rename_cli.py",
            "import re\n"
            "text = open('cli.py').read()\n"
            "open('cli.py', 'w').write(text.replace('radar', 'crawler'))\n",
        )
        self.assert_rejected("cli-rename")

    def test_rejects_radar_to_crawler_in_workflow(self):
        workflow = DRAFT_ONLY_WORKFLOW + (
            "      - name: Rename CLI\n"
            "        run: sed -i 's/radar/crawler/g' cli.py\n"
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("cli-rename")

    def test_rejects_signing_key_in_ci(self):
        workflow = DRAFT_ONLY_WORKFLOW + (
            "      - name: Sign\n"
            "        env:\n"
            "          SIGNING_KEY: ${{ secrets.COMMUNITY_SIGNING_KEY }}\n"
            "        run: openssl pkeyutl -sign -inkey key.pem\n"
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("signing-key")

    def test_rejects_pkcs8_material_in_ci(self):
        workflow = DRAFT_ONLY_WORKFLOW + (
            "      - name: Key\n"
            "        run: echo '-----BEGIN PRIVATE KEY-----' > key.pem\n"
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("signing-key")

    def test_rejects_enterprise_checkout_in_workflow(self):
        workflow = DRAFT_ONLY_WORKFLOW + (
            "      - uses: actions/checkout@v4\n"
            "        with:\n"
            "          repository: ascendantventures/axloop-edge-poc\n"
        )
        write(self.root, ".github/workflows/community-draft-release.yml", workflow)
        self.assert_rejected("enterprise-checkout")

    def test_reports_all_violations_before_exiting(self):
        write(self.root, "src/axloop/__init__.py", "")
        write(self.root, ".github/workflows/community-inputs.yml", "name: inputs\non: push\n")
        result = self.assert_rejected("enterprise-tree")
        self.assertIn("factory-workflow", result.stdout + result.stderr)

    def test_accepts_docs_only_tree(self):
        self.assert_accepted()

    def test_accepts_explicitly_draft_only_workflow(self):
        write(self.root, ".github/workflows/community-draft-release.yml", DRAFT_ONLY_WORKFLOW)
        self.assert_accepted()


if __name__ == "__main__":
    unittest.main()
