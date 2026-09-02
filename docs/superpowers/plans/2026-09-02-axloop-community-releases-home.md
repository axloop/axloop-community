# AxLoop Community Releases Home Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `axloop/axloop-community` the documented home for Community artifacts and GitHub Releases while leaving the complete source, build, signing, and acceptance factory in enterprise and publishing nothing.

**Architecture:** Use a documentation-first ownership boundary: Community explains where releases live and points to enterprise for the unchanged factory. An optional Community workflow may attach already-signed, already-accepted artifacts to a draft release only; it is omitted unless its exact handoff and least-privilege access can be proven and Nolan reviews it.

**Tech Stack:** Markdown, GitHub Actions YAML only if the optional workflow is selected, GitHub CLI for draft-only release operations only if selected, POSIX shell and Python standard library for review checks.

**Spec:** `docs/superpowers/specs/2026-09-02-axloop-community-releases-home-design.md`

## Global Constraints

- This plan PR is docs-only and must be based on `axloop/axloop-community` `main` at `f5746a39`.
- **Community artifacts + GitHub Releases:** https://github.com/axloop/axloop-community (private, `main` currently README-only at `f5746a39`).
- **Enterprise source, build, signing, acceptance:** https://github.com/ascendantventures/axloop-edge-poc (`main` at `9af8caac`). Do not rename, transfer, or copy that tree.
- Community is the Releases home, not a copy or mirror of the enterprise factory.
- Do not publish a release or add any path that can publish one.
- Do not use, promote, copy, retag, attach, publish, or accept as input the enterprise Aug 29 staging tag `community-acceptance-staging-2026-08-29`.
- CLI `radar`→`crawler` is later and must not land in this split.
- Enterprise retains `community-bundles.yml`, `community-inputs.yml`, `community-windows-input-review.yml`, `community-acceptance.yml`, `tools.community_*`, `release/`, and all source/build/signing/acceptance machinery.
- PKCS#8 stays on Abe's Mac and never enters Community or Community CI.
- Do not install Agent Stack, clone a repository, rename or transfer a repository, or run publication automation.
- Kit GitHub-signs this plan with COMMENT before Elena launches the implementation writer; chat approval and APPROVE are not the gate.
- The implementation writer is Cursor cloud Claude Fable 5.1 low (`claude-fable-5-1`, effort `low`) targeting `axloop/axloop-community` `main` after Kit's GitHub signature.
- Do not merge anything unless Abe explicitly says to merge.
- No Imani pack exists yet. Preserve the Imani-then-Reed citation slots without inventing versions.
- If a Community workflow is added, Nolan scores secrets/access on the writer PR before acceptance.
- Before any completion claim, use `superpowers:verification-before-completion`, run every applicable check in this plan fresh, read the full output, and report actual results.

---

### Task 1: Establish the Community/enterprise ownership boundary in docs

**Files:**
- Modify: `README.md`
- Create: `docs/COMMUNITY_RELEASES.md`

**Interfaces:**
- Consumes: the locked repository ownership and SHA facts in the design spec.
- Produces: a reader-visible five-fact contract and a stable `docs/COMMUNITY_RELEASES.md` link from the README.

- [ ] **Step 1: Write a failing documentation contract check**

Run this from the `axloop/axloop-community` root before editing:

```bash
python3 - <<'PY'
from pathlib import Path

readme = Path("README.md").read_text()
release_doc = Path("docs/COMMUNITY_RELEASES.md")
assert release_doc.is_file(), "missing docs/COMMUNITY_RELEASES.md"
text = readme + "\n" + release_doc.read_text()
required = {
    "Community home": "https://github.com/axloop/axloop-community",
    "enterprise home": "https://github.com/ascendantventures/axloop-edge-poc",
    "no publication": "No Community release has been published",
    "excluded staging tag": "community-acceptance-staging-2026-08-29",
    "deferred CLI rename": "radar→crawler",
}
missing = [name for name, phrase in required.items() if phrase not in text]
assert not missing, f"missing Community ownership facts: {missing}"
print("PASS: Community ownership facts are documented")
PY
```

Expected: FAIL because `docs/COMMUNITY_RELEASES.md` does not exist on the README-only baseline.

- [ ] **Step 2: Write the minimal Community documentation**

Update `README.md` to identify this private repository as the home for Community artifacts and GitHub Releases, state that enterprise remains the factory, and link `docs/COMMUNITY_RELEASES.md`. Create `docs/COMMUNITY_RELEASES.md` with these exact facts:

```markdown
# Community releases

Community artifacts and GitHub Releases live in this private repository: https://github.com/axloop/axloop-community.

Enterprise source, build, signing, and acceptance remain in https://github.com/ascendantventures/axloop-edge-poc. This repository is the Releases home, not a copy of that factory.

No Community release has been published from this repository yet. The enterprise Aug 29 staging draft tagged `community-acceptance-staging-2026-08-29` is not a Community release, is not this repository's release home, and must not be used, copied, retagged, attached, or published.

The CLI `radar`→`crawler` rename is later and is not part of this split.

The enterprise repository retains Community builds, signing requests, attended signing with PKCS#8 on Abe's Mac, offline verification, release envelopes, clean-host acceptance, notarization, and Authenticode gates. PKCS#8 never enters this repository or CI.
```

Do not copy enterprise documentation into Community; keep the page focused on ownership and safety boundaries.

- [ ] **Step 3: Run the documentation contract check and verify it passes**

Re-run the exact Python command from Step 1.

Expected: `PASS: Community ownership facts are documented` and exit code 0.

- [ ] **Step 4: Review the rendered text for false ownership claims**

Run:

```bash
rg -n -i 'builds? here|signs? here|accepts? here|publish(es|ed)? here' README.md docs/COMMUNITY_RELEASES.md
```

Expected: no output and exit code 1. Manually confirm links render and the “not a copy of that factory” sentence is unambiguous.

- [ ] **Step 5: Prepare the task commit for review; do not merge**

After the checks pass, the writer may create a normal task commit on the writer branch. Do not merge, publish, tag, or create a release. Suggested commit message: `docs: define Community releases home`.

### Task 2: Add executable boundary checks

**Files:**
- Create: `scripts/check-community-split.py`
- Create: `tests/test_community_split.py`

**Interfaces:**
- Consumes: Community repository file paths and text from Task 1; optional workflow paths from Task 3 if that task is selected.
- Produces: `scripts/check-community-split.py` with exit code 0 for an allowed tree and nonzero for any forbidden ownership, publication, staging-tag-input, CLI-rename, or signing-key condition; `tests/test_community_split.py` proves each negative rule fails.

- [ ] **Step 1: Write failing tests for every hard boundary**

Use Python's standard-library `unittest`, temporary directories, and subprocess invocation of `scripts/check-community-split.py`. Define one fixture for a minimal valid Community tree, then tests that add one forbidden condition at a time:

```python
def test_rejects_enterprise_src_copy(): ...
def test_rejects_enterprise_tools_copy(): ...
def test_rejects_factory_workflow_copy(): ...
def test_rejects_release_publish_step(): ...
def test_rejects_aug_29_tag_as_input(): ...
def test_rejects_radar_to_crawler_change(): ...
def test_rejects_signing_key_in_ci(): ...
def test_accepts_docs_only_tree(): ...
def test_accepts_explicitly_draft_only_workflow(): ...
```

Each rejection test must assert a nonzero return code and a diagnostic naming the violated rule. The staging test must place `community-acceptance-staging-2026-08-29` in workflow inputs or executable workflow configuration, not merely in explanatory Markdown; documentation must be allowed to disclaim the tag. The CLI test must detect a rename/diff intent, not reject the required sentence saying that the rename is deferred.

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest -v tests/test_community_split.py
```

Expected: FAIL because `scripts/check-community-split.py` does not exist.

- [ ] **Step 3: Implement the minimal repository-boundary checker**

Implement the checker with Python standard-library path walking and YAML-as-text policy checks; add no dependency or package setup. It must:

- reject top-level enterprise tree copies: `src`, `tools`, `packaging`, `hosted`, `supabase`, `acceptance`, and `release`;
- reject enterprise project files: `verify.py`, `pyproject.toml`, `setup.py`, `DESIGN.md`, and `PRODUCT.md`;
- reject workflow names `community-bundles.yml`, `community-inputs.yml`, `community-windows-input-review.yml`, and `community-acceptance.yml`;
- reject workflow command/config lines that publish a release, set `draft: false`, remove draft state, or edit a draft into a published release;
- reject the Aug 29 tag in workflow inputs or executable workflow configuration while allowing its explanatory mention in Markdown;
- reject files or workflow lines implementing a `radar`→`crawler` rename while allowing the explicit deferred-scope documentation;
- reject private-key/PKCS#8 material, signing commands, signing-key inputs, and signing-key secret references under `.github/workflows`;
- permit Markdown docs and an optional workflow whose release creation explicitly remains draft-only.

The checker must print all violations before exiting nonzero so review does not stop at the first problem.

- [ ] **Step 4: Run unit and live-tree checks**

Run:

```bash
python3 -m unittest -v tests/test_community_split.py
python3 scripts/check-community-split.py .
```

Expected: all nine tests PASS; the live-tree check prints a PASS summary and exits 0.

- [ ] **Step 5: Prepare the task commit for review; do not merge**

After the checks pass, the writer may create a normal task commit on the writer branch. Do not merge. Suggested commit message: `test: enforce Community repository boundary`.

### Task 3: Decide whether to add the optional draft-only attachment workflow

**Files:**
- Optional create: `.github/workflows/community-draft-release.yml`
- Modify: `docs/COMMUNITY_RELEASES.md` only if the optional workflow is added
- Test: `tests/test_community_split.py`

**Interfaces:**
- Consumes: already-signed, already-accepted artifact files supplied to Community through a documented, non-Aug-29 handoff; the checker from Task 2.
- Produces: either no workflow (the recommended default) or a manual, least-privilege draft-only attachment workflow reviewed by Nolan.

- [ ] **Step 1: Apply the omission gate**

Default to omitting the workflow. Add it only if the writer PR can state the exact artifact handoff, prove the artifacts are already signed and accepted, enumerate required permissions, and obtain Nolan's secrets/access score. If any item is unavailable, record in the PR body: `Optional draft workflow omitted; documentation establishes the Releases home.` Then skip to Task 4.

- [ ] **Step 2: If selected, extend the failing tests before adding YAML**

Add tests proving that the planned workflow:

- rejects `draft: false` and any `gh release edit ... --draft=false` or publish command;
- rejects the Aug 29 tag in inputs, defaults, environment variables, and executable steps;
- rejects checkout or download of `ascendantventures/axloop-edge-poc` source;
- rejects signing commands and key-shaped secret references;
- accepts an explicit `draft: true` create operation and attachment to a Community-local draft.

Run:

```bash
python3 -m unittest -v tests/test_community_split.py
```

Expected: FAIL on at least the new valid-workflow expectation because the workflow is absent.

- [ ] **Step 3: If selected, add the minimum manual draft workflow**

Create `.github/workflows/community-draft-release.yml` with `workflow_dispatch`, least-privilege `contents: write`, an input for a new Community-local release tag that has no default and explicitly rejects the Aug 29 tag, and an artifact handoff that never checks out enterprise source. Every release-create command must pass `--draft`; attachment may target only the Community repository's draft. Do not add a publish input, boolean switch, scheduled trigger, signing step, signing secret, enterprise checkout, or build/acceptance step.

Document the exact handoff and the fact that the workflow cannot publish in `docs/COMMUNITY_RELEASES.md`. Do not execute the workflow during this change.

- [ ] **Step 4: If selected, run policy checks and obtain Nolan's score**

Run:

```bash
python3 -m unittest -v tests/test_community_split.py
python3 scripts/check-community-split.py .
rg -n 'permissions:|contents: write|workflow_dispatch|--draft|draft: true' .github/workflows/community-draft-release.yml
```

Expected: all tests and the live-tree checker PASS; `rg` shows only the manual trigger, least-privilege release permission, and explicit draft controls. Request Nolan's secrets/access score on the writer PR and do not accept the workflow until that score is recorded. PKCS#8 must remain absent from Community.

- [ ] **Step 5: If selected, prepare the task commit for review; do not merge**

After checks and Nolan's score, the writer may create a normal task commit on the writer branch. Do not run the workflow and do not merge. Suggested commit message: `ci: add draft-only Community release attachment`.

### Task 4: Run the completion gate and prepare the unsigned writer handoff

**Files:**
- Modify: writer PR description only; no additional repository file is required

**Interfaces:**
- Consumes: the Community documentation, boundary checker/tests, and optional workflow decision.
- Produces: fresh verification evidence for reviewers and citation slots for later Imani then Reed review; it does not produce a release or merge.

- [ ] **Step 1: Confirm repository scope and required facts**

Run:

```bash
python3 -m unittest -v tests/test_community_split.py
python3 scripts/check-community-split.py .
python3 - <<'PY'
from pathlib import Path

text = Path("README.md").read_text() + "\n" + Path("docs/COMMUNITY_RELEASES.md").read_text()
for phrase in (
    "https://github.com/axloop/axloop-community",
    "https://github.com/ascendantventures/axloop-edge-poc",
    "No Community release has been published",
    "community-acceptance-staging-2026-08-29",
    "radar→crawler",
    "PKCS#8 never enters",
):
    assert phrase in text, phrase
print("PASS: live user path and safety statements are present")
PY
```

Expected: all unit tests PASS, the live-tree checker PASSes, and the documentation check prints its PASS line.

- [ ] **Step 2: Inspect the proposed change list without merging**

Using the code-review UI or another read-only change listing approved by the execution environment, confirm the writer change contains only:

- Community documentation;
- `scripts/check-community-split.py` and its standard-library tests; and
- optionally, `.github/workflows/community-draft-release.yml` plus its documentation/tests.

Fail review if enterprise source, tools, factory workflows, release machinery, CLI rename work, Agent Stack, keys, or unrelated files appear. Do not use this step to authorize cloning, publication, or merge.

- [ ] **Step 3: Apply verification-before-completion**

Invoke `superpowers:verification-before-completion`. Re-run every applicable command from Steps 1 and 2 fresh, read the complete output, count failures, and state the actual results in the writer PR. Do not claim that the boundary is complete based on earlier or partial output.

If the optional workflow exists, additionally confirm Nolan's secrets/access score is present and that no PKCS#8 or signing-key secret is referenced. If it does not exist, state that the safe documentation-only default was retained.

- [ ] **Step 4: Preserve review-pack slots without invented versions**

Put these literal placeholders in the writer PR description, not in product documentation:

```markdown
- Imani pack: [cite after this plan exists]
- Reed review, after Imani: [cite after the Imani pack lands]
```

Replace them only when the named artifacts actually exist. Imani precedes Reed.

- [ ] **Step 5: Hand off for gated review; do not publish or merge**

Report the tested writer HEAD for review. The later live-pass stamp must be `/workspace/gates/axloop-community-pr<n>-<sha7>.md` and match HEAD; text saying `LIVE PASS` in the writer body is not the stamp. Do not publish a release. Do not merge unless Abe explicitly says to merge.
