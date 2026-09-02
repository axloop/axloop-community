# AxLoop Community v0.1.0 Honesty Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Community visitor docs and visitor tests match live GitHub Release `v0.1.0` (Mac Apple Silicon only) without publishing anything new.

**Architecture:** Keep README, CHANGELOG, and the release guide as one release-discovery contract. Invert `VisitorJourneyTests` first so they fail on the unpublished lie, then update the three docs. Leave the checker and its unpublished fixture trees alone unless a visitor-test change requires a checker edit.

**Tech Stack:** Markdown, Python `unittest`, existing `scripts/check-community-split.py` and `tests/test_community_split.py`.

**Spec:** `docs/superpowers/specs/2026-09-02-axloop-community-v010-honesty-design.md`

## Global Constraints

- Base implementation on `axloop/axloop-community` `main` at `81c55c0eebee70d6e4364dda24605f0c435f722d`. Do not merge leftover plan PR #1 or #3 into this work.
- This plan document is docs-only. Later, Elena launches Cursor cloud Claude Fable 5.1 (`claude-fable-5-1`) at effort low against Community `main` only after Kit GitHub COMMENT-signs this plan. APPROVE does not count because `ajrrac` is a shared login.
- Live release is already `v0.1.0`. Do not create another tag or GitHub Release. Do not upload assets. Do not add `.github`.
- Named install: `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` with SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`, plus adjacent `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`. Mac Apple Silicon only. Do not claim linux or windows installs.
- Enterprise destination is https://www.axloop.ai only. Do not name any other GitHub owner or repository.
- README must not contain a code fence, `git clone`, `pip install`, or `curl`.
- Do not mention any historical staging identifier in visitor docs.
- Signing material never belongs in Community CI. Do not add PKCS#8, keys, or signing commands to this repository.
- Do not implement the CLI `radar` to `crawler` rename.
- Do not copy factory trees (`src/`, `tools/`, `packaging/`) or factory workflows. Do not install Agent Stack. Do not clone. Do not detach any Mac checkout.
- Jules is off. Nolan is required only if a workflow is added; no workflow is planned.
- Leave Imani and Reed evidence slots unfilled. Do not invent pack versions.
- Do not merge unless Abe directs it.
- Every implementation task follows red-green TDD. Before any completion claim, use `superpowers:verification-before-completion` and report fresh command output.

**Writer brief:** Make Community visitor docs honest about live GitHub Release `v0.1.0` (Mac Apple Silicon, darwin-arm64 archive `axloop-community-darwin-arm64-3a7bfeeb.tar.gz`, SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`). Invert visitor tests first. Do not publish anything new.

---

### Task 1: Invert visitor honesty tests

**Files:**
- Modify: `tests/test_community_split.py`

**Interfaces:**
- Consumes: real `README.md`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md` on the implementation branch.
- Produces: `VisitorJourneyTests` that fail on current `81c55c0` unpublished copy and pass only after Task 2.

- [ ] **Step 1: Confirm the locked base**

```bash
test "$(git rev-parse HEAD)" = "81c55c0eebee70d6e4364dda24605f0c435f722d" || git merge-base --is-ancestor 81c55c0eebee70d6e4364dda24605f0c435f722d HEAD
```

Expected: exit 0. Stop if this branch is not based on that SHA.

- [ ] **Step 2: Rewrite VisitorJourneyTests for the live release**

In `tests/test_community_split.py`, keep checker fixture trees unpublished. Change only `VisitorJourneyTests`:

- `test_readme_has_stranger_first_run_and_public_funnel` still requires First run, https://www.axloop.ai, `releases/latest`, `CHANGELOG.md`, `docs/COMMUNITY_RELEASES.md`. Replace the unpublished regex with requirements that README names `v0.1.0`, `darwin-arm64`, `bin/axloop-community`, and SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`. Assert README does **not** match `no .*release .*published`.
- `test_readme_does_not_present_source_checkout_as_install` stays (no clone, pip, curl, no triple-backtick fence).
- `test_release_docs_are_honest_and_consistent` requires `## [Unreleased]` **and** `## [0.1.0] - 2026-09-02`. Remove the unpublished regex and remove `no released version may be listed`. Require changelog and guide to name `v0.1.0` / latest release / darwin-arm64, and to say linux and windows installs are not published. Guide must not claim this docs change creates a release.
- `test_documents_contain_no_prohibited_values` stays.
- `test_real_repository_passes_checker` stays.

- [ ] **Step 3: Run tests and observe the intended failure**

```bash
python3 -m unittest tests.FAKESECRET_e2f3g4h5i6j7k8l9m0n1 tests.FAKESECRET_i2j3k4l5m6n7o8p9q0r1 tests.FAKESECRET_u2v3w4x5y6z7a8b9c0d1 -v
```

Expected: those cases FAIL on current unpublished docs. Checker fixture tests still pass. If visitor tests pass on unpublished docs, the inversion is wrong; stop.

- [ ] **Step 4: Commit**

```bash
git add tests/test_community_split.py
git commit -m "test: require honest v0.1.0 visitor docs"
```

---

### Task 2: Make visitor docs match v0.1.0

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/COMMUNITY_RELEASES.md`

**Interfaces:**
- Consumes: live release facts in the spec.
- Produces: one stranger-first contract that a visitor can follow to the Mac install.

- [ ] **Step 1: Update README First run**

Keep identity, First run, enterprise at https://www.axloop.ai, release guide link, issues link. Replace the unpublished paragraph. First run, in order, without a code fence:

1. Open the [latest GitHub Release](https://github.com/axloop/axloop-community/releases/latest).
2. Download `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` and `axloop-community-darwin-arm64-3a7bfeeb-SHA256SUMS`.
3. Confirm the archive SHA-256 is `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`.
4. Unpack, then run `bin/axloop-community`.
5. This install is Mac Apple Silicon only. No linux or windows Community install is published yet.

- [ ] **Step 2: Update CHANGELOG**

Keep Keep a Changelog and `## [Unreleased]` (empty or later-work only). Add:

```markdown
## [0.1.0] - 2026-09-02

### Added

- First Community GitHub Release: Mac Apple Silicon (`darwin-arm64`) archive `axloop-community-darwin-arm64-3a7bfeeb.tar.gz` (SHA-256 `27e993467ee3b57c891c416ab5963032020b38218f2c57d890f094f791ca2043`).
```

Drop every unpublished lie. Do not list linux or windows.

- [ ] **Step 3: Update the release guide**

Current state: `v0.1.0` is published at the latest-release URL. Darwin only. Point at CHANGELOG. Say this documentation change creates no new release, tag, artifact, or workflow. Signing material never belongs in Community CI. Do not mention any historical staging identifier.

- [ ] **Step 4: Re-run visitor tests and the checker**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-community-split.py .
```

Expected: all tests OK, checker PASS. If either fails, fix docs or tests; do not weaken the prohibited-value checks.

- [ ] **Step 5: Commit**

```bash
git add README.md CHANGELOG.md docs/COMMUNITY_RELEASES.md
git commit -m "docs: honest v0.1.0 Mac Community install"
```

---

### Task 3: Verify scope and live release state

- [ ] **Step 1: Confirm this change did not publish**

Read-only checks. Do not create or edit a release.

```bash
git diff --name-only 81c55c0eebee70d6e4364dda24605f0c435f722d...HEAD
gh api repos/axloop/axloop-community/releases/latest --jq '.tag_name'
```

Expected: only the four named files (tests + three docs). Latest tag remains `v0.1.0`. Stop if any extra path or a new tag appears.

- [ ] **Step 2: Walk the README as a stranger**

Confirm First run order, both asset names, archive SHA-256, `bin/axloop-community`, Mac Apple Silicon only, https://www.axloop.ai, no code fence.

- [ ] **Step 3: Report**

Record unittest output, checker output, file list, and latest tag. Do not claim live-pass from chat. Do not merge.

## Evidence slots

- Imani pack:
- Reed critic:
- Kit COMMENT:
