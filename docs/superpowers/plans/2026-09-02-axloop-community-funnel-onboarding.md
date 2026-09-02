# AxLoop Community Funnel and Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn AxLoop Community into a polished, honest onboarding funnel whose tests prevent private-repository leakage, premature publishing, Community CI signing material, and the deferred CLI rename.

**Architecture:** Treat the README, changelog, and release guide as one visitor-facing release-discovery contract, with <https://www.axloop.ai> as the only enterprise destination. Invert the existing Python checker and its tests so all Community text, including Markdown, is scanned fail-closed while sensitive forbidden phrases are assembled from fragments and never stored literally in the repository.

**Tech Stack:** Markdown, Python standard library, `unittest`, existing `scripts/check-community-split.py` and `tests/test_community_split.py`, GitHub CLI for read-only release-state verification.

**Spec:** `docs/superpowers/specs/2026-09-02-axloop-community-funnel-onboarding-design.md`

## Global Constraints

- Base all implementation work on `axloop/axloop-community` `main` at `503de93d439f29fa2367d70b99da7d585d3363c5`; do not merge plan PR #1.
- This plan PR is docs-only. Implementation happens later in Cursor cloud with Claude Fable 5.1 at low effort, targeting Community `main`, after Imani and Reed review and Kit GitHub COMMENT-signs this plan.
- Do not treat an approval state as Kit's signature; the `ajrrac` login is shared.
- Remove private enterprise repository references and obsolete private-location/factory GitHub pointers everywhere, including Markdown. Assemble forbidden match values from fragments so the forbidden strings do not appear literally in repository files.
- Use <https://www.axloop.ai> as the enterprise destination. Do not run off-site marketing campaigns.
- Do not add application code, `.github` workflows, release automation, a release draft, a tag, a GitHub Release, publish commands, installable artifacts, or signing material.
- Keep PKCS#8 and signing-key secrets/configuration out of Community CI.
- Do not implement the CLI `radar` to `crawler` rename.
- Do not copy factory workflows or `src/`, `tools/`, or `packaging/` trees. Do not install Agent Stack or clone another repository.
- The 2026-08-29 acceptance-staging tag remains forbidden as release input.
- Jules is off. Nolan is required only if a workflow is added; no workflow is planned.
- Leave the Imani and Reed evidence slots unfilled until real citations exist. Do not invent versions.
- Do not merge unless Abe directs it.
- Before any completion claim, use `superpowers:verification-before-completion` and report fresh evidence from the full test, checker, scope, and live release-state gates in Task 3.

---

### Task 1: Invert the Community boundary policy with failing tests

**Files:**
- Modify: `tests/test_community_split.py`
- Modify: `scripts/check-community-split.py`

**Interfaces:**
- Consumes: repository root path and the existing checker entry point/CLI convention found in these two files.
- Produces: a zero exit status for a compliant tree; a nonzero exit status and category-level file diagnostic for prohibited content.

- [ ] **Step 1: Confirm the locked base before editing**

Run:

```bash
test "$(git rev-parse HEAD)" = "503de93d439f29fa2367d70b99da7d585d3363c5"
```

Expected: exit 0. If it fails, stop; do not merge or rebase plan PR #1 into the implementation branch.

- [ ] **Step 2: Add test helpers that assemble sensitive values without storing them literally**

In `tests/test_community_split.py`, retain the existing test framework and add helpers equivalent to:

```python
PRIVATE_REPO = "/".join(("ascendant" + "ventures", "axloop-edge" + "-poc"))
PRIVATE_URL = "https://" + "/".join(("github.com", PRIVATE_REPO))
OBSOLETE_LOCATION = " ".join(("enterprise", "stays", "in"))
STAGING_TAG = "-".join(("community", "acceptance", "staging", "2026", "08", "29"))

def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
```

Keep the repository's existing checker invocation helper rather than inventing a second execution path.

- [ ] **Step 3: Write failing policy tests**

Add explicit tests, using temporary fixture trees, for:

```python
def test_rejects_private_repo_reference_in_markdown(self):
    write(self.root, "README.md", PRIVATE_URL)
    result = self.run_checker()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("private repository reference", result.stdout + result.stderr)

def test_rejects_obsolete_location_language(self):
    write(self.root, "docs/boundary.md", OBSOLETE_LOCATION)
    self.assertNotEqual(self.run_checker().returncode, 0)

def test_rejects_published_release_metadata(self):
    write(self.root, ".community-release.json", '{"published_at":"2026-09-02"}')
    self.assertNotEqual(self.run_checker().returncode, 0)

def test_rejects_release_workflow(self):
    write(self.root, ".github/workflows/release.yml", "name: Publish release")
    self.assertNotEqual(self.run_checker().returncode, 0)

def test_rejects_signing_material_in_community_ci(self):
    write(self.root, ".github/workflows/ci.yml", "run: openssl pkcs8 -topk8")
    self.assertNotEqual(self.run_checker().returncode, 0)

def test_rejects_deferred_cli_rename(self):
    write(self.root, "README.md", "Run `axloop crawler` instead of the old command.")
    self.assertNotEqual(self.run_checker().returncode, 0)

def test_rejects_staging_tag_as_release_input(self):
    write(self.root, "release-input.txt", STAGING_TAG)
    self.assertNotEqual(self.run_checker().returncode, 0)
```

Also add cases for the private repository slug without a URL, a non-Markdown text file, a release-tag creation command, a signing-key secret reference under `.github/workflows/`, copied factory workflow language, and forbidden top-level `src/`, `tools/`, and `packaging/` trees. Diagnostics must name the file and rule category without echoing the sensitive value.

- [ ] **Step 4: Run the focused suite and verify the new cases fail for the intended reason**

Run:

```bash
python3 -m unittest -v tests.test_community_split
```

Expected: the new inversion cases fail because the current checker permits or requires the old documentation. Record each expected failure; fix test harness errors before proceeding.

- [ ] **Step 5: Implement the minimum checker inversion**

In `scripts/check-community-split.py`:

- remove every rule that requires a private repository URL, private “home” wording, or factory-copy disclaimer;
- construct sensitive match values from the same neutral fragments used by the tests;
- recursively scan repository text files, including `.md`, while excluding only `.git` internals and binary/unreadable files;
- report relative file paths and stable categories such as `private repository reference`, `release publication`, `Community CI signing material`, and `deferred CLI rename`;
- reject release workflows, release/publish commands, tag-creation instructions, nonempty release metadata, use of the staging tag as release input, signing material in Community CI, the CLI rename, copied factory workflows, and forbidden implementation trees;
- allow ordinary enterprise prose and the exact public website `https://www.axloop.ai`.

Use only the Python standard library and preserve the existing CLI/entry-point contract.

- [ ] **Step 6: Run the focused suite and verify it passes**

Run:

```bash
python3 -m unittest -v tests.test_community_split
```

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 7: Commit the independently reviewable policy inversion**

```bash
git add scripts/check-community-split.py tests/test_community_split.py
git commit -m "test: invert community boundary policy"
```

### Task 2: Build the stranger-first Community funnel

**Files:**
- Modify: `README.md`
- Create: `CHANGELOG.md`
- Modify: `docs/COMMUNITY_RELEASES.md`
- Test: `tests/test_community_split.py`

**Interfaces:**
- Consumes: the checker behavior from Task 1 and this repository's GitHub Releases URL derived from `axloop/axloop-community`.
- Produces: one consistent visitor journey across README, changelog, and release guide.

- [ ] **Step 1: Add failing visitor-journey tests**

Add tests that read the real repository documents and assert:

```python
def test_readme_has_stranger_first_run_and_public_funnel(self):
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    self.assertIn("First run", readme)
    self.assertIn("https://www.axloop.ai", readme)
    self.assertIn("releases/latest", readme)
    self.assertRegex(readme.lower(), r"no .*release .*published")

def test_release_docs_are_honest_and_consistent(self):
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    guide = (REPO_ROOT / "docs/COMMUNITY_RELEASES.md").read_text(encoding="utf-8")
    self.assertIn("## [Unreleased]", changelog)
    self.assertRegex(changelog.lower(), r"no .*release .*published")
    self.assertIn("releases/latest", guide)
    self.assertRegex(guide.lower(), r"no .*release .*published")
```

Use the repository's actual `REPO_ROOT` convention. Add assertions that the README does not present source checkout as an install and that none of the three documents contains assembled prohibited values.

- [ ] **Step 2: Run the visitor tests and verify they fail**

Run:

```bash
python3 -m unittest -v tests.test_community_split
```

Expected: failures identify the missing changelog, missing first-run/release path, or stale private-boundary copy.

- [ ] **Step 3: Rewrite `README.md` around the visitor journey**

Use this exact information hierarchy:

```markdown
# AxLoop Community

[One concise sentence describing the Community offering without claims not supported by the repository.]

## First run

1. Check the [latest GitHub Release](https://github.com/axloop/axloop-community/releases/latest) for the newest install.
2. No Community GitHub Release has been published yet. Until one appears, there is no supported Community install to run.
3. Read the [changelog](CHANGELOG.md) for notable Community changes and current release status.

## Enterprise

For the AxLoop enterprise product, visit [axloop.ai](https://www.axloop.ai).

## Release information

See [Community releases](docs/COMMUNITY_RELEASES.md) for how versions and installs will be announced.
```

Style with restrained badges or separators only if their targets already exist and remain accurate. Do not add fabricated install commands, a private GitHub destination, factory-boundary copy, or campaign tracking parameters.

- [ ] **Step 4: Create `CHANGELOG.md` with an honest unreleased state**

Write Keep a Changelog-shaped content:

```markdown
# Changelog

Notable changes to AxLoop Community are recorded here.

## [Unreleased]

### Changed

- Refined Community onboarding and release discovery.

No Community GitHub Release has been published yet. When one is available, find the latest install on the [GitHub Releases page](https://github.com/axloop/axloop-community/releases/latest).
```

Do not add a released version, date, comparison link, tag, artifact, or inferred Imani/Reed version.

- [ ] **Step 5: Rewrite `docs/COMMUNITY_RELEASES.md` as the release-discovery contract**

Cover only these concrete points:

- `CHANGELOG.md` records notable Community changes under `Unreleased`.
- `https://github.com/axloop/axloop-community/releases/latest` is where the latest install will appear.
- No Community GitHub Release has been published yet.
- This change creates no release, tag, artifact, draft, or publishing workflow.
- Release signing material never belongs in Community CI.
- The historical 2026-08-29 acceptance-staging tag is not a release input.

Do not name a private repository, a machine owner, or a private key location. Do not describe the deferred CLI rename.

- [ ] **Step 6: Run the focused suite and checker**

Run:

```bash
python3 -m unittest -v tests.test_community_split
python3 scripts/check-community-split.py .
```

Expected: both commands exit 0; the unit-test output has zero failures and zero errors, and the checker reports no policy violations.

- [ ] **Step 7: Commit the independently reviewable funnel**

```bash
git add README.md CHANGELOG.md docs/COMMUNITY_RELEASES.md tests/test_community_split.py
git commit -m "docs: add community funnel and onboarding"
```

### Task 3: Apply the Superpowers verification and governance gate

**Files:**
- Verify: `README.md`
- Verify: `CHANGELOG.md`
- Verify: `docs/COMMUNITY_RELEASES.md`
- Verify: `scripts/check-community-split.py`
- Verify: `tests/test_community_split.py`
- Verify: `docs/superpowers/specs/2026-09-02-axloop-community-funnel-onboarding-design.md`
- Verify: `docs/superpowers/plans/2026-09-02-axloop-community-funnel-onboarding.md`

**Interfaces:**
- Consumes: Tasks 1 and 2 plus live GitHub release metadata.
- Produces: fresh evidence that the source tree and external release state satisfy the design before any completion claim or merge request.

- [ ] **Step 1: Run the complete repository test command**

```bash
python3 -m unittest discover -s tests -v
```

Expected: exit 0 with zero failures and zero errors. Read the full output; do not infer success from the focused tests.

- [ ] **Step 2: Run the checker against the complete worktree**

```bash
python3 scripts/check-community-split.py .
```

Expected: exit 0 and no policy violations, including in Markdown and these Superpowers documents.

- [ ] **Step 3: Prove no prohibited files or implementation trees were added**

```bash
python3 - <<'PY'
from pathlib import Path

root = Path(".")
forbidden = [root / ".github", root / "src", root / "tools", root / "packaging"]
present = [str(path) for path in forbidden if path.exists()]
if present:
    raise SystemExit("unexpected paths: " + ", ".join(present))
PY
```

Expected: exit 0 with no output.

- [ ] **Step 4: Verify the live GitHub release state without mutating it**

```bash
test "$(gh api 'repos/axloop/axloop-community/releases?per_page=1' --jq 'length')" = "0"
```

Expected: exit 0, proving no GitHub Release is published. This command is read-only. If authentication or network access fails, stop and report that the external-state gate is unverified; do not skip or substitute a source-tree inference.

- [ ] **Step 5: Verify there are no release tags without creating or fetching any**

```bash
test -z "$(git tag --list)"
```

Expected: exit 0. Do not create, delete, push, or fetch tags.

- [ ] **Step 6: Verify the exact change scope**

```bash
git diff --name-only 503de93d439f29fa2367d70b99da7d585d3363c5...HEAD
```

Expected output contains only:

```text
CHANGELOG.md
README.md
docs/COMMUNITY_RELEASES.md
scripts/check-community-split.py
tests/test_community_split.py
```

The two Superpowers documents belong to the separately reviewed docs-only plan PR and are not merged from plan PR #1. Any workflow, application, artifact, or other path is a gate failure.

- [ ] **Step 7: Perform the human-readable acceptance walkthrough**

Open `README.md` as a stranger and verify, in order: Community identity, `First run`, the latest-release link, the explicit no-release notice, the changelog link, and the <https://www.axloop.ai> enterprise link. Follow the local links and confirm the changelog and release guide repeat the same release state without a fabricated install command.

Expected: all seven visitor outcomes are visible and mutually consistent. Record the reviewed commit SHA and evidence in the implementation handoff.

- [ ] **Step 8: Enforce the review sequence before implementation or merge**

Fill only real references into the design's evidence slots in this order: Imani review, Reed review, then Kit's GitHub COMMENT signature. Do not use an approval state as the Kit gate. Keep Jules off; because no workflow is added, do not add Nolan to the default path.

Expected: all three references exist before Elena starts the Cursor cloud Claude Fable 5.1 low implementation. No merge occurs unless Abe gives a separate direction.

- [ ] **Step 9: Stop at verified implementation; do not publish**

Do not run `gh release create`, `git tag`, `git push --tags`, a publishing workflow, or any equivalent mutation. Report the fresh outputs from Steps 1–7 and hand the branch back for review.
