# AxLoop Community v0.1.0 Visitor-Docs Honesty Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the AxLoop Community visitor journey tell the truth about the live v0.1.0 Mac Apple Silicon release and keep that truth enforced by tests.

**Architecture:** Invert only the real-file `VisitorJourneyTests` to establish a red documentation contract, then update `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` as one green documentation unit. Preserve the existing fail-closed checker and its fixture trees; do not add release automation or touch application runtime code.

**Tech Stack:** Markdown, Python standard-library `unittest`, and the existing `scripts/check-community-split.py` policy checker.

**Spec:** `docs/superpowers/specs/2026-09-02-axloop-community-v010-honesty-design.md`

## Global Constraints

- Execute against `axloop/axloop-community` main based on `81c55c0eebee70d6e4364dda24605f0c435f722d`.
- Do not merge leftover plan PR #1 or #3 into this work.
- This is documentation-contract work only: change `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md`; do not change application runtime code.
- Kit must GitHub COMMENT-sign this plan before execution. A GitHub `APPROVE` review does not count because `ajrrac` is a shared login.
- After that COMMENT, Elena launches Cursor cloud Claude Fable 5.1 (`claude-fable-5-1`) effort low against Community main.
- Kit does not write application code. Jules remains off. Nolan is involved only if a workflow appears; the default and required implementation adds no workflow.
- Do not add `.github`, a release, a tag, a workflow, signing material, or a Linux or Windows asset.
- Do not publish or modify any release. Abe alone controls any later merge decision.
- The live release is `v0.1.0`, release ID `381577289`, published `2026-09-02T21:12:15Z`, public, final, and not a prerelease.
- Its title is `AxLoop Community 0.1.0 for Mac (Apple Silicon)` and its latest-release path is https://github.com/axloop/axloop-community/releases/latest.
- The only published platform is Mac Apple Silicon, represented by `darwin-arm64`; do not claim Linux or Windows is published or available.
- The archive is `axloop-community-darwin-arm64-3a7bfeeb.tar.gz`; its SHA-256 is `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`.
- The adjacent checksum asset is `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`.
- The named path ends by running `bin/axloop-community`; the enterprise destination remains https://www.axloop.ai.
- `README.md` has no fenced code blocks and does not present clone, pip, or curl commands as installation.
- Checker fixtures may keep an unpublished mini README. Only `VisitorJourneyTests` read and enforce the real visitor files.
- Keep sensitive values assembled from fragments in tests and the checker. In public prose say only `the private factory`; include no protected owner, repository name, URL, obsolete slogan, staging-tag value, publish instruction, or private-key block.
- Do not weaken `scripts/check-community-split.py`, invent pack versions, or fill the Imani, Reed, or Kit COMMENT slots.
- The Superpowers tests must FAIL if a real visitor document still claims unpublished status.
- The Superpowers tests must FAIL if required `v0.1.0`, `darwin-arm64`, or latest-release facts are missing.
- The Superpowers tests must FAIL if Linux or Windows is affirmatively claimed as published or available.
- The Superpowers tests must FAIL if a scanned document refers to the private factory or contains a staging tag.
- The Superpowers tests must FAIL if `README.md` contains a fenced code block or presents clone, pip, or curl commands as installation.

---

## Execution gate

Do not begin Task 1 until Kit's GitHub COMMENT is present on this plan. Keep these slots blank in the plan artifact:

| Reviewer | GitHub COMMENT |
| --- | --- |
| Imani | |
| Reed | |
| Kit | |

### Task 1: Invert the real visitor contract and prove red

**Files:**

- Modify: `tests/test_community_split.py`
- Read: `README.md`
- Read: `CHANGELOG.md`
- Read: `docs/COMMUNITY_RELEASES.md`
- Leave unchanged: checker fixture trees in `tests/test_community_split.py`

**Interfaces:**

- Consumes: the existing file-loading setup and assembled sensitive-value checks in `VisitorJourneyTests`.
- Produces: real-file assertions that define the published v0.1.0 visitor contract for Task 2.

- [ ] **Step 1: Locate the live-file assertions and preserve fixture isolation**

Open `VisitorJourneyTests.test_readme_has_stranger_first_run_and_public_funnel`, `VisitorJourneyTests.test_release_docs_are_honest_and_consistent`, `VisitorJourneyTests.test_readme_does_not_present_source_checkout_as_install`, and `VisitorJourneyTests.test_documents_contain_no_prohibited_values`. Confirm that the first two load the real root files. Do not change unpublished text inside checker fixture trees.

- [ ] **Step 2: Replace the unpublished assertions with exact published-release assertions**

Within the existing methods, retain their current real-file loading expressions and use the following contract. Match variable names to the already-loaded README, changelog, and release-guide strings; do not create a second file-discovery mechanism.

```python
unpublished_claim = re.compile(
    r"(?im)(?:\bno\b[^\n]{0,40}\brelease\b[^\n]{0,30}\bpublished\b|"
    r"\bno published release\b|\bnot yet published\b|\bunpublished\b)"
)
affirmative_other_platform = re.compile(
    r"(?im)(?:\b(?:linux|windows)\b(?:(?!\b(?:no|not)\b)[^.\n]){0,40}"
    r"\b(?:published|available|released)\b|"
    r"\b(?:published|available|released)\b(?:(?!\b(?:no|not)\b)[^.\n]){0,40}"
    r"\b(?:linux|windows)\b)"
)

for label, text in {
    "README": readme,
    "CHANGELOG": changelog,
    "Community release guide": release_guide,
}.items():
    self.assertNotRegex(text, unpublished_claim, f"{label} still claims unpublished")
    self.assertNotRegex(
        text,
        affirmative_other_platform,
        f"{label} claims an unavailable platform is published",
    )

self.assertIn("v0.1.0", readme)
self.assertIn("darwin-arm64", readme)
self.assertIn("https://github.com/axloop/axloop-community/releases/latest", readme)
self.assertIn("axloop-community-darwin-arm64-3a7bfeeb.tar.gz", readme)
self.assertIn("axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS", readme)
self.assertIn(
    "27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043",
    readme,
)
self.assertIn("bin/axloop-community", readme)
self.assertIn("https://www.axloop.ai", readme)

self.assertRegex(changelog, r"(?m)^## \[Unreleased\]\s*$")
self.assertRegex(changelog, r"(?m)^## \[0\.1\.0\] - 2026-09-02\s*$")
self.assertIn("darwin-arm64", changelog)

self.assertIn("v0.1.0", release_guide)
self.assertIn("darwin-arm64", release_guide)
self.assertIn(
    "https://github.com/axloop/axloop-community/releases/latest",
    release_guide,
)
```

Delete the old regex requiring unpublished language and the old assertion forbidding a released-version heading.

- [ ] **Step 3: Retain the README installation guard unchanged**

Keep `test_readme_does_not_present_source_checkout_as_install` enforcing all four existing rules: no clone command, no pip install, no curl install, and no triple-backtick fence in the real README.

- [ ] **Step 4: Retain and scope the prohibited-value guard**

Keep the existing assembled-fragment checks in `test_documents_contain_no_prohibited_values` for the private factory, obsolete wording, staging-tag value, and tracking parameters. Ensure its scanned document set still covers the three live visitor files and the Markdown under `docs/superpowers/`. Do not copy any assembled protected value into a public document.

- [ ] **Step 5: Run the focused tests and verify the red phase**

```text
python3 -m unittest tests.test_community_split.VisitorJourneyTests -v
```

Expected: FAIL against base `81c55c0eebee70d6e4364dda24605f0c435f722d` because the real docs still claim no release is published and omit required v0.1.0 release facts. Confirm that failures are honesty-contract failures, not import errors, syntax errors, fixture failures, or protected-value failures.

- [ ] **Step 6: Record the red-test checkpoint**

Record only `tests/test_community_split.py` in the writer branch with checkpoint message `test: invert community release honesty contract`. Do not merge or publish anything.

### Task 2: Make all three visitor documents green

**Files:**

- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/COMMUNITY_RELEASES.md`
- Test: `tests/test_community_split.py`

**Interfaces:**

- Consumes: the exact v0.1.0 contract established by Task 1.
- Produces: one consistent visitor journey across the README, changelog, and Community release guide.

- [ ] **Step 1: Replace the README's unpublished story with the named First run path**

Use this content model in `README.md`, adapting only its surrounding heading level to the existing document. Keep it as prose and list markup; do not wrap any part in a fenced block.

> **First run**
>
> AxLoop Community v0.1.0 is published for Mac with Apple Silicon only (`darwin-arm64`).
>
> 1. Open the [latest release](https://github.com/axloop/axloop-community/releases/latest).
> 2. Download `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`.
> 3. Check that the archive SHA-256 is `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`.
> 4. Unpack the archive.
> 5. From the unpacked directory, run `bin/axloop-community`.
>
> For enterprise AxLoop, visit https://www.axloop.ai.

Remove every live README sentence saying that no release is published. Do not add source-checkout, pip, or network-command installation alternatives.

- [ ] **Step 2: Add the v0.1.0 Keep a Changelog entry**

Keep the existing changelog preamble and `## [Unreleased]` heading for later work. Directly below that section, add:

```markdown
## [0.1.0] - 2026-09-02

### Added

- First AxLoop Community install for Mac Apple Silicon (`darwin-arm64`), available from the [v0.1.0 release](https://github.com/axloop/axloop-community/releases/tag/v0.1.0).
```

Remove the unpublished claim. If the file uses link definitions, keep them consistent by pointing `[0.1.0]` to the public v0.1.0 release page and `[Unreleased]` to comparison beginning at v0.1.0. Do not invent another version.

- [ ] **Step 3: Rewrite the Community release guide around the live release**

Make `docs/COMMUNITY_RELEASES.md` state all of the following in short visitor-facing prose:

- v0.1.0 is published and is the first Community install.
- It supports Mac Apple Silicon only, identified as `darwin-arm64`.
- The visitor starts at https://github.com/axloop/axloop-community/releases/latest.
- The visitor downloads `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`, checks archive SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`, unpacks, and runs `bin/axloop-community`.
- The enterprise destination is https://www.axloop.ai.
- This documentation change creates no release, tag, workflow, or Linux or Windows asset.

Remove the unpublished story and every staging-tag mention. Do not add platform promises or release instructions.

- [ ] **Step 4: Run the focused visitor tests and verify green**

```text
python3 -m unittest tests.test_community_split.VisitorJourneyTests -v
```

Expected: PASS with every `VisitorJourneyTests` test successful. If a test fails, change only the inaccurate assertion or visitor prose; do not weaken protected-value, README-installation, or platform guards.

- [ ] **Step 5: Inspect the visitor journey as a stranger**

Read `README.md` from top to bottom without relying on repository knowledge. Confirm that `First run` reaches the latest-release path, names both assets and the exact archive digest, says Mac Apple Silicon only, ends at `bin/axloop-community`, and retains https://www.axloop.ai. Compare the release facts character-for-character with the changelog and release guide.

- [ ] **Step 6: Record the green-docs checkpoint**

Record `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` in the writer branch with checkpoint message `docs: tell the truth about community v0.1.0`. Do not merge or publish anything.

### Task 3: Run the fail-closed review bar

**Files:**

- Verify: `tests/test_community_split.py`
- Verify: `README.md`
- Verify: `CHANGELOG.md`
- Verify: `docs/COMMUNITY_RELEASES.md`
- Verify unchanged: `scripts/check-community-split.py`

**Interfaces:**

- Consumes: the red-green result from Tasks 1 and 2.
- Produces: fresh evidence that the documentation contract and existing Community boundary both pass.

- [ ] **Step 1: Run the complete Community test module**

```text
python3 -m unittest tests.test_community_split -v
```

Expected: PASS with zero failures and zero errors.

- [ ] **Step 2: Run the existing fail-closed checker from the repository root**

```text
python3 scripts/check-community-split.py .
```

Expected: exit status 0. Do not edit the checker to obtain this result.

- [ ] **Step 3: Run targeted public-copy scans**

```text
python3 - <<'PY'
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
docs = "\n".join(
    Path(path).read_text(encoding="utf-8")
    for path in ("README.md", "CHANGELOG.md", "docs/COMMUNITY_RELEASES.md")
)

required = (
    "v0.1.0",
    "darwin-arm64",
    "https://github.com/axloop/axloop-community/releases/latest",
)
missing = [value for value in required if value not in docs]
assert not missing, f"missing release facts: {missing}"
assert "```" not in readme, "README contains a fenced block"
assert "27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043" in readme
assert "bin/axloop-community" in readme
assert "https://www.axloop.ai" in readme
print("visitor-copy scan passed")
PY
```

Expected: `visitor-copy scan passed` and exit status 0.

- [ ] **Step 4: Perform the final scope audit**

Confirm from the writer's change list that only `tests/test_community_split.py`, `README.md`, `CHANGELOG.md`, and `docs/COMMUNITY_RELEASES.md` changed during implementation. Confirm there is no `.github` addition, workflow, application-code change, release or tag operation, extra asset, signing material, invented pack version, filled COMMENT slot, or content imported from PR #1 or #3.

- [ ] **Step 5: Apply the verification-before-completion gate**

Re-read the full output from Steps 1 through 3 and the audit from Step 4. Report completion only if the commands are fresh, all exit successfully, the focused red failure was observed before the green edits, and every scope item is satisfied. Report any discrepancy as a blocker instead of claiming success.

## Handoff

After Kit's qualifying GitHub COMMENT and Elena's verified execution, return the test outputs and scope audit to Abe. Do not merge until Abe explicitly directs it. This plan creates no additional release or publication step.
