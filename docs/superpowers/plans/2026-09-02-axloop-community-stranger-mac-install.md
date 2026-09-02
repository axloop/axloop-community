# AxLoop Community Stranger-First Mac Install Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public Apple Silicon Community install journey Finder-first, while preventing visitor documentation from claiming that journey before a notarized installer is truly published.

**Architecture:** Treat packaging/publication and Community visitor copy as separate trust boundaries. Nolan supplies the notarized package outside Community CI, Abe controls publication, and the Community writer changes only real-file visitor tests plus three documents after the live-asset gate clears; the existing checker and fixtures remain fail-closed and unchanged.

**Tech Stack:** Markdown, Python standard-library `unittest`, the existing `scripts/check-community-split.py` checker, GitHub Releases, and a notarized macOS Apple Silicon `.pkg` installer.

**Spec:** `docs/superpowers/specs/2026-09-02-axloop-community-stranger-mac-install-design.md`

## Global Constraints

- This plan/spec authoring stream changes only the two Markdown files under `docs/superpowers/` named in the request.
- This is a docs-and-tests-only implementation. Do not change application runtime code.
- Base the work on `axloop/axloop-community` main at `81c55c0eebee70d6e4364dda24605f0c435f722d`.
- Do not merge leftover plan pull requests #1 or #3, or the separate honesty pull request #5, into this work.
- Kit must GitHub COMMENT-sign this plan after Imani and Reed. APPROVE does not count because `ajrrac` is a shared login. Chat approval does not count.
- After Kit's COMMENT and the live-installer gate, Elena launches Cursor cloud Claude Fable 5.1 (`claude-fable-5-1`) at effort low against `axloop/axloop-community` main.
- Kit does not write application code. Jules is off.
- The visitor path is Apple Silicon only: open `https://github.com/axloop/axloop-community/releases/latest`, download the published installer, open it in Finder, and run Community.
- Enterprise remains `https://www.axloop.ai`.
- Recommend a notarized Apple Silicon `.pkg` installer. Packaging and notarization are Nolan's desk, outside Community CI and outside this writer's scope.
- The private factory supplies the payload and writes `manifest.sig` first. Do not name or expose its GitHub identity.
- Do not add a workflow, `.github` content, signing material, credentials, keys, a release, a tag, an asset upload, or another operating-system artifact.
- At plan time the live `v0.1.0` release contains only the `darwin-arm64` archive and checksum asset. This stream does not replace it.
- Stop before editing if latest still lacks Nolan's published notarized installer. Never describe the current archive as that installer.
- TDD order is mandatory: invert only real-file `VisitorJourneyTests` and observe red; then edit `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` to green.
- Keep `scripts/check-community-split.py` unchanged and fail-closed. Preserve every checker fixture tree.
- README contains no fenced code blocks and does not present clone, pip, or a command-line download as installation.
- Do not claim a Linux or Windows artifact is published.
- Do not add a factory GitHub reference, a staging tag, publication commands, or tag-publication commands to Community instruction lines.
- Sensitive forbidden values stay assembled from the existing fragments. Do not literalize them.
- Do not invent a package version or fill any review COMMENT slot.
- Do not merge or publish anything unless Abe separately directs it.

---

### Task 1: Enforce authorization, base, and live-installer gates

**Files:**

- Read: `docs/superpowers/specs/2026-09-02-axloop-community-stranger-mac-install-design.md`
- Read: `docs/superpowers/plans/2026-09-02-axloop-community-stranger-mac-install.md`
- Read: `README.md`
- Read: `docs/COMMUNITY_RELEASES.md`
- No files changed

**Interfaces:**

- Consumes: Kit's GitHub COMMENT after Imani and Reed, the locked base SHA, Nolan's package/notarization evidence, and the public latest-release asset list.
- Produces: A written go/no-go checkpoint for Elena. A no-go ends execution with no repository edits.

- [ ] **Step 1: Confirm the worker and review gate**

Confirm that Elena launched Cursor cloud with model `claude-fable-5-1`, effort low, against `axloop/axloop-community` main. On GitHub, confirm that the plan has COMMENTs in order from Imani, Reed, and Kit. Treat a review approval or chat message as insufficient.

- [ ] **Step 2: Confirm the exact base**

Run:

```bash
git rev-parse HEAD
```

Expected: exactly `81c55c0eebee70d6e4364dda24605f0c435f722d`. If it differs, stop and report the actual SHA to Abe; do not merge another branch to manufacture the expected state.

- [ ] **Step 3: Inspect the public latest release in a browser**

Open `https://github.com/axloop/axloop-community/releases/latest`. Record the release tag and asset names in the work log. Verify that a published Apple Silicon installer is present and that it is distinct from the `v0.1.0` archive and checksum asset.

Expected at plan-authoring time: the gate is closed because only the current archive path is live. If that remains true at execution time, stop with: “Blocked: latest does not yet contain Nolan's notarized Apple Silicon installer; no visitor files changed.”

- [ ] **Step 4: Verify Nolan's package evidence**

Confirm Nolan's evidence identifies the same published asset and records an attended Developer ID/notarization result plus an Apple Silicon Finder-open/run check. Confirm the packaged bundle retained the private factory's `manifest.sig` verification.

Expected: all evidence refers to one published installer. If any part is missing or mismatched, stop without editing files.

- [ ] **Step 5: Freeze the allowed implementation scope**

Record this exact allowlist before editing:

```text
tests/test_community_split.py
README.md
CHANGELOG.md
docs/COMMUNITY_RELEASES.md
```

Expected: no runtime, fixture, checker, automation, packaging, or release file is on the list.

### Task 2: Invert the real-file visitor contract and prove red

**Files:**

- Modify: `tests/test_community_split.py` within `VisitorJourneyTests`, plus only the standard-library imports that class requires
- Preserve: `scripts/check-community-split.py`
- Preserve: all fixture trees used by `tests/test_community_split.py`

**Interfaces:**

- Consumes: The gate-clear record from Task 1 and the existing real-file loading helpers, fragment-assembled sensitive checks, and checker invocation in `tests/test_community_split.py`.
- Produces: Real-file visitor assertions that are red against the pre-change README/release docs and encode the Finder-first contract.

- [ ] **Step 1: Read the existing test boundaries before editing**

Locate `VisitorJourneyTests`, its repository-root helper, its real-file readers, and the existing fragment-assembled forbidden-value checks. Identify fixture-only test classes and fixture directories so the edit cannot spill into them.

Expected: the patch target is only the real-file `VisitorJourneyTests` class and any standard-library imports it requires. Do not change helper semantics, fixtures, or the checker.

- [ ] **Step 2: Add or invert the Finder-first README assertion**

Using the existing repository-root/read helper names where they already exist, make the real-file assertion equivalent to this standard-library test:

```python
def test_readme_first_run_is_finder_first(self):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^## First run\s*$\n(.*?)(?=^##\s|\Z)",
        readme,
    )
    self.assertIsNotNone(match, "README must have a First run section")
    first_run = match.group(1).lower()
    for required in (
        "https://github.com/axloop/axloop-community/releases/latest",
        "apple silicon",
        "installer",
        "finder",
        "download",
        "open",
        "run",
    ):
        self.assertIn(required, first_run)
    for terminal_requirement in (
        r"\bcurl\b",
        r"\bshasum\b",
        r"\btar\b",
        r"\bxattr\b",
        r"\bdoctor\b",
    ):
        self.assertNotRegex(first_run, terminal_requirement)
```

If `ROOT`, `re`, or the real-file reader already has another local name, reuse it instead of defining a duplicate. The behavior and failure messages remain as shown.

- [ ] **Step 3: Enforce README shape and installation vocabulary**

Add or invert an assertion equivalent to:

````python
def test_readme_has_no_developer_install_path(self):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    lowered = readme.lower()
    self.assertNotIn("```", readme)
    for forbidden in ("git " + "clone", "pip " + "install", "cu" + "rl"):
        self.assertNotIn(forbidden, lowered)
````

This deliberately checks the real README, not fixture READMEs. Keep the split spelling for sensitive scanning patterns already represented that way in the file.

- [ ] **Step 4: Enforce platform and archive honesty across visitor documents**

Add or invert assertions equivalent to:

```python
def test_visitor_docs_do_not_claim_unpublished_platforms(self):
    visitor_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("README.md", "CHANGELOG.md", "docs/COMMUNITY_RELEASES.md")
    )
    claim = re.compile(
        r"(?is)(?:\b(?:linux|windows)\b.{0,80}\b(?:published|available|download|installer|release)\b|"
        r"\b(?:published|available|download|installer|release)\b.{0,80}\b(?:linux|windows)\b)"
    )
    self.assertIsNone(claim.search(visitor_text))

def test_v010_archive_is_not_described_as_the_finder_installer(self):
    visitor_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("README.md", "CHANGELOG.md", "docs/COMMUNITY_RELEASES.md")
    )
    for paragraph in re.split(r"\n\s*\n", visitor_text.lower()):
        finder_claim = "finder" in paragraph or "installer" in paragraph
        old_archive = "v0.1.0" in paragraph and (
            "tar.gz" in paragraph or "sha256sums" in paragraph
        )
        self.assertFalse(
            finder_claim and old_archive,
            "v0.1.0 archive must not be described as the Finder installer",
        )
```

Historical archive facts may remain in a separate historical paragraph. The live installer claim must never attach to that old archive.

- [ ] **Step 5: Retain the real-tree fail-closed checker assertion**

Keep the existing assertion that runs `scripts/check-community-split.py` against the real repository tree. If `VisitorJourneyTests` lacks that assertion, add the following without changing the checker:

```python
def test_real_tree_passes_fail_closed_checker(self):
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check-community-split.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
```

Reuse existing imports and invocation arguments if present. This retains enforcement for factory GitHub references, staging tags, forbidden instruction lines, signing material, and factory trees without putting sensitive literal values in this test.

- [ ] **Step 6: Run only the real-file visitor class and prove red**

Run:

```bash
python3 -m unittest tests.test_community_split.VisitorJourneyTests -v
```

Expected: FAIL in the newly inverted Finder-first assertions because the real visitor files still describe the pre-installer path. Confirm failures are assertion failures against `README.md`, `CHANGELOG.md`, or `docs/COMMUNITY_RELEASES.md`, not import, syntax, fixture, or checker errors. Do not commit the red-only state.

### Task 3: Make the three visitor documents satisfy the Finder contract

**Files:**

- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/COMMUNITY_RELEASES.md`
- Do not modify any test fixture or checker file

**Interfaces:**

- Consumes: The red assertions from Task 2 and the verified published-installer evidence from Task 1.
- Produces: Minimal, mutually consistent visitor copy for a published notarized Apple Silicon installer.

- [ ] **Step 1: Replace the README install/First run path**

Preserve unrelated accurate project material, but make the install and First run copy read exactly as follows. If the README already has an install heading, replace its visitor steps rather than creating a competing path.

````markdown
## Install

AxLoop Community is published for Mac computers with Apple silicon.

## First run

1. Open the [latest Community release](https://github.com/axloop/axloop-community/releases/latest).
2. Download the published Apple Silicon installer.
3. Open the installer in Finder and follow the macOS prompts.
4. Open AxLoop Community in Finder and run it.

For AxLoop Enterprise, visit [axloop.ai](https://www.axloop.ai).
````

Remove any competing README install path based on source checkout, Python package installation, shell download, archive/checksum handling, quarantine removal, or diagnostic bypass flags. Do not add any fenced example to the README itself.

- [ ] **Step 2: Add the visitor change to the existing unreleased changelog area**

Under the existing unreleased heading, add this bullet:

````markdown
- Changed the Apple Silicon installation journey to download the published installer from the latest Community release, open it in Finder, and run Community without Terminal setup.
````

If no unreleased heading exists, add `## Unreleased`; that heading is not a package version. Preserve accurate historical `v0.1.0` facts, but keep them in a separate historical paragraph or section and never describe that archive as this installer.

- [ ] **Step 3: Align the Community releases guide**

Preserve unrelated accurate release policy, but replace contradictory visitor/install guidance with these sections:

````markdown
## Community install

AxLoop Community is published for Mac computers with Apple silicon. Visitors install from the [latest Community release](https://github.com/axloop/axloop-community/releases/latest): download the published Apple Silicon installer, open it in Finder, follow the macOS prompts, then open and run AxLoop Community.

## Installer trust boundary

The visitor-facing package is notarized before publication. Nolan owns attended Developer ID packaging and notarization outside Community CI. The private factory produces the payload and writes `manifest.sig` before that package is wrapped; packaging does not replace payload verification.

The Community repository contains no signing material and no signing or notarization workflow. Visitor documentation may advertise the installer only while the latest public release actually provides Nolan's verified package.

## Enterprise

AxLoop Enterprise is available at [axloop.ai](https://www.axloop.ai).
````

Do not add claims for other published platforms. Do not add publication instructions, asset-upload instructions, signing steps, secret setup, or a package version.

- [ ] **Step 4: Run the focused class and prove green**

Run:

```bash
python3 -m unittest tests.test_community_split.VisitorJourneyTests -v
```

Expected: PASS for every test in `VisitorJourneyTests`, including the real-tree checker assertion.

- [ ] **Step 5: Commit the completed red-green unit**

Run:

```bash
git add tests/test_community_split.py README.md CHANGELOG.md docs/COMMUNITY_RELEASES.md
git commit -m "docs: make Apple Silicon install Finder-first"
```

Expected: one commit containing only the four allowlisted visitor-contract files. Do not merge or publish it.

### Task 4: Verify scope, fail-closed behavior, and handoff

**Files:**

- Verify: `tests/test_community_split.py`
- Verify: `README.md`
- Verify: `CHANGELOG.md`
- Verify: `docs/COMMUNITY_RELEASES.md`
- Verify unchanged: `scripts/check-community-split.py`
- Verify unchanged: all fixture trees

**Interfaces:**

- Consumes: The green visitor-contract commit from Task 3.
- Produces: Fresh test and scope evidence for human review; it does not merge, publish, tag, or modify a release.

- [ ] **Step 1: Run the complete Superpowers test module**

Run:

```bash
python3 -m unittest tests.test_community_split -v
```

Expected: PASS with zero failures and zero errors.

- [ ] **Step 2: Run the fail-closed checker directly**

Run:

```bash
python3 scripts/check-community-split.py
```

Expected: exit 0. Any nonzero result blocks handoff; fix only an allowlisted visitor-contract file or revert the out-of-scope change that caused it. Do not weaken the checker.

- [ ] **Step 3: Inspect the final file scope**

Run:

```bash
git diff --name-only 81c55c0eebee70d6e4364dda24605f0c435f722d...HEAD
```

Expected implementation file list:

```text
CHANGELOG.md
README.md
docs/COMMUNITY_RELEASES.md
tests/test_community_split.py
```

The plan/spec documentation may already exist on the base branch. Any other implementation path is a scope failure. In particular, there must be no runtime, `.github`, fixture, checker, signing, packaging, or release-automation change.

- [ ] **Step 4: Review the contract line by line**

Confirm all of the following from the final files and fresh command output:

- README First run links latest, says Apple Silicon, download, installer, Finder, open, and run.
- README has no fence and no source-, Python-, or shell-based installation path.
- Visitor docs do not claim another published platform.
- No visitor paragraph associates the `v0.1.0` archive/checksum with the Finder installer.
- The checker still rejects private-factory GitHub references, staging tags, forbidden instruction lines, signing material, deferred crawlers, and factory trees.
- The fixture trees and checker have no diff.
- No package version was invented.

Expected: every item has direct file or command evidence. If any item lacks evidence, do not claim completion.

- [ ] **Step 5: Hand off for review without merging or publishing**

Report the base SHA, commit SHA, the verified latest-release installer asset name, Nolan evidence reference, focused and full test counts, checker result, and exact changed-file list. Hand the branch back to Kit and Abe for review. Do not merge, modify a release, or create an additional artifact.

## Required GitHub COMMENT gates

Imani COMMENT:

Reed COMMENT:

Kit COMMENT:
